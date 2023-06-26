from cone_dingtalk.client.api.base import DingTalkV1API


class UserAPI(DingTalkV1API):

    def get_by_mobile(self, mobile):
        """
        根据手机号获取用户userid
        :param mobile: 手机号
        :return: userid
        """
        return self._request(
            'topapi/v2/user/getbymobile',
            json={'mobile': mobile}
        )['result']['userid']


if __name__ == '__main__':
    client = UserAPI()
    res = client.get_by_mobile(
        mobile='18895379450'
    )
    print(res)
