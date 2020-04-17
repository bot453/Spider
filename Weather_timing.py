#数据爬取
import requests
from bs4 import BeautifulSoup
# 邮件连接发送
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# 定时
import schedule
import time

# 发送人邮件账号
account = ""
# SMTP授权码
passwd = ""
# 收件人邮箱账号
receiver = ""


def weather_spider():
    url = "http://www.weather.com.cn/weather/101020100.shtml"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}

    res = requests.get(url, headers=headers)
    # 乱码，更该编码格式
    res.encoding = "utf-8"
    # bs模块解析数据
    soup = BeautifulSoup(res.text, "html.parser")
    # 数据提取
    tem1 = soup.find(class_="tem")
    weather1 = soup.find(class_="wea")
    tem = tem1.text
    weather = weather1.text
    return tem, weather


def send_email(tem, weather):
    # qq邮箱SMMP服务器地址
    mailhost = "smtp.qq.com"
    # 实例化一个smtplib模块里的SMTP类的对象，这样就可以SMTP对象的方法和属性了
    qqmail = smtplib.SMTP()
    # 连接服务器 【第一个参数是服务器地址，第二个参数是SMTP端口号】
    qqmail.connect(mailhost, 25)
    # 以上为【连接邮箱服务器】

    qqmail.login(account, passwd)
    # 以上为【登录邮箱】

    # 邮件正文，为字符串格式
    content = tem+weather
    # 实例化一个MIMEText邮件对象，三个参数【邮件正文，文本格式，编码】
    message = MIMEText(content, "plain", "utf-8")
    # 邮件主题，为字符串格式
    subject = "今日天气预报"
    # 等号的右边是实例化了一个Header邮件头对象，该对象需要写入两个参数，分别是邮件主题和编码，然后赋值给等号左边的变量message['Subject']
    message["Subject"] = Header(subject, "utf-8")
    # 以上为【邮件主题】and【邮件正文】

    try:
        qqmail.sendmail(account, receiver, message.as_string())
        print("邮件发送成功")
    except:
        print("邮件发送失败")
    qqmail.quit()
    # 以上为【发送邮箱】and【退出邮箱】


def job():
    print("开始一次任务")
    tem,weather = weather_spider()
    send_email(tem,weather)
    print("任务完成")


schedule.every().day.at("23:12").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
