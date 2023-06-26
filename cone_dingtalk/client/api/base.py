from urllib.parse import urljoin
from alibabacloud_dingtalk.oauth2_1_0.client import Client as OauthClient
from alibabacloud_dingtalk.oauth2_1_0.models import GetAccessTokenRequest
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.robot_1_0 import models as dingtalkrobot__1__0_models
from cachetools import TTLCache
from requests import request
import time
import json
import os
import requests


access_token_cache = TTLCache(maxsize=10, ttl=7200)


class DingTalkBaseAPI(object):

    API_BASE_URL = None

    def __init__(self, access_key_id=None, access_key_secret=None):
        access_key_id = access_key_id or os.environ.get('DINGTALK_ACCESS_KEY_ID')
        access_key_secret = access_key_secret or os.environ.get('DINGTALK_ACCESS_KEY_SECRET')
        assert access_key_id and access_key_secret, "access_key_id and access_key_secret must be provided"
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

    def request_access_token(self):
        raise NotImplementedError

    @property
    def access_token(self):
        key = f"{self.access_key_id}:{self.access_key_secret}"
        try:
            return access_token_cache[key]
        except KeyError:
            return self.request_access_token()


class DingTalkV1API(DingTalkBaseAPI):
    # 旧版API
    BASE_URL = 'https://oapi.dingtalk.com/'

    def sign(self):
        pass

    def request_access_token(self):
        response = requests.get(
            urljoin(self.BASE_URL, 'gettoken'),
            params={'appkey': self.access_key_id, 'appsecret': self.access_key_secret},
            headers={'Content-Type': 'application/json'},
        )
        return response.json()['access_token']

    def _handle_result(self, res, method=None, url=None, result_processor=None, top_response_key=None, **kwargs):
        if not isinstance(res, dict):
            # Dirty hack around asyncio based AsyncWeChatClient
            result = self._decode_result(res)
        else:
            result = res

        if not isinstance(result, dict):
            return result
        if top_response_key:
            if 'error_response' in result:
                error_response = result['error_response']
                logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                             url, kwargs.get('params', ''), kwargs.get('data', ''), result)
                raise DingTalkClientException(
                    error_response.get('code', -1),
                    error_response.get('sub_msg', error_response.get('msg', '')),
                    client=self,
                    request=res.request,
                    response=res
                )
            top_result = result
            if top_response_key in top_result:
                top_result = result[top_response_key]
                if 'result' in top_result:
                    top_result = top_result['result']
                    if isinstance(top_result, six.string_types):
                        try:
                            top_result = json_loads(top_result)
                        except Exception:
                            pass
            if isinstance(top_result, dict):
                if ('success' in top_result and not top_result['success']) or (
                        'is_success' in top_result and not top_result['is_success']):
                    logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                                 url, kwargs.get('params', ''), kwargs.get('data', ''), result)
                    raise DingTalkClientException(
                        top_result.get('ding_open_errcode', -1),
                        top_result.get('error_msg', ''),
                        client=self,
                        request=res.request,
                        response=res
                    )
            result = top_result
        if not isinstance(result, dict):
            return result
        if 'errcode' in result:
            result['errcode'] = int(result['errcode'])

        if 'errcode' in result and result['errcode'] != 0:
            errcode = result['errcode']
            errmsg = result.get('errmsg', errcode)

            logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                         url, kwargs.get('params', ''), kwargs.get('data', ''), result)
            raise DingTalkClientException(
                errcode,
                errmsg,
                client=self,
                request=res.request,
                response=res
            )

        return result if not result_processor else result_processor(result)

    def _request(self, path, method='POST', params=None, **kwargs):
        params = params or {}
        if 'access_token' not in params:
            params['access_token'] = self.access_token
        result = request(method, urljoin(self.BASE_URL, path),
                         headers=self.get_request_header(),
                         params=params, **kwargs).json()
        # result = self._handle_result(
        #     res, method, url, result_processor, top_response_key, **kwargs
        # )
        #
        # logger.debug("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【响应数据】：%s",
        #              url, kwargs.get('params', ''), kwargs.get('data', ''), result)
        return result

    def get_request_header(self):
        return {
            'Content-type': 'application/json;charset=UTF-8',
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
        }

    def request(self, params=None, **kwargs):
        params = params or {}
        header = self.get_request_header()


class DingTalkV2API(DingTalkBaseAPI):
    # 新版API

    def request_access_token(self):
        oauth_client = OauthClient(
            config=open_api_models.Config(
                protocol='https',
                region_id='central',
                access_key_id=self.access_key_id,
                access_key_secret=self.access_key_secret,
            )
        )
        get_access_token_request = GetAccessTokenRequest(
            app_key=self.access_key_id,
            app_secret=self.access_key_secret,
        )
        try:
            ret = oauth_client.get_access_token(get_access_token_request)
            return ret.body.to_map()['accessToken']
        except Exception as err:
            code, msg = getattr(err, 'code', None), getattr(err, 'message', None)
            if code:
                raise Exception(f'{code}: {msg}')
            raise err


if __name__ == '__main__':
    # api_v2 = DingTalkV2API(
    #     access_key_id='dinghkwyfwu272bbhve4',
    #     access_key_secret='ea6y5jBRZ2hJ2u1Z3LXBkaz78qH85RKXqSWj830sLF5agsvFHJnURCsOrtmu7Gez',
    # )
    # print(api_v2.access_token)

    api_v1 = DingTalkV1API(
        access_key_id='dinghkwyfwu272bbhve4',
        access_key_secret='ea6y5jBRZ2hJ2u1Z3LXBkaz78qH85RKXqSWj830sLF5agsvFHJnURCsOrtmu7Gez',
    )
    print(api_v1.access_token)
