# -*- coding: utf-8 -*-
import json
import requests
import re
import openpyxl
import random
from openpyxl.workbook import Workbook
from Setting import UserAgent,IpFilter
from Setting.IpFilter import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class THXX:
    # 桃花晓晓爬虫
    def __init__(self):
        self.dict = []
        self.dict = UserAgent.Android_USER_AGENT+UserAgent.iPhone_USER_AGENT
        #self.ipf = IpFilter('1')   #ip代理池
        self.outwb = Workbook()#Excel对象

        self.headers = {
            'charset': 'utf-8',
            'Accept-Encoding': 'gzip',
            'referer': 'https://servicewechat.com/wx58588cb6bb896bd2/15/page-frame.html',
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070338) NetType/WIFI Language/zh_CN Process/toolsmp',
            'Host': 'wxapp.bdsimg.com',
            'Connection': 'Keep-Alive'
            }

    def initialization(self):  # 请求初始化函数 设置useragent和代理ip
        self.headers['User-Agent'] = random.sample(self.dict, 1)[0]
        # print self.headers['User-Agent']
        # self.proxies = self.ipf.getIp()
        self.proxies = {'HTTP': 'localhost:8080'}
        # print self.proxies
        print '已初始化useragent和代理ip'

    def getBaseUrl(self,page):
        # 每次每页取最大数据
        url = "https://wxapp.bdsimg.com/taohua.xiaoxiao/wxapp/?mod=home&page=%s&dstrictid=125" % page  #爬取所有
        return url

    def getExcel(self,career_Name):
        wo = self.outwb.active
        careerSheet = self.outwb.create_sheet(unicode(career_Name), 0)
        careerSheet.append(['标签', '剩余','零售价', '特点', '团购价', '展示名', '已售','预计配送时间'])
        return careerSheet

    def SaveExcel(self,ExcelName):
        self.outwb.save(ExcelName+'.xlsx')

    def getDataByUrl(self,url):
        print '当前url'+url
        self.initialization()
        req = requests.get(url=url, headers=self.headers,proxies = self.proxies).json()
        return json.dumps(req, ensure_ascii=False)


    def getData(self):
        i = 1
        EndCount = 0
        careerSheet = self.getExcel("All")
        while EndCount == 0:
            try:
                data = json.loads(self.getDataByUrl(self.getBaseUrl(str(i))))
                for item in data['products']:
                    careerSheet.append([
                        item['subtitle'], #标签
                        item['restnum'],  # 剩余
                        item['oldprice'],  # 零售价
                        item['point'],  # 特点
                        item['price'],  # 团购价
                        item['title'],  # 展示名
                        item['hadsale'],  # 已售
                        item['distribution'],  # 预计配送时间
                    ])
                    if item['title'] == '1对【凉被子衣架·好评如潮】':   #最后一个商品id
                        EndCount = EndCount + 1
                i = i+1
            except:
                print 'ERROR'
        print '总计爬取%d页数据' % i
    def Crawl(self,ExcelName):
        self.getData() #组装url
        self.SaveExcel(ExcelName)  #储存

THXX_ = THXX()
THXX_.Crawl('TaoHuaXiaoXiao')











