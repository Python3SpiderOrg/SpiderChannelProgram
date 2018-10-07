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
#今天星期几
today=int(time.strftime("%w"))
print (today)




