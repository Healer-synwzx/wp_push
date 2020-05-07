from robot import Robot
from config import QR_SCENE, APP_ID, APP_SECRET

from redis_util import redis_client


robot = Robot(token='tokenhere')
robot.config["APP_ID"] = APP_ID
robot.config["APP_SECRET"] = APP_SECRET


@robot.scan
def scan(message):
    ticket = message.Ticket
    unique_id = redis_client.get_ticket_unique(ticket)
    info = robot.client.get_user_info(message.FromUserName)
    redis_client.set_scaned_flag(unique_id, info["openid"])
    return "扫码成功，请点击电脑页面上的「检查结果并确认绑定按钮」"


@robot.subscribe
def subscribe(message):
    if message.EventKey == f'qrscene_{QR_SCENE}':
        return scan(message)


@robot.templatesendjobfinish_event
def push_finish(message):
    print(message.__dict__)
    return ''
