# encoding: utf-8
import requests

res = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&searchid=38536692909188629&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w=%E5%91%A8%E6%9D%B0%E4%BC%A6&g_tk_new_20200303=5381&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0')
json_music = res.json() #转化json数据为列表/字典
#print(json_music)
list_music = json_music['data']['song']['list']
for music in list_music:
    print(music)
    print(music['name'])
    print("所属专辑："+music['album']['name'])
    print('播放时长：'+str(music['interval'])+'秒')
    print('发行时间：'+str(music["time_public"]))
    print('播放链接：'+'https://y.qq.com/n/yqq/song/'+str(music['mid'])+'.html\n')

print('-'*30)

url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
# 请求歌曲评论的url参数的前面部分

for i in range(5):
   params = {
   'g_tk':'5381',
   'loginUin':'0',
   'hostUin':'0',
   'format':'json',
   'inCharset':'utf8',
   'outCharset':'GB2312',
   'notice':'0',
   'platform':'yqq.json',
   'needNewCode':'0',
   'cid':'205360772',
   'reqtype':'2',
   'biztype':'1',
   'topid':'102065756',
   'cmd':'6',
   'needmusiccrit':'0',
   'pagenum':str(i),
   'pagesize':'15',
   'lasthotcommentid':'song_102065756_3202544866_44059185',
   'domain':'qq.com',
   'ct':'24',
   'cv':'10101010'
   }
   # 将参数封装为字典
   res_comments = requests.get(url,params=params)
   # 调用get方法，下载这个字典
   json_comments = res_comments.json()
   list_comments = json_comments['comment']['commentlist']
   for comment in list_comments:
       print(comment['rootcommentcontent'])

