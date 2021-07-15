#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import binascii
import asyncio
import hashlib
import ujson
# import aiosmtplib
import uuid
import re
#from gatco.exceptions import ServerError
from email.mime.text import MIMEText
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from gatco.response import json
from application.database import db
from application.extensions import auth
from application.models.model import *
from application.server import app
from datetime import datetime
from gatco.response import json, text, html
# from gatco_restapi.helpers import to_dict
from application.common.constants import ERROR_CODE, ERROR_MSG

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'


def remove_accents(input_str):
    s = ""
    strr = str(input_str)
    for c in strr:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s


def now_timestamp():
    return round(time.time() * 1000)


def get_datetime_timezone(timestamp, timezone='Asia/Ho_Chi_Minh'):
    return datetime.fromtimestamp(timestamp/1000, tz=pytz.timezone(timezone))


def get_year_later(number_of_year):
    udate_now = datetime.utcnow()
    current_year = udate_now.year
    date = udate_now.replace(year=current_year + number_of_year)
    return date


def generate_key(type="number", length=16):
    s = ''
    for i in range(length):
        s += str(random.randint(0, 9))

    if type == "number":
        return int(s)
    else:
        return s


def generate_group_id():
    code = ''.join(random.choice(string.ascii_lowercase + string.digits)
                   for _ in range(16))
    return code


# async def send_mail(subject, recipient, body):
#     # Thanks: https://github.com/cole/aiosmtplib/issues/1
#     host = app.config.get('MAIL_SERVER_HOST')
#     port = app.config.get('MAIL_SERVER_PORT')
#     user = app.config.get('MAIL_SERVER_USER')
#     password = app.config.get('MAIL_SERVER_PASSWORD')

#     loop = asyncio.get_event_loop()

#     #server = aiosmtplib.SMTP(host, port, loop=loop, use_tls=False, use_ssl=True)
#     server = aiosmtplib.SMTP(hostname=host, port=port,
#                              loop=loop, use_tls=False)
#     await server.connect()

#     await server.starttls()
#     await server.login(user, password)

#     async def send_a_message():
#         message = MIMEText(body)
#         message['From'] = app.config.get('MAIL_SERVER_USER')
#         message['To'] = recipient
#         message['Subject'] = subject
#         await server.send_message(message)

#     await send_a_message()


def get_uuid():
    return str(uuid.uuid4())


def generate_secret_app(number_digits):
    code = ''.join(random.choice(string.ascii_lowercase + string.digits)
                   for _ in range(number_digits))
    return code


def generate_salt():
    code = ''.join(random.choice(string.ascii_lowercase + string.digits)
                   for _ in range(32))
    return code


async def generate_token(data, time_expire):
    token = binascii.hexlify(uuid.uuid4().bytes).decode()
    p = redisdb.pipeline()
    p.set("sessions:" + token, data)
    if (time_expire > 0):
        p.expire("sessions:" + token, time_expire)
    p.execute()
    return token


def convert_phone_number(phone, output_type="0"):
    tmp_phone = str(phone)
    if output_type == "0" or output_type == 0:
        if tmp_phone[:1] == "0":
            pass
        elif tmp_phone[:2] == "84":
            tmp_phone = tmp_phone.replace("84", "0")
        elif tmp_phone[:3] == "+84":
            tmp_phone = tmp_phone.replace("+84", "0")
        else:
            return None

        return tmp_phone

    elif output_type == "84" or output_type == 84:
        if tmp_phone[:2] == "84":
            pass
        elif tmp_phone[:1] == "0":
            tmp_phone = tmp_phone.replace("0", "84")
        elif tmp_phone[:3] == "+84":
            tmp_phone = tmp_phone.replace("+84", "84")
        else:
            return None

        return tmp_phone

    elif output_type == "+84":
        if tmp_phone[:3] == "+84":
            pass
        if tmp_phone[:1] == "0":
            tmp_phone = tmp_phone.replace("0", "+84")
        elif tmp_phone[:2] == "84":
            tmp_phone = tmp_phone.replace("84", "+84")
        else:
            return None
        return tmp_phone
    else:
        return None


def convert_datetime_format(input_datetime, format="%Y-%m-%d", inputFormat="%d/%m/%Y"):

    if str(input_datetime).find("T") >= 0:
        return str(input_datetime)[:str(input_datetime).index("T")]
    else:
        inDate = datetime.strptime(input_datetime, inputFormat)
#         print (inDate.strftime(format))
        return inDate.strftime(format)


def get_day_of_week(value=datetime.now()):
    return datetime.strptime(value).weekday()


def hash_value(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()


def check_content_json(request):
    ret = False
    try:
        content_type = request.headers.get('Content-Type', "")
        ret = content_type.startswith('application/json')
    except:
        ret = False
    return ret


def valid_phone_number(phone_number):
    if phone_number is None:
        return False
    if phone_number.isdigit() and len(phone_number) >= 8 and len(phone_number) <= 12 and phone_number.startswith("0"):
        return True
    return False


async def get_current_user(request, **kw):
    return auth.current_user(request)


def auth_func(request=None, **kw):
    current_user = auth.current_user(request)
    if current_user is None:
        return json({"error_code": "SESSION_EXPIRED", "error_message": "Hết phiên làm việc, vui lòng đăng nhập lại"}, status=520)


def deny_func(request=None, **kw):
    return json({"error_code": "PERMISSION_DENY", "error_message": "Không có quyền thực hiện hành động này"}, status=520)


async def hasRole(request, role):
    currentUser = await get_current_user(request)
    if currentUser is not None:
        return currentUser.has_role(role)
    else:
        return False


async def verify_admin(request=None, **kw):
    currentUser = await get_current_user(request)
    # if currentUser is not None:
    #     if not currentUser.has_role('Admin'):
    #         return json({"error_code": "PERMISSION_DENY", "error_message": "permission denied"}, status=520)
    # else:
    #     return json({"error_code": "SESSION_EXPIRED", "error_message": "not found session"}, status=520)


def role_pregetmany(search_params=None, **kw):
    search_params["filters"] = {"$and": [search_params["filters"], {"id": {"$neq": 1}}]} if ("filters" in search_params)   \
        else {"id": {"$neq": 1}}


async def user_pregetmany(search_params, Model, **kw):
    request = kw.get("request", None)
    currentUser = await get_current_user(request)
    if currentUser is not None:
        if currentUser.has_role('Admin'):
            print("user_pregetmany=============== is Admin")
        else:
            search_params["filters"] = ("filters" in search_params) and {"$and": [search_params["filters"], {"id": {"$eq": currentUser.id}}]} \
                or {"id": {"$eq": currentUser.id}}


async def verify_access(request, **kw):
    try:
        valid = False
        if auth_func(request) is None:
            valid = True

        app_key = request.headers.get('X-UPACCOUNTS-APPKEY', None)
        app_secret = request.headers.get('X-UPACCOUNTS-SECRETKEY', None)

        if valid == True:
            print("passed authen")
            pass
        else:
            return json(ERROR_MSG['TOKEN_ERROR'], status=520)
    except:
        return json(ERROR_MSG['TOKEN_ERROR'], status=520)


def convert_no_accent_vietnamese_regex(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s
