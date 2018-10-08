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
import requests
import time
import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import datetime
from datetime import timedelta
from collections import OrderedDict

#tvmao_url = r'https://www.tvmao.com' #PC端电视猫
#mobile_tvmao_url = r'https://m.tvmao.com' #移动终端电视猫
#baitv_url = r'http://www.baitv.com' #PC端百视网
urls = {'tvmao_url':r'https://www.tvmao.com' ,'mobile_tvmao_url':r'https://m.tvmao.com','baitv_url':r'http://www.baitv.com'}
driver_path = os.getcwd() + '\driver\phantomjs.exe'
program_info = OrderedDict() #创建一个有序字典
# days = range(1,15) #爬取天数
week_dict = {"0":'星期天',"1": "星期一", "2": "星期二", "3": "星期三", "4": "星期四", "5": "星期五", "6": "星期六"}
# 央视
cctv_prog = {'CCTV1':'CCTV1','CCTV2':'CCTV2','CCTV3':'CCTV3','CCTV4':'CCTV4','CCTV5':'CCTV5','CCTV5+':'CCTV5-PLUS',
             'CCTV6':'CCTV6','CCTV7':'cctv7','CCTV8':'CCTV8','CCTV9':'CCTV9','CCTV10':'CCTV10','CCTV11':'CCTV11',
             'CCTV12':'CCTV12','CCTV13':'CCTV13','CCTV14':'CCTV14','CCTV15':'CCTV16'}
#卫视
province_prog = {'AHWS':'AHTV','BTV':'BTV','GDWS':'GDTV','SZWS':'SZTV','GXWS':'GUANXI','HNWS':'HUNANTV','JSWS':'JSTV',
                 'YNWS':'YNTV'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}

now = datetime.datetime.now()
this_week_start = now - timedelta(days=now.weekday()) #获取本周一的时间

class Error(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo

def read_channelname():
    channelname=[]
    errorname=[]
    try:
        with open('channelname.txt','r') as f:
            for line in f.readlines():
                if line.strip('\n') not in {**cctv_prog,**province_prog}.keys():
                    errorname.append(line.strip('\n'))
                channelname.append(line.strip('\n'))
        if len(errorname)!=0:
            raise Error("暂时不支持频道%s的节目单爬取，请检查频道名称！"%errorname)
    except FileNotFoundError:
        raise ("channelname.txt文件不存在！")
    return channelname

def select_url(**urls):
    print("检查与目标网址的连接状态......")
    for urlname in urls.keys():
        try:
            rec = requests.get(urls.get(urlname),headers=headers)
            if rec.status_code == 200:
                print("与目标网址%s连接成功，开始爬取节目单......"%urlname)
                return urlname
            else:
                print("与目标网址%s连接失败......" % urlname)
        except:
            pass
    raise ("与所有目标网址连接失败，停止节目单爬取，请检查你的网络！")
class spiderprogram:
    def __init__(self,urlname,channelname,days):
        self.url = urls.get(urlname)
        self.channelname = channelname
        self.days = days

    def spider_tvmao(self):
        driver = webdriver.PhantomJS(executable_path=driver_path)
        for i in range(1,days+1):
            programname_list = []
            if name in cctv_prog.keys():
                link = self.url+'/program/'+'CCTV-'+cctv_prog.get(name)+'-w'+str(i)+'.html'
            elif name in province_prog.keys():
                link = self.url + '/program_satellite/' + province_prog.get(name) + '1'+'-w' + str(i) + '.html'
            else:
                raise ("频道名称错误，请检查！")
            driver.get(link)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source,'lxml')
            program_data = soup.find(id="pgrow")
            if program_data.find("span") is not None:
                day = (this_week_start + datetime.timedelta(days=(i - 1))).strftime("%Y/%m/%d")
                week = week_dict.get((this_week_start + datetime.timedelta(days=(i - 1))).strftime("%w"))
                for program in program_data.find_all('li'):
                    if  program.get('id') not in ('noon','night') :
                        program_time = program.find("span").text
                        program_name = program.find(class_="p_show").text
                        programname_list.append(program_time + '  ' + program_name)
                program_info[day[2:] + '   ' + week] = programname_list
        driver.quit()
        return program_info
    def spider_mobiletvmao(self):
        driver = webdriver.PhantomJS(executable_path=driver_path)
        for i in range(1,days+1):
            programname_list = []
            if name in cctv_prog.keys():
                link = self.url+'/program/'+'CCTV-'+name+'-w'+str(i)+'.html'
            elif name in province_prog.keys():
                link = self.url + '/program/' + province_prog.get(name) + '-' + province_prog.get(
                    name) + '1' + '-w' + str(i) + '.html'
            else:
                raise ("频道名称错误，请检查！")
#                link = r'https://m.tvmao.com/program/CCTV-CCTV1-w17.html'
            driver.get(link)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source,'lxml')
            program_data = soup.find(attrs={'class':"timeline clear blank"})
            if program_data.find("table").tr is not None:
                day = (this_week_start + datetime.timedelta(days=(i - 1))).strftime("%Y/%m/%d")
                week = week_dict.get((this_week_start + datetime.timedelta(days=(i - 1))).strftime("%w"))
                for program in program_data.table.find_all('tr'):
                    if  program.get('id') not in ('noon','night') :
                        program_time = program.find("div").text
                        program_name = program.contents[1].text
                        programname_list.append(program_time+'  '+program_name)
                program_info[day[2:] + '   ' + week] = programname_list
        driver.quit()
        return program_info

    def spider_baitv(self):
        for i in range(1,days+1):
            programname_list = []
            programname_list_bak = []
            if self.channelname in cctv_prog.keys():
                link = self.url + '/program/' + 'CCTV-' + cctv_prog.get(self.channelname) + '-w' + str(i) + '.html'
            elif self.channelname in province_prog.keys():
                link = self.url + '/program/' + province_prog.get(self.channelname) + '-' + province_prog.get(
                    self.channelname) + '1' + '-w' + str(i) + '.html'
            else:
                raise ("频道名称错误，请检查！")
            res = requests.get(link,headers=headers).text
            soup = BeautifulSoup(res, 'lxml')
            program_data = soup.find(attrs={'class': "schedule-data"})
            if program_data is not None:
                day = (this_week_start + datetime.timedelta(days=(i - 1))).strftime("%Y/%m/%d")
                week = week_dict.get((this_week_start + datetime.timedelta(days=(i - 1))).strftime("%w"))
                for program in program_data.find_all(class_='title'):
                    program_name = program.text.replace(' ','').strip().replace('\n','  ')
                    programname_list_bak.append(program_name)
                for pro in programname_list_bak:    #百视网查询的节目单有重复的，对节目单列表去重
                    if pro not in programname_list:
                        programname_list.append(pro)
                program_info[day[2] + '   ' + week] = programname_list
            time.sleep(1)
        return program_info

def write_txt(filename,data):
    path = os.getcwd() + "\output\%s.txt" % filename
    if os.path.exists(path):
        os.remove(path)
    with open(path,'a+') as f:
        for key in data:
            f.writelines(key)
            f.writelines('\n')
            for line in data.get(key):
                f.writelines(line.strip('\n'))
                f.writelines('\n')


def createprogram(channelname,days):
    programfile_path = os.getcwd()+"\programbak\%s.txt"%channelname
    commonfile_path = os.getcwd()+"\programbak\common.txt"
    if os.path.exists(programfile_path):
        readfile_path = programfile_path
    else:
        readfile_path = commonfile_path
    with open(readfile_path,'r') as f:
        programbak_data =f.readlines()
    for i in range(1,days+1):
        day = (this_week_start + datetime.timedelta(days=(i - 1))).strftime("%Y/%m/%d")
        week = week_dict.get((this_week_start + datetime.timedelta(days=(i - 1))).strftime("%w"))
        program_info[day[2:] + '   ' + week] = programbak_data
    return(program_info)




if __name__=='__main__':
    print("读取配置文件......")
    cf = configparser.ConfigParser()
    cf.read('spiderset.conf')
    isspider = int(cf.get('config','isspider'))
    days = int(cf.get('config','days'))
    channelnames = read_channelname()
    if isspider==1 and days<=14:
        print("开始从网络上爬取节目单......")
        spider_urlname = select_url(**urls)
        for name in channelnames:
            print("正在爬取%s的节目单......"%name)
            if spider_urlname == 'tvmao_url':
                data = spiderprogram(spider_urlname,name,days).spider_tvmao()
            elif spider_urlname == 'mobile_tvmao_url':
                data = spiderprogram(spider_urlname,name,days).spider_mobiletvmao()
            else:
                data = spiderprogram(spider_urlname,name,days).spider_baitv()
            write_txt(name,data)
        print("所有频道的节目单爬取完毕！")
    else:
        print("开始自动生成节目单......")
        for name in channelnames:
            print("正在生成%s的节目单......" % name)
            data =createprogram(name,days)
            write_txt(name,data)
        print("所有频道的节目单生成完毕！")




