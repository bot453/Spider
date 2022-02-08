# encoding: utf-8
"""
@software: PyCharm
@time: 2020/4/13 15:45
"""
import requests
import bs4
import csv
#序号/电影名/评分/推荐语/链接
csv_file =open("豆瓣T250.csv",'w',newline='')
writer = csv.writer(csv_file)
list = ['编号','书名','评分','链接','推荐语'] #创建列表
writer.writerow(list)

for x in range(11):
    url = 'https://movie.douban.com/top250?start=' + str(x * 25) + '&filter='
    headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    res = requests.get(url,headers=headers)
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    contents = soup.find_all('div',class_='item')
    for content in contents:
        try:
            pic = content.find('div',class_='pic').text.strip() #编号
            title = content.find('span',class_='title').text    #名称
            rating_num = content.find('span',class_='rating_num').text  #评分
            inq = content.find('span',class_='inq').text    #推荐语
            real_url = content.find('a')['href']
            list = (pic,title,rating_num,real_url,inq)
            writer.writerow(list)
        except:
            continue
csv_file.close()
print("okay")