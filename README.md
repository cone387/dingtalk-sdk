# dingtalk-sdk
dingtalk sdk for me


## 背景

想要通过钉钉发送消息，和接受消息。

要想通过机器人发送消息有两种选择
1. 使用自定机器人，这种只需要有app-key, app-secret就行了， 但是这种机器人不能接受消息，所以满足不了需求
2. 新建app，在app中新建机器人
    使用这种机器人发送消息需要使用dinktalk API了。

## 使用APP中的机器人

1. 可以单独发送消息给指定用户，也可以发送群聊消息并且@指定用户

2. 可以给机器人发送单聊消息，也可以发送群聊消息并且@执行机器人


### 发送群聊消息，需要使用到几个接口

1. token接口，获取token
2. conversationId, 必须通过接口创建的群聊才能拿到有用的conversationId
3. 发送消息

### 发送单聊消息，需要使用到几个接口

1. token接口，获取token
2. user_id, 通过手机号获取到user_id
3. 发送消息