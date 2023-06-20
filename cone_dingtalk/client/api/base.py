from alibabacloud_dingtalk.oauth2_1_0.client import Client as OauthClient
from alibabacloud_dingtalk.oauth2_1_0.models import GetAccessTokenRequest
from alibabacloud_tea_openapi import models as open_api_models
from cachetools import TTLCache


access_token_cache = TTLCache(maxsize=10, ttl=7200)


class DingTalkBaseAPI(object):

    API_BASE_URL = None

    def __init__(self, access_key_id, access_key_secret):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self._oauth_client = OauthClient(
            config=open_api_models.Config(
                protocol='https',
                region_id='central',
                access_key_id=access_key_id,
                access_key_secret=access_key_secret,
            )
        )

    def _request_access_token(self):
        get_access_token_request = GetAccessTokenRequest(
            app_key=self.access_key_id,
            app_secret=self.access_key_secret,
        )
        try:
            ret = self._oauth_client.get_access_token(get_access_token_request)
            return ret.body.to_map()['accessToken']
        except Exception as err:
            code, msg = getattr(err, 'code', None), getattr(err, 'message', None)
            if code:
                raise Exception(f'{code}: {msg}')
            raise err

    @property
    def access_token(self):
        key = f"{self.access_key_id}:{self.access_key_secret}"
        try:
            return access_token_cache[key]
        except KeyError:
            return self._request_access_token()
