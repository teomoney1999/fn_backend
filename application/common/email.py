'''
Created on Oct 14, 2018

@author: namdv
'''
import time
import asyncio
import aiosmtplib
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from email.mime.text import MIMEText
from gatco_restapi.helpers import to_dict
from application.server import app
from application.extensions import  jinja

from gatco.response import json, text
import ujson


async def send_mail(subject, recipient, body):

    #Thanks: https://github.com/cole/aiosmtplib/issues/1
    host = app.config.get('MAIL_SERVER_HOST')
    port = app.config.get('MAIL_SERVER_PORT')
    user = app.config.get('MAIL_SERVER_USER')
    password = app.config.get('MAIL_SERVER_PASSWORD')

    loop = asyncio.get_event_loop()

    #server = aiosmtplib.SMTP(host, port, loop=loop, use_tls=False, use_ssl=True)
    server = aiosmtplib.SMTP(hostname=host, port=port, loop=loop, use_tls=False)
    await server.connect()

    await server.starttls()
    await server.login(user, password)

    async def send_a_message():
        message = MIMEText(body)
        message['From'] = app.config.get('MAIL_SERVER_USER')
        #message['To'] = ','.join(new_obj.get('email_to'))
        message['To'] = recipient
        message['Subject'] = subject
        await server.send_message(message)

    await send_a_message()
# 
async def send_email_instructions(subject, recipient, mailbody):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_mail,args=[subject, recipient, mailbody])
    scheduler.start()
#     
    


