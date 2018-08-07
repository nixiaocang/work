#coding:utf-8
import time
import json
import numpy as np
import pandas as pd
import requests
from myapp_baidu.main.datasourceservice.apisdk.sms_service_ReportService import sms_service_ReportService
from myapp_baidu.main.datasourceservice.apisdk.sms_service_KeywordService import sms_service_KeywordService
from myapp_baidu.main.datasourceservice.apisdk.sms_service_AccountService import sms_service_AccountService

fmap = {
        "日期":"date",
        "账户名":"account",
        "设备":"device",
        "关键词id":"keywordId",
        "账户id":"account_id",
        "计划id":"campaignId",
        "单元id":"adgroupId",
        "关键词":"keyword",
        "关键词出价":"price",
        "pc url":"pcDestinationUrl",
        "移动url":"mobileDestinationUrl",
        "匹配方式":"matchType",
        "pc关键词质量度":"pcQuality",
        "移动关键词质量度":"mobileQuality",
        "推广渠道":"channel",
        }

class KeywordInfoReport(sms_service_KeywordService):
    def __init__(self, username, password, token):
        self.username = username
        self.password = password
        self.token = token
        self.report_obj = sms_service_ReportService(username, password, token)
        super(KeywordInfoReport, self).__init__(username, password, token)

    def get_data(self, startDate, endDate, metricList):
        account_id = self.get_user_id()
        # get report id
        getProfessionalReportIdRequest = {
                'reportRequestType':{
                    'performanceData':['cost','cpc','click','impression','ctr','cpm','conversion'],
                    'startDate': startDate,
                    'endDate': startDate,
                    'levelOfDetails':11,
                    'unitOfTime':7,
                    'reportType':14
                                }
                            }
        # 分设备获取
        # device = 1 PC  device=2 移动
        fres = []
        for device in (1, 2):
            getProfessionalReportIdRequest['device'] = device
            pres = self.report_obj.getProfessionalReportId(getProfessionalReportIdRequest)
            print(pres)
            print("********")
            preportId = pres['body']['data'][0]['reportId']
            count = 0
            report_param = {
                'reportId':preportId
                }
            while count < 3:
                psres = self.report_obj.getReportState(report_param)
                pstatus = psres['body']['data'][0]['isGenerated']
                if pstatus != 3:
                    time.sleep(5)
                    count += 1
                    if count == 3:
                        raise Exception('报告获取失败')
                else:
                    break
            pures = self.report_obj.getReportFileUrl(report_param)
            purl = pures['body']['data'][0]['reportFilePath']
            res = requests.get(purl)
            with open("/tmp/%s_%s.csv" % (preportId, device), "wb") as code:
                code.write(res.content)
            df = pd.read_csv('/tmp/%s_%s.csv' % (preportId, device), sep='\t', encoding='gbk')
            fres += self.get_keyword_info(account_id, device, df, endDate, metricList)
        return fres


    def get_keyword_info(self, account_id, device, df, endDate, metricList):
        keyword_id_list = np.array(df['关键词keywordID']).tolist()
        keyword_ids = list(set(keyword_id_list))
        # 分批处理
        getWordRequest = {
                "wordFields":["keywordId","keyword","adgroupId", "campaignId", "price", "pcDestinationUrl", "mobileDestinationUrl", "matchType", "pcQuality", "mobileQuality"],
                "idType":11,
                "getTemp":0,
                            }
        data_list = []
        for i in range(0, len(keyword_ids), 10000):
            temp = keyword_ids[i:i+10000]
            getWordRequest["ids"] = temp
            tres = self.getWord(getWordRequest)
            data_list += tres['body']['data']
        fields = [item['id'] for item in metricList]
        if not fields:
            fields =['adgroupId', 'keyword', 'campaignId', 'price', 'pcQuality', 'pcDestinationUrl', 'mobileQuality', 'mobileDestinationUrl', 'keywordId', 'matchType' ]
            fields = ['单元id','关键词','计划id','关键词出价','pc关键词质量度', 'pc url', '移动关键词质量度','移动url','关键词id', '匹配方式','日期','账户名','设备','推广渠道','账户id']
        bag = {
                'date':endDate,
                'account':self.username,
                'channel':'百度推广',
                'account_id':account_id,
                'device': '计算机' if device == 1 else '移动'
                }
        data = []
        for item in data_list:
            idata = []
            item.update(bag)
            for fid in fields:
                idata.append(item.get(fmap[fid]))
            data.append(idata)
        return data

    def get_user_id(self):
        test = sms_service_AccountService(self.username, self.password, self.token)
        getAccountInfoRequest = {
                "accountFields": ["userId"]
                }
        res = test.getAccountInfo(getAccountInfoRequest)
        userId = res['body']['data'][0]['userId']
        return userId

if __name__=='__main__':
    username = 'ptengine'
    password = 'H7i9H0'
    token = '764cc17aa8f1094457a3016c7161e05d'
    data = KeywordInfoReport(username, password, token)
    print(len(data))
