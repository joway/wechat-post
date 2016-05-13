from django.http.response import HttpResponse, HttpResponseBadRequest

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage

from utils.github import comment_on_github
from wechat.services import WechatService


@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not WechatService.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")

    # 解析本次请求的 XML 数据
    try:
        WechatService.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    if not WechatService.is_admin():
        WechatService.response_text(content='没有发送权限')
        return HttpResponseBadRequest('None Auth')

    # 获取解析好的微信请求信息
    message = WechatService.get_message()
    print("接受消息: "+message)
    response = ""
    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        comment_on_github(content)
        reply_text = '创建issues成功'
        response = WechatService.response_text(content=reply_text)

    return HttpResponse(response, content_type="application/xml")
