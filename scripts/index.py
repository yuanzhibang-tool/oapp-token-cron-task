import json
from task import run

# 此为阿里云函数计算入口,配置触发消息如下,触发实际为1分钟执行一次,阿里云函数计算安装依赖请参考
# https://help.aliyun.com/document_detail/422183.html
# update_server_access_token: {"action":"update_server_access_token" }
# update_js_ticket: {"action":"update_js_ticket" }


def handler(event, context):
    event_dict = json.loads(event)
    payload = json.loads(event_dict['payload'])
    action = payload['action']
    run(action)
