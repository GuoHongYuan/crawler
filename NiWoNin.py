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

class NiWoNinTuanGou:
    '''
    你我您爬虫
    ***token需要定期更换*********
    '''
    def __init__(self):

        self.dict = []
        self.dict = UserAgent.Android_USER_AGENT+UserAgent.iPhone_USER_AGENT

        #self.ipf = IpFilter('1')

        self.outwb = Workbook()#Excel对象

        self.agentCode = {
            '长沙':{
                '今日团品':'agentCode=Agt18082315112411716&latitude=39.966711&longitude=116.374811&columnCode=AC18081914381217643&searchValue=&opc=cs_cs',
                '优品返厂':'agentCode=Agt18082315112411716&latitude=39.966711&longitude=116.374811&columnCode=AC18090120173816728&searchValue=&opc=cs_cs'
            },
            '重庆':{
                '新鲜水果':'agentCode=Agt18110518312515172&latitude=39.966711&longitude=116.374811&columnCode=AC18102711482711022&searchValue=&opc=cd_cq',
                '速冻美食':'agentCode=Agt18110518312515172&latitude=39.966711&longitude=116.374811&columnCode=AC18102711582313352&searchValue=&opc=cd_cq',
                '休闲零食':'agentCode=Agt18110518312515172&latitude=39.966711&longitude=116.374811&columnCode=AC18102711524119774&searchValue=&opc=cd_cq',
                '时令鲜疏':'agentCode=Agt18110518312515172&latitude=39.966711&longitude=116.374811&columnCode=AC18102711502517422&searchValue=&opc=cd_cq',
                '鲜花绿植':'agentCode=Agt18110518312515172&latitude=39.966711&longitude=116.374811&columnCode=AC18102714072311025&searchValue=&opc=cd_cq',
                '服饰内衣':'agentCode=Agt18110518312515172&latitude=39.966711&longitude=116.374811&columnCode=AC18102717043115996&searchValue=&opc=cd_cq',
                '美妆护肤':'agentCode=Agt18110518312515172&latitude=39.966711&longitude=116.374811&columnCode=AC18102711552617273&searchValue=&opc=cd_cq',
                '家居日用':'agentCode=Agt18110518312515172&latitude=39.966711&longitude=116.374811&columnCode=AC18102711564512179&searchValue=&opc=cd_cq',
                '粮油干货':'agentCode=Agt18110518312515172&latitude=39.966711&longitude=116.374811&columnCode=AC18102711534012305&searchValue=&opc=cd_cq'
            }
        }
        self.agentCode_url = {} #储存组装后的url
        self.agentCode_Data = {}  #储存agentCode_url请求后数据

        self.url_Activity = 'https://pt.morning-star.cn/pt-app/api/home/getAllActivityCodes?'
        self.url_ActivityInfo = 'https://pt.morning-star.cn/pt-app/api/home/getActivityInfo?'
        self.headers = {
            'charset': 'utf-8',
            'Accept-Encoding': 'gzip',
            'token':'jcegq5ybw0hf',
            'referer': 'https://servicewechat.com/wx3feeea844b1d03ff/52/page-frame.html',
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070336) NetType/WIFI Language/zh_CN Process/appbrand0',
            'Host': 'pt.morning-star.cn',
            'Connection': 'Keep-Alive'
        }

    def initialization(self):   #请求初始化函数 设置useragent和代理ip
        self.headers['User-Agent'] = random.sample(self.dict, 1)[0]
        #print self.headers['User-Agent']
        #self.proxies = self.ipf.getIp()
        self.proxies = {'HTTP': 'localhost:8080'}
        #print self.proxies
        print '已初始化useragent和代理ip'
    # agentCode_url工厂
    def getAgentCode_Url(self):
        for Key,Value in self.agentCode.items():
            urlDict = {}
            for key,value in Value.items():
                url = self.url_Activity+value
                urlDict[key] = url
                self.agentCode_url[Key] = urlDict
        print 'agentCode_url组装完毕'

    def getExcel(self,career_CityName):
        wo = self.outwb.active
        careerSheet = self.outwb.create_sheet(unicode(career_CityName), 0)
        careerSheet.append(['团购价|零售价', '名称', '结团时间', '预计配送时间', '特色标签', '已售数量|剩余数量'])
        return careerSheet

    def SaveExcel(self,ExcelName):
        self.outwb.save(ExcelName+'.xlsx')

    def getData(self,url):   #post获取数据
        self.initialization()
        req = requests.post(url=url, headers=self.headers,proxies = self.proxies).json()
        return json.dumps(req, ensure_ascii=False)

    # ActivityInfo_url工厂
    def getData_agentCode(self):
        self.getAgentCode_Url()
        for Key,Value in self.agentCode_url.items():
            urlDict = {}
            for key,value in Value.items():
                urlstr = self.url_ActivityInfo+'activityCodeStr='
                for data_ in json.loads(self.getData(value))['data']['activityCodes']:  #json.loads json转dict
                    urlstr = urlstr + data_ + ','
                urlDict[key] = urlstr
                self.agentCode_Data[Key] = urlDict
        #print self.agentCode_Data
        print 'ActivityInfo_url组装完毕'

    def getData_ActivityInfo(self):
        for Key,Value in self.agentCode_Data.items():
            for key,value in Value.items():
                careerSheet = self.getExcel(Key+'_'+key)   # 通过 self.outwb 新建的城市-类别 的excel页
                bool = True
                while bool:
                    try:
                        self.initialization()
                        new_dict = json.loads(self.getData(value))
                        print value
                        if new_dict['desc'] == '成功':
                            bool = False
                            for item in new_dict['data']:
                                careerSheet.append([
                                    item['priceS'] , #团购价|零售价
                                    item['title'] , # 名称
                                    item['endTime'],  # 结团时间
                                    item['expArriveTime'],  # 预计配送时间
                                    item['label'],  # 特色标签
                                    item['activityCountS'],  # 已售数量|剩余数量
                                ])
                        bool = False
                        print Key + '_' + key + json.loads(self.getData(value))['desc']
                    except:
                        print Key+'_'+key+'爬取失败'
    def Crawl(self,ExcelName):
        self.getData_agentCode() #组装url
        self.getData_ActivityInfo()  #获取数据
        self.SaveExcel(ExcelName)  #储存


n = NiWoNinTuanGou()
n.Crawl('NiWoNin')




























