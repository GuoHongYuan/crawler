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

class SHSX:
    # 食行生鲜爬虫
    def __init__(self):
        self.dict = []
        self.dict = UserAgent.Android_USER_AGENT+UserAgent.iPhone_USER_AGENT
        #self.ipf = IpFilter('1')
        self.outwb = Workbook()#Excel对象

        self.url_Class = {
            '蔬菜豆菇':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100840',
            '新鲜水果':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100559',
            '鲜肉蛋禽':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100771',
            '水产生鲜':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100591',
            '乳品烘培':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100705',
            '面点速食':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100736',
            '粮油副食':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100870',
            '休闲零食':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100935',
            '酒水饮料':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100996',
            '生活百货':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=100625',
            '鲜花绿植':'https://api1.34580.com/sz/productcategory/firstdetail?sourcetype=9&id=101017'
        }
        self.headers = {
            'charset': 'utf-8',
            'Accept-Encoding': 'gzip',
            'referer': 'https://servicewechat.com/wx6e7ce0c196b0c3c2/32/page-frame.html',
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070338) NetType/WIFI Language/zh_CN Process/toolsmp',
            'Host': 'api1.34580.com',
            'Connection': 'Keep-Alive'
        }

    def getBaseUrl(self,str_ID):
        # 每次每页取最大数据
        url_allClass = 'https://api1.34580.com/sz/ProductRequests/ProductMultiConditionRequest?sourcetype=9&OrderDirectionType=0&OrderFieldType=0&CategoryIds=%s&PageSize=%s&PageIndex=1&SourceType=9&MallTypes=&joinedproduct=true' % (str_ID, '1000')
        return url_allClass

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
        careerSheet.append(['展示名称', '团购价','标签', '划线价', '单价', '重量', '单位','展示名称','已售数量'])
        return careerSheet

    def SaveExcel(self,ExcelName):
        self.outwb.save(ExcelName+'.xlsx')

    def getDataByUrl(self,url):
        print '当前url'+url
        self.initialization()
        req = requests.get(url=url, headers=self.headers,proxies = self.proxies).json()
        return json.dumps(req, ensure_ascii=False)

    def getAllClassID(self):
        for Key,Value in self.url_Class.items():
            urlDict = {}
            urldata_ID = json.loads(self.getDataByUrl(Value))
            for item in urldata_ID['Data']['Children']:
                urlDict[item['Name']] = self.getBaseUrl(item['Id'])
            self.url_Class[Key] = urlDict
        print '所有子类url组装到url_Class——完毕'
        #print self.url_Class

    #获得点开商品后的数据 如 销售量
    def getSingleProductData(self,id):
        data_ = ''
        try:
            url = "https://api1.34580.com/sz/product/detail?sourcetype=9&ssuId=%s" % id
            headers = {
                'charset': 'utf-8',
                'Accept-Encoding': 'gzip',
                'referer': 'https://servicewechat.com/wx6e7ce0c196b0c3c2/32/page-frame.html',
                'content-type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070338) NetType/WIFI Language/zh_CN Process/toolsmp',
                'Host': 'api1.34580.com',
                'Connection': 'Keep-Alive'
            }
            req = requests.get(url=url, headers=headers).json()
            data = json.loads(json.dumps(req, ensure_ascii=False))
            data_ = data['result']['productInfo']['soldNumber']
        except:
            print '销售量失败'
        print data_
        return data_


    def getAllClassData(self):
        self.getAllClassID()
        for Key,Value in self.url_Class.items():
            careerSheet = self.getExcel(Key) #以一级分类为基础建立Excel页
            for key,value in Value.items():
                careerSheet.append([key])
                try:
                    data = json.loads(self.getDataByUrl(value))
                    if data['Message'] == '返回正确':
                        for item in data['Data']['SourceData']:
                            careerSheet.append([
                                item['ProductName'],  #展示名称
                                item['UnitPeriodMoney'],  # 团购价
                                item['PriceName'],  # 标签
                                item['DefaultMoney'],  # 划线价
                                item['PvStandard'],  # 单价
                                item['Weight'],  # 重量
                                item['Unit'],  # 单位
                                item['ProductName'],  # 展示名称
                                str(self.getSingleProductData(item['ProductId'])) #已售数量
                            ])
                    print data['Message']
                except:
                    print 'Fail'


    def Crawl(self,ExcelName):
        self.getAllClassData() #组装url
        self.SaveExcel(ExcelName)  #储存






SHSX1 = SHSX()
SHSX1.Crawl('ShiHangShengXian')






































