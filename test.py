# !usr/bin/env python3
# -*- coding:utf-8 -*- 
"""
@project = SpiderChannelProgram
@file = test
@author = Easton Liu
@time = 2018/10/5 12:52
@Description: 

"""
import os
from  lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver

import time
import datetime
from datetime import timedelta


now = datetime.datetime.now()
this_week_start = now - timedelta(days=now.weekday()) #获取本周一的时间
day = (this_week_start + datetime.timedelta(days=(2 - 1))).strftime("%Y/%m/%d")
print(day[2:])

