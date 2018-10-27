#!/usr/bin/python
# # -*- coding: utf-8 -*-
import datetime
startTime = datetime.datetime.strptime('2018-10-27 14:00:00', "%Y-%m-%d %H:%M:%S")  #游戏开始 UTC 时间 
endTime = startTime + datetime.timedelta(hours=1.5)                      #游戏结束时间
print(endTime.strftime("%Y-%m-%d %H:%M:%S"))