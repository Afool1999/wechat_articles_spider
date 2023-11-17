# coding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
from functools import reduce
from pprint import pprint
import pickle

"""
note: 需要使用selenium，chrome版本需要与chromedriver版本对应。具体见https://chromedriver.storage.googleapis.com/
该文件仅作测试用，可能失效
"""


def login(username, password):
    # 打开微信公众号登录页面
    driver.get("https://mp.weixin.qq.com/")
    driver.maximize_window()
    time.sleep(3)
    
    # 切换登录方式
    driver.find_element(By.XPATH,
        '//div[@id="app"]/div[2]/div[2]/div/div/div[2]/a'
    ).click()
    time.sleep(.2)
    # 自动填充帐号密码
    driver.find_element(By.XPATH,
        '//div[@id="app"]/div[2]/div[2]/div/div/div/form/div/div/div/span/input'
    ).clear()
    driver.find_element(By.XPATH,
        '//div[@id="app"]/div[2]/div[2]/div/div/div/form/div/div/div/span/input'
    ).send_keys(username)
    driver.find_element(By.XPATH,
        '//div[@id="app"]/div[2]/div[2]/div/div/div/form/div/div[2]/div/span/input'
    ).clear()
    driver.find_element(By.XPATH,
        '//div[@id="app"]/div[2]/div[2]/div/div/div/form/div/div[2]/div/span/input'
    ).send_keys(password)
    time.sleep(.2)

    # 登录
    driver.find_element(By.XPATH,
        '//div[@id="app"]/div[2]/div[2]/div/div/div/form/div[4]/a'
    ).click()

    # 拿手机扫二维码！
    time.sleep(15)


def open_link(nickname):
    # 进入新建图文素材
    driver.find_element(By.XPATH,
        '//div[@class="new-creation__menu-item"][1]'
    ).click()
    time.sleep(10)

    # 切换到新窗口
    for handle in driver.window_handles:
        if handle != driver.current_window_handle:
            driver.switch_to.window(handle)

    # 点击超链接
    driver.find_element(By.XPATH,'//li[@id="js_editor_insertlink"]').click()
    time.sleep(3)
    # 点击查找文章
    driver.find_element(By.XPATH,'//button[@class="weui-desktop-btn weui-desktop-btn_default"][1]').click()
    # 输入公众号名称
    driver.find_element(By.XPATH,
        '//*[@placeholder="输入文章来源的公众号名称或微信号，回车进行搜索"]'
    ).clear()
    driver.find_element(By.XPATH,
        '//*[@placeholder="输入文章来源的公众号名称或微信号，回车进行搜索"]'
    ).send_keys(nickname)
    # 点击搜索
    driver.find_element(By.XPATH,
        '//*[@class="weui-desktop-icon-btn weui-desktop-search__btn"][1]'
    ).click()
    time.sleep(3)
    # 点击第一个公众号
    driver.find_element(By.XPATH,
        '//*[@class="inner_link_account_item"][1]'
    ).click()
    time.sleep(3)


def get_url_title(html):
    lst = []
    for item in driver.find_elements_by_class_name(By.CLASS_NAME, "my_link_item"):
        temp_dict = {
            "date": item.text.split("\n")[0],
            "url": item.find_element_by_tag_name("a").get_attribute("href"),
            "title": item.text.split("\n")[1],
        }
        lst.append(temp_dict)
    return lst


# 用webdriver启动谷歌浏览器
chromedriver_path = "C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe"
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service)

nickname = "萤人聚集地"  # 公众号名称
username = "yieer123@126.com"  # 账号
password = "Shichufeng991125"  # 密码
login(username, password)
open_link(nickname)
page_num = int(
    driver.find_elements_by_class_name(By.CLASS_NAME, "page_num")[-1].text.split("/")[-1].lstrip()
)

# 点击下一页
url_title_lst = get_url_title(driver.page_source)

for _ in range(1, page_num):
    try:
        pagination = driver.find_elements_by_class_name(By.CLASS_NAME, "pagination")[1]
        pagination.find_elements_by_tag_name("a")[2].click()
        time.sleep(5)
        url_title_lst += get_url_title(driver.page_source)
    except:
        # 保存
        with open("data.pickle", "wb") as f:
            pickle.dump(url_title_lst, f)
        print("第{}页失败".format(_))
        break

with open("data2.pickle", "wb") as f:
    pickle.dump(data, f)
# 读取
with open("data.pickle", "rb") as f:
    b = pickle.load(f)
