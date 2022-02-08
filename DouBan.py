# encoding: utf-8
"""
@Time: 2020/6/7 16:33
@Software: PyCharm
"""

import re
import xlwt
import urllib.request
from bs4 import BeautifulSoup
import sqlite3

# 1.爬取网页
# 2.解析网页
# 3.保存文件
def main():  #主函数

    #请求网页
    baseurl = 'https://movie.douban.com/top250?start='
    datalist = getData(baseurl)

    #保存数据
    # savepath = r"D:\豆瓣Top250.xls"
    savepath = ".\豆瓣Top250.xls"
    saveData(datalist,savepath)

    #数据库保存
    dbpath = 'Moives.db' # 创建数据库
    saveDataDB(datalist,dbpath)

    #askURL('https://movie.douban.com/top250?start=')


# 创建正则匹配对象，匹配规则
#re.S让换行符包含在字符串中
#\d 数字
findlink = re.compile(r'<a href="(.*?)">')  #影片详情链接
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)  #影片图片链接
findtitle = re.compile(r'<span class="title">(.*)</span>')  #影片片名
findRating = re.compile('<span class="rating_num" property="v:average">(.*)</span>') #影片评分
findJuge = re.compile('<span>(\d*)人评价</span>')  #影片评价人数
findInq = re.compile('<span class="inq">(.*)</span>') #影片简介
findBD = re.compile('<p class="">(.*?)</p>',re.S) #影片相关内容


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl +str(i*25)
        html = askURL(url)


        # 逐一解析网页
        soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all('div',class_='item'):
            # print(item)  #item全部信息
            data = []  #保存一部电影信息
            item = str(item)  #转化为字符串类型

            # print(item)  #打印一个item
            # break        #返回、不在执行

            # re匹配指定内容
            #replace字符  更改/为空字符
            link = re.findall(findlink,item)[0]     #影片链接
            data.append(link)

            Image = re.findall(findImgSrc,item)[0]  #图片链接
            data.append(Image)

            titles = re.findall(findtitle,item)     #影片片名
            if (len(titles) == 2):
                ctitle = titles[0]  #中文片名
                data.append(ctitle) #添加中文名
                otitle = titles[1].replace('/','')  #外文片名
                data.append(otitle.strip()) #添加英文名
            else:
                data.append(titles[0])
                data.append(' ')    #外文名留空

            Rating = re.findall(findRating,item)[0]    #影片评分
            data.append(Rating)

            JugeNum = re.findall(findJuge,item)[0]     #评价人数
            data.append(JugeNum)

            Inq = re.findall(findInq,item)             #影片概况
            if len(Inq) != 0:
                Inq = Inq[0].replace('。','')         #去掉句号
                data.append(Inq)                      #添加概述
            else:
                data.append(' ')                       #留空

            bd = re.findall(findBD,item)[0]            #影片相关内容
            bd = re.sub('<br(\s+)?/>(\s+)?',' ',bd)    #去掉<br/>
            bd = re.sub('/', ' ', bd)                  #去掉/
            data.append(bd.strip())                    #去掉前后空格

            datalist.append(data)                      #将处理好的信息放入datalist
    # for i in datalist:
    #     print(i)
    return datalist

# 得到指定一个url的网页内容
def askURL(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    request= urllib.request.Request(url,headers=headers)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    return html

# 保存数据Excel
def saveData(datalist,savepath):
    print('save...')
    work = xlwt.Workbook(encoding='utf-8',style_compression=1)  #样式压缩
    sheet = work.add_sheet('豆瓣Top250',cell_overwrite_ok=True)    #写入时覆盖之前内容
    col = ('影片链接','图片链接','影片中文名','影片外文名','影片评分','影片评价人数','影片简介','影片相关内容')

    for i in range(0,8):
        sheet.write(0,i,col[i]) #列名  添加表头

    for i in range(0,250):
        print('第%d条'%(i+1))
        data = datalist[i]  #遍历每条信息
        for j in range(0,8):
            sheet.write(i+1,j,data[j])  #数据写入。第二列开始写入(1,内容信息)


    book = work.save(savepath)  #文件保存

# 数据库保存数据
def saveDataDB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for datadb in datalist:
        for index in range(len(datadb)):
            if index ==4 or index == 5:
                continue
            datadb[index] = '"'+datadb[index]+'"'

        sql = '''
            insert into MovieDB(
            info_link,pic_link,cname,ename,score,reted,instroduction,info)
            values(%s)'''%','.join(datadb)

        # print(sql)
        cur.execute(sql) #执行sql语句
        conn.commit() #提交
    cur.close()
    conn.close()

# 初始化数据库
def init_db(dbpath):
    sql = '''
    create table MovieDB
    (
    id integer primary key autoincrement,
    info_link text,
    pic_link text,
    cname varchar,
    ename varchar,
    score numeric,
    reted numeric,
    instroduction text,
    info text
    )
    '''  #创建表
    conn = sqlite3.connect(dbpath)#连接数据库
    c = conn.cursor() #创建游标
    c.execute(sql) #执行sql语句
    conn.commit() #提交表单
    conn.close() #关闭数据库


if __name__ == "__main__": #当程序执行时
    main() #调用函数
    # init_db('Movie.db')
    print('爬取完毕')

