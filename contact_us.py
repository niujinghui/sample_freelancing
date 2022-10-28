#!/usr/bin/env python3

from my_utility_scripts.logging_tools import log_request, my_logger
my_logger.info(f"开始运行module:{__name__}, 其文件位置在: {__file__}")

import cherrypy
from my_utility_scripts import changeDir
from my_utility_scripts.ast_analyzer import extract_ClassDefs
from my_mako_adaptor import mako_lookup
from my_cherrypy_adaptor import cherrypy_conf
import server_base

import email, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


# PORT = 587
PORT = 994
# SMTP_SERVER = "smtp.office365.com"
SMTP_SERVER = "smtp.ym.163.com"
SENDER_EMAIL = "***@mdrtfinancial.com"
# PASSWORD = "!1qazZ@2wsxX"
receiver_email = "***@gmail.com"


class UnitServer(server_base.BasicServer):

    mako_template_for_server_index = "contact_us.html"
    SCRIPT_NAME = "contact_us"

    @cherrypy.expose
    def message_board(self, sender_name, sender_email, message_content):
        cherrypy.log(f"""<message_board> 被调用！收到的参数是：
                        sender_name: {sender_name}, sender_email: {sender_email}\n
                        message_content: {message_content}""")

        context = ssl.create_default_context()
        email_text = f"""
            留言人名字：{sender_name}
            留言人电子邮箱地址：{sender_email}
            留言内容：{message_content}
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = "留言板有新的留言！"
        message["From"] = SENDER_EMAIL
        message["To"] = receiver_email
        part1 = MIMEText(email_text, "html")
        message.attach(part1)
        # with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        with smtplib.SMTP_SSL(SMTP_SERVER, 994) as server:
            # server.ehlo()
            # server.starttls(context=context)
            # server.ehlo()
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        return




'''
import csv
import datetime
import time

SCHEDULED_SEND_TIME = None
# SCHEDULED_SEND_TIME = datetime.datetime(2019,12,8,17,35,0) # set your sending time in UTC


context = ssl.create_default_context()

def generate_content(Username):
    html_content = """
    <html>
        <body>
        <p>各位亲爱的会员 {Username}：</p>
<p>感谢您成为38FULE的会员，因为会员购买产品已经有一段时间了，我们希望做一个调查，有利于我们了解您或者您��朋友、客人使用产品的反馈，请您填好后，同样回复到这个邮箱，我们会给积极回复的会员予以奖励新产品的试用套装。</p>
<p>谢谢您的配合!</p>
<p>&nbsp;</p>
<p>Dear member  {Username}，</p>
<p>Thank you for becoming a member of 38FULE. We would like to receive your feedback regarding our products since you already bought them for a while. Please fill the survey form and give you or your clients feedback to us. We will reward you small gifts with our new products which will arrive soon.</p>
<p>Thank you for your cooperation!</p>
<p>Kelly Li</p>
<p>Marketing Director</p>
<p>Jan 22,2020</p>
        </body>
    </html>
    """.format(Username=Username)
    return html_content
    
if SCHEDULED_SEND_TIME:
    time.sleep(SCHEDULED_SEND_TIME.timestamp() - time.time())
print("Time is up, now start sending emails...")

with open("MemberEmailNotification.csv") as file:
    reader = csv.reader(file)
    for username, receiver_email, password in reader:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Username & Password"
        message["From"] = SENDER_EMAIL
        message["To"] = receiver_email
        email_body = generate_content(Username=username, Password=password)
        part1 = MIMEText(email_body, "html")
        message.attach(part1)
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())

with open("38FULE 会员产品使用调查表.docx", "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    attachment_part = MIMEBase("application", "octet-stream")
    attachment_part.set_payload(attachment.read())
email.encoders.encode_base64(attachment_part)
attachment_part.add_header(
    "Content-Disposition",
    "attachment",
    filename="38FULE 会员产品使用调查表.docx"
)
            
with open("会员电子邮件地址.csv") as file:
# with open("MemberEmailNotification.csv") as file:
    reader = csv.reader(file)
    for username, receiver_email in reader:
        message = MIMEMultipart("mixed")
        message["Subject"] = "38FULE 会员产品使用调查表---38FULE members using products Survey"
        message["From"] = SENDER_EMAIL
        message["To"] = receiver_email
        email_body = generate_content(Username=username)
        part1 = MIMEText(email_body, "html")
        message.attach(part1)
        message.attach(attachment_part)
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
'''