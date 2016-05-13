from wechat_sdk import WechatBasic
from wechat_sdk import WechatConf

from config import local_settings

conf = WechatConf(
    token=local_settings.WECHAT_APP_TOKEN,
    appid=local_settings.WECHAT_APP_ID,
    appsecret=local_settings.WECHAT_APP_SECRET,
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key=local_settings.encoding_aes_key  # 如果传入此值则必须保证同时传入 token, appid
)

wechat = WechatBasic(conf=conf)
open_id = 'oV2n_jpd6LQxQW4Bwif4rhOXuNsQ'


class WechatService(object):
    @classmethod
    def check_signature(cls, signature, timestamp, nonce):
        return wechat.check_signature(signature, timestamp, nonce)

    @classmethod
    def parse_data(cls, data):
        return wechat.parse_data(data=data)

    @classmethod
    def get_message(cls):
        return wechat.get_message()

    @classmethod
    def response_text(cls, content):
        return wechat.response_text(content=content)

    @classmethod
    def get_user(cls):
        return wechat.message.source

    @classmethod
    def is_admin(cls):
        print(open_id)
        print(cls.get_user())
        return open_id == cls.get_user()
