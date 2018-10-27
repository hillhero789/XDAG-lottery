#!/usr/bin/python
# # -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime
from selenium.common.exceptions import NoSuchElementException
import xlwings as xw
#################以下数据需进行初始化#################
workbook = xw.Book(r'./Tx.xls')     
xlGridIndex = 1
roundIndex = 0                     
lotteryPrice = 0.001                                #彩票价格           
preLastTx = 'w9uZCcIjcLk3h5ER8pgKhM4F0ZDlM0ko'      #该哈希值为钱包当前最后一次交易哈希
lastTX = preLastTx            
delayTime = [24,24,24,12,12,12,6,6,6,3,3,3,2,2,2,1] #每次收到转账时的延时时间，延时时间达到1小时后，每次均延迟1小时。  
startTime = datetime.datetime.strptime('2018-10-27 14:00:00', "%Y-%m-%d %H:%M:%S")  #游戏开始 UTC 时间 
endTime = startTime + datetime.timedelta(hours=24)                      #游戏结束时间
#################以上数据需进行初始化#################

c = webdriver.Chrome()

while True:
    c.get('http://xdagscan.com/cnblockDetails.html?address=SNiOG7aUUyZ3QmSl87T0CsUezb5C5l5X')   #读取页面数据
    time.sleep(5)       #不延时会出问题

    '''#此小段代码目的：通过点击显示更多按钮刷新页面实现显示所有交易数据
    elementBtns = c.find_elements_by_class_name('btn-primary')
    while len(elementBtns) > 1 :    
        elementBtns[1].click()
        elementBtns = c.find_elements_by_class_name('btn-primary')
        time.sleep(5)'''

    tbody = c.find_elements_by_tag_name('tbody')    #tbody[2]为交易数据所在表格
    tds = tbody[2].find_elements_by_tag_name('td')  #tds[0].text 传输方向，tds[1].text 传输哈希，tds[2].text 金额，tds[3].text 时间

    lastTX = tds[1].text
    xlGrid = workbook.sheets('Sheet1').range('A' + str(xlGridIndex))
    if  (not (lastTX == preLastTx)) and (float(tds[2].text) == lotteryPrice) :  #条件成立表示有新的有效交易产生
        preLastTx = lastTX

        endTime = datetime.datetime.strptime(tds[3].text, "%Y-%m-%d %H:%M:%S") 
        xlGrid.value = [lastTX, endTime]
        xlGridIndex = xlGridIndex + 1
        endTime = endTime + datetime.timedelta(minutes=delayTime[roundIndex])
        if roundIndex < len(delayTime)-1:
            roundIndex = roundIndex + 1
        workbook.save()
                                                                                                            #endTim加10分钟是考虑转账到浏览器显示
    if (datetime.datetime.now()) + datetime.timedelta(hours=-8) > endTime + datetime.timedelta(minutes=10): #减8小时就是转换为 UTC 时间
        break
    time.sleep(60)

c.quit()