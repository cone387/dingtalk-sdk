from cone_dingtalk.client.api.base import DingTalkV1API


class ChatAPI(DingTalkV1API):

    def create(self,
               title,
               template_id,
               owner_user_id,
               user_ids=None,
               subadmin_ids=None,
               uuid=None,
               icon=None,
               mention_all_authority=0,
               show_history_type=0,
               searchable=0,
               validation_type=0,
               chat_banned_type=0,
               management_type=0,
               only_admin_can_ding=0,
               all_members_can_create_mcs_conf=1,
               all_members_can_create_calendar=0,
               group_email_disabled=0,
               only_admin_can_set_msg_top=0,
               add_friend_forbidden=0,
               group_live_switch=1,
               members_to_admin_chat=0,
               ):
        """
        创建会话
        :param title: 群名称。长度限制为1~20个字符
        :param template_id: 群模板ID，登录开发者后台 > 开放能力 > 场景群 > 群模板查看id。
        :param owner_user_id: 群主的userid。
        :param user_ids: 群成员userid列表。最多传999个。以逗号分隔
        :param subadmin_ids: 群管理员userid列表。以逗号分隔
        :param uuid: 建群去重的业务ID，由接口调用方指定。(建议长度在64字符以内。)
        :param icon: 群头像，格式为mediaId。需要调用上传媒体文件接口上传群头像，获取mediaId。
        :param mention_all_authority: @all 权限，0-默认，所有人，1-仅群主可@all
        :param show_history_type: 新成员是否可查看聊天历史消息：0（默认）：不可以查看历史记录 1：可以查看历史记录
        :param validation_type: 入群验证，0：不入群验证（默认） 1：入群验证
        :param searchable: 群可搜索，0-默认，不可搜索，1-可搜索
        :param chat_banned_type: 群禁言，0-默认，不禁言，1-全员禁言
        :param management_type: 管理类型，0-默认，所有人可管理，1-仅群主可管理
        :param only_admin_can_ding: 群内发DING权限：0（默认）：所有人可发DING 1：仅群主和管理员可发DING
        :param all_members_can_create_mcs_conf: 群会议权限：0：仅群主和管理员可发起视频和语音会议 1（默认）：所有人可发起视频和语音会议
        :param all_members_can_create_calendar: 群日历权限：0：群日历设置项，群内非好友/同事的成员是否可相互发起钉钉日程：0（默认）：
        非好友/同事的成员不可发起钉钉日程1：非好友/同事的成员可以发起钉钉日程
        :param group_email_disabled: 群邮件开关，0-默认，群内成员可以对本群发送群邮件，1-群内成员不可对本群发送群邮件
        :param only_admin_can_set_msg_top: 置顶群消息权限：0-默认，所有人可置顶群消息，1-仅群主和管理员可置顶群消息
        :param add_friend_forbidden: 群成员私聊权限：0-默认，所有人可私聊，1-普通群成员之间不能够加好友、单聊，且部分功能使用受限（管理员与非管理员之间不受影响）
        :param group_live_switch: 群直播权限：0-仅群主与管理员可发起直播，1-默认，所有人可发起直播
        :param members_to_admin_chat: 是否禁止非管理员向管理员发起单聊：0-（默认）非管理员可以向管理员发起单聊，1-禁止非管理员向管理员发起单聊
        :return: 群会话的id
        返回结果示例：
        {
            "result":{
                    "open_conversation_id":"cidt*****Xa4K10w==",
                    "chat_id":"chat6d99a92e8x***"
            },
            "errcode":0,
            "success":true,
            "errmsg":"ok",
            "request_id": "ed669urokuvq"
        }
        """
        return self._request(
            '/topapi/im/chat/scenegroup/create',
            method='POST',
            json={
                'title': title,
                'template_id': template_id,
                'owner_user_id': owner_user_id,
                'user_ids': user_ids,
                'subadmin_ids': subadmin_ids,
                'uuid': uuid,
                'icon': icon,
                'mention_all_authority': mention_all_authority,
                'show_history_type': show_history_type,
                'validation_type': validation_type,
                'searchable': searchable,
                'chat_banned_type': chat_banned_type,
                'management_type': management_type,
                'only_admin_can_ding': only_admin_can_ding,
                'all_members_can_create_mcs_conf': all_members_can_create_mcs_conf,
                'all_members_can_create_calendar': all_members_can_create_calendar,
                'group_email_disabled': group_email_disabled,
                'only_admin_can_set_msg_top': only_admin_can_set_msg_top,
                'add_friend_forbidden': add_friend_forbidden,
                'group_live_switch': group_live_switch,
                'members_to_admin_chat': members_to_admin_chat
            }
        )

    def send(self, chatid, msg_body):
        """
        发送群消息

        :param chatid: 群会话的id
        :param msg_body: BodyBase 消息体
        :return: 加密的消息id
        """
        if isinstance(msg_body, BodyBase):
            msg_body = msg_body.get_dict()
        msg_body['chatid'] = chatid
        return self._post(
            '/chat/send',
            msg_body,
            result_processor=lambda x: x['messageId']
        )

    def get_read_list(self, message_id, cursor=0, size=100):
        """
        查询群消息已读人员列表

        :param message_id: 发送群消息接口返回的加密消息id
        :param cursor: 分页查询的游标，第一次传0，后续传返回结果中的next_cursor。返回结果中没有next_cursor时，表示没有后续的数据了
        :param size: 分页查询的大小，最大可以传100
        :return:
        """
        return self._get(
            '/chat/getReadList',
            {"messageId": message_id, "cursor": cursor, "size": size}
        )


if __name__ == '__main__':
    client = ChatAPI()
    res = client.create(
        title='测试群',
        template_id='eea10ee3-733b-43c1-b4f1-29fe04fd1e38',
        owner_user_id='01465416484027168950'
    )
    print(res)
