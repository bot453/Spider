# encoding: utf-8
"""
@software: PyCharm
@time: 2020/4/3 11:28
"""
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import schedule
import time


# 邮件账号
account = ""
# 收件SMTP授权码
passwd = ""
# 收件人邮箱
receiver = ""

def recipe_spider():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    res = requests.get("http://www.xiachufang.com/explore/",headers=headers)
    soup = BeautifulSoup(res.text,"html.parser")
    list_foods = soup.find_all("div",class_="info pure-u")

    list_all = ""
    num = 0
    for food in list_foods:
        num +=1
        #菜名
        tag_a = food.find("a")
        name = tag_a.text[17:-13]
        #佐料
        tag_p = food.find("p",class_="ing ellipsis")
        ingredients = tag_p.text
        #URL
        URL = "http://www.xiachufang.com"+tag_a["href"]
        #print(name,ingredients,URL)
        food_info = '''
        序号：%s
        菜名：%s
        链接：%s
        佐料：%s
        '''%(num,name,URL,ingredients)
        list_all =list_all+food_info
    return(list_all)

def send_email( list_all):
    #qq邮箱服务器地址
    hostmail = "smtp.qq.com"
    #调用SMTP对象的属性和方法
    qqmail = smtplib.SMTP()
    #连接服务器，【地址】【端口】
    qqmail.connect(hostmail,25)

    #登录邮箱
    qqmail.login(account,passwd)

    #邮箱内容，为字符串格式
    content = '本周的热门菜谱如下'+list_all

    #实例化MIMEText邮件对象【邮件正文】【文本格式】【编码】
    message = MIMEText(content,"plain","utf-8")

    #邮件主题
    subject = "今日美食"

    #实例化了一个Header邮件头对象【邮件主题】【编码】，赋值给变量message['Subject']
    message["Subject"] = Header(subject, "utf-8")

    try:
        qqmail.sendmail(account, receiver, message.as_string())
        print("邮件发送成功")
    except:
        print("邮件发送失败")
    qqmail.quit()
    # 以上为【发送邮箱】and【退出邮箱】


def job():
    print("开始一次任务")
    list_all = recipe_spider()
    send_email(list_all)
    print("任务完成")

#每天12：15执行一次任务
schedule.every().day.at("12:15").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)

