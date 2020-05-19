from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options # 从options模块中调用Options类

#【QQ音乐热评spider】
chrome_options = Options() # 实例化Option对象
chrome_options.add_argument('--headless') # 把Chrome浏览器设置为静默模式
driver = webdriver.Chrome("c:\chromedriver.exe",options = chrome_options) # 设置引擎为Chrome，在后台默默运行

#driver = webdriver.Chrome("c:\chromedriver.exe") #启动程序
driver.get("https://y.qq.com/n/yqq/song/000xdZuV2LcQ19.html")#打开网页
time.sleep(2)

#查找【加载更多按钮】
button = driver.find_element_by_class_name("js_get_more_hot")
#点击【加载更多按钮】
button.click()
time.sleep(2)

#1查找所有评论区中一条评论 /【使用class_name找到评论】
comments = driver.find_element_by_class_name("js_hot_list").find_elements_by_class_name("js_cmt_li")
time.sleep(2)
#2打印长度
print(len(comments))
print()
#3for循环所有评论
for comment in comments:
    sweet = comment.find_element_by_tag_name("p")
    print('评论：%s\n--\n'%sweet.text)
#关闭驱动
driver.close()



