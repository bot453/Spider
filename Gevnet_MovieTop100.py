# encoding: utf-8
"""
@software: PyCharm
@time: 2020/4/5 16:44
"""

#从gevent库导入monkey模块
from gevent import monkey
#启动"猴子补丁"
monkey.patch_all()
import gevent,requests,csv
from bs4 import BeautifulSoup
#导入排队模块
from gevent.queue import Queue

#反扒定义头部信息
headers={
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
"Cache-Control": "no-cache",
"Connection": "keep-alive",
"Cookie": "_userCode_=2020451637419896; _userIdentity_=202045163741409; _tt_=83C3346A4ABF32A15DAC83F524ABDC88; DefaultCity-CookieKey=790; DefaultDistrict-CookieKey=0; __utmz=196937584.1586075862.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); waf_cookie=1927b8ea-7200-4362e44603ccfbe1d98af3fa48f36c39736d; _ydclearance=75a4699927cdeabbca67c445-b749-4885-895d-ca23d57dcc9f-1586260718; __utma=196937584.1951495530.1586075862.1586243073.1586253519.7; __utmc=196937584; __utmt=1; __utmt_~1=1; __utmb=196937584.2.10.1586253519; Hm_lvt_6dd1e3b818c756974fb222f0eae5512e=1586075865,1586237813,1586253520; Hm_lpvt_6dd1e3b818c756974fb222f0eae5512e=1586253520",
"Host": "www.mtime.com",
"Pragma": "no-cache",
"Upgrade-Insecure-Requests": "1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

#创建队列
work = Queue()
url_1 = "http://www.mtime.com/top/tv/top100/"
#队列储存数据
work.put_nowait(url_1)

#循环2-10页
url_2 = "http://www.mtime.com/top/tv/top100/index-{page}.html"
for x in range(2,999):
    real_url = url_2.format(page=x)
    #队列存储数据
    work.put_nowait(real_url)

def crawler():
    #提取数据
    url = work.get_nowait()
    res = requests.get(url,headers=headers)
    #print(res.status_code)
    bs_res = BeautifulSoup(res.text,"html.parser")
    datas = bs_res.find_all("div",class_="mov_con")
    for data in datas:
        TV_title = data.find("a").text
        data = data.find_all("p")
        TV_data =""
        for i in data:
            TV_data =TV_data + ''+i.text
        writer.writerow([TV_title,TV_data])
        print([TV_title,TV_data])

csv_file =open("MovieTop100.csv",'w',newline='',encoding="utf-8")
writer = csv.writer(csv_file)

task_list = []
for x in range(5):
    task = gevent.spawn(crawler)
    task_list.append(task)
gevent.joinall(task_list)