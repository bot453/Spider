#selenium 发表评论
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options # 从options模块中调用Options类

#记录时间
start = time.time()
'''
chrome_options = Options() # 实例化Option对象
chrome_options.add_argument('--headless') # 把Chrome浏览器设置为静默模式
driver = webdriver.Chrome("c:\chromedriver.exe",options = chrome_options) # 设置引擎为Chrome，在后台默默运行
'''
driver = webdriver.Chrome("c:\chromedriver.exe")

#打开网页
driver.get("https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-login.php")
time.sleep(2)
#查找【用户名】框
user = driver.find_element_by_id("user_login")
#输入内容
user.send_keys("1987662794@qq.com")
time.sleep(1)
#查找【密码】框
passwd = driver.find_element_by_id("user_pass")
#填写内容
passwd.send_keys("qwe147369.cn")
time.sleep(1)
#查找【登录按钮】
sub = driver.find_element_by_id("wp-submit")
#点击登录
sub.click()
time.sleep(1)

#寻找第一个【未来已来（三）——同九义何汝秀】
one = driver.find_element_by_partial_link_text("汝秀")
#点击
one.click()
time.sleep(2)

#查找评论框
comment = driver.find_element_by_id("comment")
time.sleep(1)
#输入内容
comment.send_keys("Selenium 123。。")
time.sleep(1)
#寻找发表
submit = driver.find_element_by_id("submit")
time.sleep(1)
#点击发表
submit.click()
time.sleep(1)
end =time.time() #结束时间

title = driver.find_element_by_class_name("comments-title")
print(title.text)
print(start-end) #打印运行时间
driver.close()