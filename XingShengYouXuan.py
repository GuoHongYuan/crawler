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

class xsyx:
    # 兴盛优选爬虫
    def __init__(self):

        self.dict = []
        self.dict = UserAgent.Android_USER_AGENT+UserAgent.iPhone_USER_AGENT
        #self.ipf = IpFilter('1')
        self.outwb = Workbook()#Excel对象

        self.url = 'https://yd.frxs.cn/api/user/product/indexProduct?'
        self.messageData = 'storeId=1141&userKey=d3910b61-5852-4e74-82c8-dc1050e255f1'

        self.headers = {
            'charset': 'utf-8',
            'Accept-Encoding': 'gzip',
            'referer': 'https://servicewechat.com/wx6025c5470c3cb50c/13/page-frame.html',
            'content-type': 'application/x-www-form-urlencoded',

            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070336) NetType/WIFI Language/zh_CN Process/appbrand0',
            'Host': 'yd.frxs.cn',
            'Connection': 'Keep-Alive'
        }

    def initialization(self):   #请求初始化函数 设置useragent和代理ip
        self.headers['User-Agent'] = random.sample(self.dict, 1)[0]
        #print self.headers['User-Agent']
        #self.proxies = self.ipf.getIp()
        self.proxies = {'HTTP': 'localhost:8080'}
        #print self.proxies
        print '已初始化useragent和代理ip'

    def getExcel(self,career_Name):
        wo = self.outwb.active
        careerSheet = self.outwb.create_sheet(unicode(career_Name), 0)
        careerSheet.append(['预售时间', '提货时间','商家', '规格', '数量', '展示名称','团购价','划线价','已售数量','限量'])
        return careerSheet

    def SaveExcel(self,ExcelName):
        self.outwb.save(ExcelName+'.xlsx')

    def getDataByUrl(self,url):
        print url
        self.initialization()
        req = requests.post(url=url, headers=self.headers,proxies = self.proxies).json()
        return json.dumps(req, ensure_ascii=False)

    def SaveData(self):
        data = json.loads(self.getDataByUrl(self.url + self.messageData))
        careerSheet = self.getExcel('兴盛优选-长沙')
        try:
            for item in data['data']['pres']:
                careerSheet.append([
                    item['tmBuyStart'], #预售时间
                    item['tmPickUp'],  # 提货时间
                    item['veName'],  # 商家
                    item['attrs'][0]['name'],  # 规格
                    item['attrs'][0]['attr'],  # 数量
                    item['prName'],  # 展示名称
                    item['saleAmt'],  # 团购价
                    item['marketAmt'],  # 划线价
                    item['saleQty'],  # 已售数量
                    item['limitQty'],  # 限量
                ])
                print 'Success'
        except:
            print 'Fail'

    def Crawl(self,ExcelName):
        self.SaveData()
        self.SaveExcel(ExcelName)  #储存

xsyx = xsyx()
xsyx.Crawl('XingShengYouXuan')
