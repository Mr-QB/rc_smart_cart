import os
from zlapi import ZaloAPI
from zlapi.models import *
import json

imei = os.getenv("ZALO_IMEI")
cookies = json.loads(os.getenv("ZALO_COOKIES"))
print(type(cookies))


bot = ZaloAPI("+84378640335", "Matkhau123@", imei=imei, cookies=cookies)
bot.sendMessage(
    message=Message("Hello from ZaloAPI"),
    thread_id=bot.fetchPhoneNumber("0325372909").uid,
    thread_type=ThreadType.USER,
)
