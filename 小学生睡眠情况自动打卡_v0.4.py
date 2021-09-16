# -*- coding: utf-8 -*-
"""
Created on 2021/9/9
@author: 胖加菲
腾讯文档，每天按时自动打卡，随机生成睡觉时间。
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import datetime
import time
import random
from datetime import datetime, timedelta
from chinese_calendar import is_workday



def workdays(start,end):
    '''
    计算两个日期间的工作日
    start:开始时间
    end:结束时间
    '''
     # 字符串格式日期的处理
    if type(start) == str:
        start = datetime.strptime(start,'%Y-%m-%d').date()
    if type(end) == str:
        end = datetime.strptime(end,'%Y-%m-%d').date()
    # 开始日期大，颠倒开始日期和结束日期
    if start > end:
        start,end = end,start
    counts = 0
    while True:
        if start > end:
            break
        if is_workday(start):
            counts += 1
        start += timedelta(days=1)
    return counts

#随机选择一个睡觉时间
sleeptime = ['21:00', '21:10', '21:20', '21:30', '21:40', '21:50', '21:35']
sleeptime = random.choice(sleeptime)
#print(sleeptime)

# 填写腾讯文档
def visit_txt():
    # print(workdays('2021-08-31','2021-09-14'))  #数据测试用
    date_str = "2021-08-31"  # 开始打开日期
    date_end = datetime.now().strftime('%Y-%m-%d')
    caltime = workdays(date_str, date_end)  # 计算从开始打卡到今天间隔的工作日天数
    start = 3  # 开始填表的列数
    c = chr(int(caltime) + start - 1 + 65)  # 计算偏量值1，当日打卡
    # print(c)
    h = 43	# 行号，即你要填写对应的行号
  
    url = "https://docs.qq.com/sheet/DRGFOR09Qc2hMTnNs?tab=g273er&c=" + c + str(h) +"A0A0" # 需要修改
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)
    driver.implicitly_wait(20)
    time.sleep(10)
    elmet = driver.find_element_by_id("header-login-btn")
    elmet.click()
    time.sleep(2)
#    elmet = driver.find_element_by_id("blankpage-button-pc")
#    elmet.click()
#    time.sleep(3)
    # 得提前登录qq，因为这里用了快捷登录接口
    driver.switch_to.frame("login_frame")
    elmet = driver.find_element_by_id("img_out_527630")# 需要修改
    elmet.click()
    # 转换frame
    driver.switch_to.parent_frame()
    time.sleep(5)

    try:
#录入数据
        elmet = driver.find_element_by_class_name('formula-input')
        elmet.click()
        elmet.send_keys(sleeptime)  # 输入xxx,即你想输入的字符
        time.sleep(1)
        elmet.send_keys(Keys.ENTER)
        time.sleep(3)
        elmet.send_keys(Keys.TAB)
        print("打卡成功！！！")

    except:
        print("出现某些异常，请检查！！！")

if __name__ == "__main__" :
     visit_txt()
