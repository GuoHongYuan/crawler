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

'''
车客生鲜爬虫概要
pid=4 代表品类    page=4代表页数，车客生鲜暂时每类包含四页
pid索引
无--推荐
https://api.jingchengcaidian.com/api/Category/getCategoryName?pid=7&page=1&sessionId=26b81f731dd1ef77abcb51df0364e1ad HTTP/1.1
#url = "https://api.jingchengcaidian.com/api/Category/getCategoryName?pid=4&page=4"
'''
class CheKeShengXian:
    '''车客生鲜爬虫'''
    def __init__(self):

        self.proxies = {}
        self.ipf = IpFilter('1')
        self.dict = []
        self.dict = UserAgent.MY_USER_AGENT
        self.outwb = Workbook()
        self.BaseUrl = "https://api.jingchengcaidian.com/api/Category/getCategoryName?"
        self.headers = {
            'charset': 'utf-8',
            'Accept-Encoding': 'gzip',
            'referer': 'https://servicewechat.com/wx2911548a18ed7d95/42/page-frame.html',
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070337) NetType/WIFI Language/zh_CN Process/appbrand2',
            'Host': 'api.jingchengcaidian.com',
            'Connection': 'Keep-Alive'
        }
        self.PidIndex = {
            '7' :'蔬菜',
            '5' :'水果',
            '4' :'水产',
            '8' :'禽蛋',
            '1' :'肉类',
            '9' :'粮油',
            '2' :'乳饮',
            '10' :'零食',
            '3' :'速食',
            '6' :'生活',
            '23' :'扶贫'
        }
        self.pageCount = [1,2,3,4]

    def initialization(self):
        self.headers['User-Agent'] = random.sample(self.dict, 1)[0]
        #self.proxies = self.ipf.getIp()
        self.proxies = {'HTTP': 'localhost:8080'}
        #s设置请求头和ip

    def getUrlAndSheet(self):  #url工厂
        returnData = {}
        for pid,value in self.PidIndex.items():
            urlList = []
            for page in self.pageCount:
                url = self.BaseUrl+'pid='+pid+'&page='+str(page)
                urlList.append(url)
            returnData[pid] = urlList
        return returnData

    def getExcel(self,careerName,outwb):
        wo = self.outwb.active
        careerSheet = self.outwb.create_sheet(unicode (careerName), 0)
        careerSheet.append(['id', '库存amount', '下单数buynum', '团购价格group_price', '划线价market_price', '名称name', '特色标签label', '描述samllpromotion'])
        return careerSheet

    def SaveExcel(self,ExcelName):
        self.outwb.save(ExcelName+'.xlsx')

    def getData(self):
        urlDict = self.getUrlAndSheet()
        for key,values in urlDict.items():
            careerSheet = self.getExcel(self.PidIndex[key],self.outwb)
            for url in values:
                bool = True
                while bool: #如果代理ip和请求头未能获得数据，则更换信息，继续请求
                    try:
                        self.initialization()

                        req = requests.get(url=url,headers=self.headers).json()
                        data1 = json.dumps(req, ensure_ascii=False)
                        data2 = json.loads(data1)
                        if data2['message'] == '列表获取成功':
                            for item in data2['data']:
                                careerSheet.append([item['id'],
                                                    item['amount'],
                                                    item['buynum'],
                                                    item['group_price'],
                                                    item['market_price'],
                                                    item['name'],
                                                    item['lable'],
                                                    item['smallpromotion']
                                                    ])
                        bool = False
                        print data2['message']
                    except:
                        print '爬虫失败,继续尝试'
    def Crawl(self,ExcelName):
        self.getData()
        self.SaveExcel(ExcelName)

c = CheKeShengXian()
c.Crawl('CheKeShengXian')

















