#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
# 第三方 SMTP 服务
mail_host="smtp.qq.com"  #设置服务器
mail_user="your qq email"    #用户名
mail_pass="your key"   #SMTP授权码，搜索：qq邮箱smtp设置
sender = 'your qq email'
receivers = ['your qq email']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
def send_mail(message):
        message = MIMEText(message, 'plain', 'utf-8')
        message['From'] = Header("班车预约信息", 'utf-8')
        message['To'] =  Header("测试", 'utf-8')
        subject = '冠寓至大瓦窑预约信息'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtp = SMTP_SSL(mail_host)
            smtp.ehlo(mail_host)
            smtp.login(mail_user,mail_pass)
            smtp.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")