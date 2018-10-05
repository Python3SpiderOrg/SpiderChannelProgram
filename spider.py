# !usr/bin/env python3
# -*- coding:utf-8 -*- 
"""
@project = SpiderChannelProgram
@file = spider
@author = Easton Liu
@time = 2018/10/4 23:21
@Description: 

"""
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
from datetime import timedelta

link = r'https://www.tvmao.com'
# 央视
cctv_prog = ['CCTV1','CCTV2','CCTV3','CCTV4','CCTV5','CCTV6','CCTV7','CCTV8','CCTV9','CCTV10','CCTV11','CCTV12','CCTV13',
             'CCTV14','CCTV16']
#卫视
province_prog = ['AHTV1','BTV1','GDTV1','SZTV1','GUANXI1','HUNANTV1','JSTV1']

def read_channelname():
    channelname=[]
    errorname=[]
    try:
        with open('channelname.txt','r') as f:
            for line in f.readlines():
                if line=='HNTV':
                    line = 'HUNANTV1'
                elif line=='GXTV':
                    line = 'GUANXITV1'
                elif line=='CCTV15':
                    line = 'CCTV16'
                elif line.strip('\n') in cctv_prog:
                    line = line
                elif line.strip('\n') in province_prog:
                    line = line+'1'
                else:
                    errorname.append(line)
                channelname.append(line.strip('\n'))
        if len(errorname)!=0:
            raise ("暂时不支持频道%s的节目单爬取，请检查频道名称！"%errorname)
    except:
        raise ("channelname.txt文件不存在！")
    return channelname

def get_program_info(channelname):
    now = datetime.datetime.now()
    this_week_start = now - timedelta(days=now.weekday()) #获取本周一的时间
    for name in channelname:
        for i in range(1,3):
            if name in cctv_prog:
                url = link+'/program/'+'CCTV-'+name+'-w'+str(i)+'.html'
            elif name in province_prog:
                url = link+'/program_satellite/'+name+'-w'+str(i)+'.html'
            else:
                raise ("频道名称错误，请检查！")
            driver_path=os.getcwd()+'\driver\chromedriver.exe'
            driver =  webdriver.Chrome(executable_path=driver_path)
            driver.get(url)
            page_source = driver.page_source
            driver.quit()
            soup = BeautifulSoup(page_source,'lxml')
            program_data = soup.find_all(class_="over_hide")
            with open("%s.txt" % name, "a") as f:
                f.writelines((this_week_start + datetime.timedelta(days=(i - 1))).strftime("%Y/%m/%d"))
                f.write('\n')
            for program in program_data:
                program_time = program.find("span").string
                program_name = program.find(class_="p_show").text
                with open("%s.txt"%name,"a") as f:
                    f.writelines(program_time+'  '+program_name)
                    f.write('\n')
            time.sleep(1)

if __name__=='__main__':
    name = read_channelname()
    get_program_info(name)
