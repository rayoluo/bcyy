# -*- coding: utf-8 -*-
import requests
import json
import datetime
import time
import send_email

# 手动填写账号和密码
idserial = "your id"
password = "your password"

print("===============log info===============")
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
session = requests.session()
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
            # week = 5 # 测试用

            if week == 0 or week == 6:
                print("别卷了卷王！要加班自己手动预约吧！！！")
                send_email.send_mail("别卷了卷王！要加班自己手动预约吧！！！")
                exit(-1)
            else: # 开始班车预约
                # 正式代码
                data = {
                    "selldate":selldatemax,
                    "enddate":selldatemax,
                    "method":"/mobile/home/queryHomeGoods"
                }

                response = session.post(url=url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    print("获取可预约班车最大日期的班车信息成功!")
                    # print(response.text)
                    # 获取从益园到张仪村晚上20:30的班车信息
                    info = json.loads(response.text).get("data")[11]
                    # 构建班车预约请求负载，只多了一个method:/mobile/pay/toPaySelf键值对
                    info["method"] = "/mobile/pay/toPaySelf"
                    response = session.post(url=url, headers=headers, data=json.dumps(info))
                    if response.status_code == 200:
                        code = json.loads(response.text).get("code")
                        msg = json.loads(response.text).get("msg")
                        if code == 200 and msg == "success":
                            print("晚上八点半的班车预约成功！日期：")
                            print(selldatemax)
                            send_message = u"晚上八点半的班车预约成功！\n日期：" + selldatemax
                            send_email.send_mail(send_message)

                        else:
                            # print("班车预约失败!", "code:", code, "error message:", msg)
                            print("班车预约失败！错误信息：")
                            print(msg)
                            send_message = u"班车预约失败！\n预约日期:" + selldatemax +  u"\n错误信息: %s" % msg
                            send_email.send_mail(send_message)
                            exit(-1)
                else:
                    print("获取可预约班车最大日期的班车信息失败!")
                    exit(-1)

        else:
            print("获取班车预约日期区间失败！")
            exit(-1)

        # 程序的逻辑是始终帮你预约可预约班车最大日期的8:30的班车，需要注意如果是周六就预约5:30的
else:
    print('dataForward接口访问失败！')
    exit(-1)