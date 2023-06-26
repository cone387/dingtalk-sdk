from cone_dingtalk.client.api.base import DingTalkV2API
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.robot_1_0 import models as robot_models
from alibabacloud_dingtalk.robot_1_0.client import Client
from alibabacloud_tea_util import models as util_models
import json


class DingTalkMessage:
    name = "钉钉消息类型"
    key = None

    @property
    def body(self):
        if self.__class__ == DingTalkMessage:
            raise Exception("DingTalkMessage can't be used directly.")
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                result[key] = value
        return json.dumps(result, ensure_ascii=False)


class SampleText(DingTalkMessage):
    name = "文本类型"
    key = "sampleText"

    def __init__(self, content):
        self.content = content


class SampleMarkdown(DingTalkMessage):
    name = "Markdown类型"
    key = "sampleMarkdown"

    def __init__(self, title, text):
        self.title = title
        self.text = text


class SampleImageMsg(DingTalkMessage):
    name = "图片类型"
    key = "sampleImageMsg"

    def __init__(self, photo_url):
        self.photo_url = photo_url


class SampleLink(DingTalkMessage):
    name = "链接类型"
    key = "sampleLink"

    def __init__(self, title, text, message_url, pic_url):
        self.title = title
        self.text = text
        self.message_url = message_url
        self.pic_url = pic_url


class ActionCard(DingTalkMessage):
    name = "ActionCard类型"

    def __init__(self, title, text):
        self.title = title
        self.text = text


class SampleActionCard(ActionCard):
    """
        卡片消息：竖向一个按钮。
    """
    key = "sampleActionCard"

    def __init__(self, title, text, single_title, single_url):
        super().__init__(title, text)
        self.single_title = single_title
        self.single_url = single_url


class SampleActionCard2(ActionCard):
    """
    卡片消息：竖向二个按钮。
    """
    key = "sampleActionCard2"

    def __init__(self, title, text, action_title1, action_url1, action_title2, action_url2):
        super().__init__(title, text)
        self.action_title1 = action_title1
        self.action_url1 = action_url1
        self.action_title2 = action_title2
        self.action_url2 = action_url2


class SampleActionCard3(SampleActionCard2):
    """
    卡片消息：竖向三个按钮。
    """
    key = "sampleActionCard3"

    def __init__(self, title, text,
                 action_title1, action_url1,
                 action_title2, action_url2,
                 action_title3, action_url3):
        super(SampleActionCard3, self).__init__(title, text, action_title1, action_url1, action_title2, action_url2)
        self.action_title3 = action_title3
        self.action_url3 = action_url3


class SampleActionCard4(SampleActionCard3):
    """
        卡片消息：竖向四个按钮。
    """
    key = "sampleActionCard4"

    def __init__(self, title, text,
                 action_title1, action_url1,
                 action_title2, action_url2,
                 action_title3, action_url3,
                 action_title4, action_url4):
        super(SampleActionCard4, self).__init__(title, text, action_title1, action_url1, action_title2,
                                                action_url2, action_title3, action_url3)
        self.action_title4 = action_title4
        self.action_url4 = action_url4


class SampleActionCard5(SampleActionCard4):
    """
    卡片消息：竖向五个按钮。
    """
    key = "sampleActionCard5"

    def __init__(self, title, text,
                 action_title1, action_url1,
                 action_title2, action_url2,
                 action_title3, action_url3,
                 action_title4, action_url4,
                 action_title5, action_url5):
        super(SampleActionCard5, self).__init__(title, text, action_title1, action_url1, action_title2,
                                                action_url2, action_title3, action_url3,
                                                action_title4, action_url4)
        self.action_title5 = action_title5
        self.action_url5 = action_url5


class SampleActionCard6(ActionCard):
    """
    卡片消息：横向二个按钮。
    """
    key = "sampleActionCard6"

    def __init__(self, title, text,
                 button_title1, button_url1,
                 buttonTitle2, button_url2):
        super(ActionCard, self).__init__(title, text)
        self.button_title1 = button_title1
        self.button_url1 = button_url1
        self.buttonTitle2 = buttonTitle2
        self.button_url2 = button_url2


class SampleAudio(DingTalkMessage):
    """
    语音消息：
        mediaId：通过上传媒体文件接口，获取media_id参数值。
            说明
                支持ogg、amr格式。
        duration：语音消息时长，单位毫秒。
    """
    name = "语音类型"
    key = "sampleAudio"

    def __init__(self, duration, media_id):
        self.duration = duration
        self.media_id = media_id


class SampleFile(DingTalkMessage):
    """
    文件消息：
        mediaId：通过上传媒体文件接口，获取media_id参数值。
        fileName：文件名称。
        fileType：文件类型。
            说明
                文件类型，支持xlsx、pdf、zip、rar、doc、docx格式。
    """
    name = "文件类型"
    key = "sampleFile"

    def __init__(self, media_id, file_name, file_type):
        self.media_id = media_id
        self.file_name = file_name
        self.file_type = file_type


class SampleVideo(DingTalkMessage):
    """
    视频消息：
        duration：语音消息时长，单位秒。
        videoMediaId：通过上传媒体文件接口，获取media_id参数值。
        videoType：视频类型，支持mp4格式。
        picMediaId：视频封面图，通过上传媒体文件接口，获取media_id参数值。
        height：视频展示高度，单位px。
    """
    name = "视频类型"
    key = "sampleVideo"

    def __init__(self, duration, video_media_id, video_type, pic_media_id):
        self.video_media_id = video_media_id
        self.video_type = video_type
        self.duration = duration
        self.pic_media_id = pic_media_id


class RobotAPI(DingTalkV2API):

    def __init__(self, access_key_id=None, access_key_secret=None, conversion_id=None, robot_code=None, user_id=None):
        super().__init__(access_key_id, access_key_secret)
        self.client = Client(config=open_api_models.Config(
            protocol='https',
            region_id='central',
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
        ))
        self.conversion_id = conversion_id
        self.robot_code = robot_code
        self.user_id = user_id

    def send_to_conversation(self, message: DingTalkMessage, robot_code, conversation_id: str):
        org_group_send_headers = robot_models.OrgGroupSendHeaders()
        org_group_send_headers.x_acs_dingtalk_access_token = self.access_token
        org_group_send_request = robot_models.OrgGroupSendRequest(
            msg_param=message.body,
            msg_key=message.key,
            open_conversation_id=conversation_id,
            robot_code=robot_code,
            cool_app_code=None
        )
        try:
            ret = self.client.org_group_send_with_options(org_group_send_request, org_group_send_headers,
                                                          util_models.RuntimeOptions())
        except Exception as err:
            raise err
        return ret

    def send_to_user(self, message: DingTalkMessage, robot_code: str, user_id: str):
        batch_send_otoheaders = robot_models.BatchSendOTOHeaders()
        batch_send_otoheaders.x_acs_dingtalk_access_token = self.access_token
        batch_send_otorequest = robot_models.BatchSendOTORequest(
            robot_code=robot_code,
            user_ids=[user_id],
            msg_key=message.key,
            msg_param=message.body,
        )
        try:
            ret = self.client.batch_send_otowith_options(batch_send_otorequest, batch_send_otoheaders,
                                                         util_models.RuntimeOptions())
            print(ret)
        except Exception as err:
            raise err
        return ret

    def send_msg(self, message: DingTalkMessage, robot_code=None, conversation_id=None, user_id=None):
        robot_code = robot_code or self.robot_code
        user_id = user_id or self.user_id
        conversation_id = conversation_id or self.conversion_id
        assert robot_code, "robot_code must be set."
        assert conversation_id or user_id, "conversation_id or user_id must be set one."
        assert not (conversation_id and user_id), "conversation_id and user_id can only set one."
        if user_id:
            return self.send_to_user(message, robot_code, user_id,)
        if conversation_id:
            return self.send_to_conversation(message, robot_code, conversation_id)

    def __call__(self, robot_code=None, user_id=None, conversation_id=None):
        self.robot_code = robot_code
        self.user_id = user_id
        self.conversion_id = conversation_id
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__ == '__main__':
    """
        open_conversation_id='cidSixfT7UGbVLVJkgIzleF20=',
        robot_code='dinghkwyfwu272bbhve4',
        user_id: 01465416484027168950
    """
    robot = RobotAPI(robot_code='dinghkwyfwu272bbhve4', user_id='01465416484027168950')
    robot.send_msg(
        message=SampleMarkdown(title="测试", text="我是不上"),
    )

    with robot as r:
        r.send_msg(message=SampleMarkdown(title="测试", text="我是不上1"))

