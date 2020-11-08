# -*- coding: utf-8 -*-
import requests
import json
import datetime
import time
import argparse

# ********************** example ***********************
# python cliBcyy.py --id 12345 --password 12345 --weeks 12345
# 
parser =argparse.ArgumentParser()

parser.add_argument('--id', type=str)
parser.add_argument('--password', type=str, default='111111')
parser.add_argument('--weeks', type=str, default='12345')

args = parser.parse_args()

idserial = args.id
password = args.password
weeks = args.weeks

session = requests.session()


url = 'http://159.226.95.123/dataForward'

def login_in(idserial, password='111111'):
    url_welcome = 'http://bcyy.iie.ac.cn/'
    r = session.get(url=url_welcome)
    if r.status_code == 200:
        print('初始页面请求成功！')
    else:
        print('初始页面请求失败！')
    # 首先发送GET请求，获取token值
    url = 'http://159.226.95.123/dataForward'
    data = {
        "idserial":idserial,
        "password":password,
        "method":"/mobile/login/userLoginCheck",
    }
    headers = {
        "user-agent":"Mozilla/5.0",
        "Content-Type":"application/json",
        "X-Token":None,
    }
    # 需要使用json.dumps()将data转化为json格式，否则会报json解析错误
    response = session.post(url=url, headers=headers, data=json.dumps(data))
    # print(response.content)
    return response
    
def book_now(token, selldate):
    data = {"selldate":selldate,
                "enddate":selldate,
                "method":"/mobile/home/queryHomeGoods"
        }
    headers = {
        "user-agent":"Mozilla/5.0",
        "Content-Type":"application/json",
        "X-Token":token,
    }
    response = session.post(url=url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("获取可预约班车最大日期的班车信息成功!")
            # print(response.text)
            # 获取从益园到张仪村晚上20:30的班车信息
        infos = json.loads(response.text).get("data")
        info = list(filter(lambda i: i['goodsdetail']==u'益园-张仪村' and i['selldate']==selldate and i['starttime']==u'20:30', infos))[0]
        # 构建班车预约请求负载，只多了一个method:/mobile/pay/toPaySelf键值对
        info["method"] = "/mobile/pay/toPaySelf"
        response = session.post(url=url, headers=headers, data=json.dumps(info))
        if response.status_code == 200:
            code = json.loads(response.text).get("code")
            msg = json.loads(response.text).get("msg")
            if code == 200 and msg == "success":
                print("晚上八点半的班车预约成功！日期：")
                print(selldate)
                # to do 添加邮箱通知模块
            else:
                # print("班车预约失败!", "code:", code, "error message:", msg)
                print("班车预约失败！错误信息：")
                print(msg)
                exit(-1)
    else:
        print("获取可预约班车最大日期的班车信息失败!")
        exit(-1)

def book(token):
    # 接下来通过dataForward接口并指定method为/mobile/home/queryGoodsAuxData可获取售票日期区间
    # 获取可预约的日期区间
    headers = {
                "user-agent": "Mozilla/5.0",
                "Content-Type": "application/json",
                "X-Token": token
            }
    data = {
                "method":"/mobile/home/queryGoodsAuxDate",
            }

    response = session.post(url=url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("获取班车预约日期区间成功！")
        selldatemin = json.loads(response.text).get("data").get("selldatemin")
        selldatemax = json.loads(response.text).get("data").get("selldatemax")
        print("可预约时间区间为:")
        print(selldatemin, "---", selldatemax)

                # 判断selldatamax是不是周末，是的话就不预约
                # strptime是将一个字符串转化成一个时间对象
        date_obj = datetime.datetime.strptime(selldatemax, "%Y-%m-%d")
                # strftime是把一个时间对象进行处理，转化为想要的格式
                # date_str = datetime.datetime.strftime(data_obj, "%Y %m %d)
        week = int(datetime.datetime.strftime(date_obj, "%w"))
                # week周一到周六代表1-6，周日为0
        
        if week == 0 or week == 6:
            print("别卷了卷王！要加班自己手动预约吧！！！")
            exit(-1)            
        else: # 开始班车预约
                    # 正式代码
            if str(week) in set(weeks):
                book_now(token, selldatemax)
    else:
        print("获取班车预约日期区间失败！")
        exit(-1)

if __name__ == '__main__':
    print("===============log info===============")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    
    response = login_in(idserial, password)

    if response.status_code == 200:
        print('dataForward接口访问成功，已post账号密码！')
        print(response.text)
        code = json.loads(response.text).get("code")
        if code == 500:
            print("账号密码错误，请检查！")
            exit(-1)
        else:
            print("账号密码正确，成功获取到token!")
            token = json.loads(response.text).get("data").get("token")
            print("token:"+token)
            book(token)
            # 程序的逻辑是始终帮你预约可预约班车最大日期的8:30的班车，需要注意如果是周六就预约5:30的
    else:
        print('dataForward接口访问失败！')
        exit(-1)
