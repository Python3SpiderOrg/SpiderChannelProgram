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
                if line.strip('\n')=='HNTV':
                    line = 'HUNANTV1'
                elif line.strip('\n')=='GXTV':
                    line = 'GUANXI1'
                elif line.strip('\n')=='CCTV15':
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
    driver_path = os.getcwd() + '\driver\phantomjs.exe'
    driver = webdriver.PhantomJS(executable_path=driver_path)
    for name in channelname:
        print("正在爬取%s的节目单!" % name)
        if os.path.exists(os.getcwd() + "\output\%s.txt" % name):
            os.remove(os.getcwd() + "\output\%s.txt" % name)
        for i in range(1,15):
#            print("正在爬取%s的第%d天节目单!" % (name,i))
            if name in cctv_prog:
                url = link+'/program/'+'CCTV-'+name+'-w'+str(i)+'.html'
            elif name in province_prog:
                url = link+'/program_satellite/'+name+'-w'+str(i)+'.html'
            else:
                raise ("频道名称错误，请检查！")
#            print(url)
            driver.get(url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source,'lxml')
            program_data = soup.find(id="pgrow")
#            print(program_data)
            if program_data.find("span") is not None:
                with open(os.getcwd()+"\output\%s.txt" % name, "a") as f:
                    f.writelines((this_week_start + datetime.timedelta(days=(i - 1))).strftime("%Y/%m/%d"))
                    f.write('\n')
                for program in program_data.find_all('li'):
                    if  program.get('id') not in ('noon','night') :
                        program_time = program.find("span").text
    #                    print(program_time)
                        program_name = program.find(class_="p_show").text
                        with open(os.getcwd()+"\output\%s.txt"%name,"a") as f:
                            f.writelines(program_time+'  '+program_name)
                            f.write('\n')
    driver.quit()

if __name__=='__main__':
    name = read_channelname()
    get_program_info(name)
    print("所有频道的节目单爬取完毕！")
