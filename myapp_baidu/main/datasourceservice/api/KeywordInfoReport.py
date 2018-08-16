#coding:utf-8
import time
import json
import numpy as np
import pandas as pd
import requests
from myapp_baidu.main.datasourceservice.apisdk.sms_service_ReportService import sms_service_ReportService
from myapp_baidu.main.datasourceservice.apisdk.sms_service_KeywordService import sms_service_KeywordService
from myapp_baidu.main.datasourceservice.apisdk.sms_service_AccountService import sms_service_AccountService

class KeywordInfoReport(sms_service_ReportService):
    def __init__(self, username, password, token):
        self.username = username
        self.password = password
        self.token = token
        self.table = 't_keyword'
        self.report_obj = sms_service_KeywordService(username, password, token)
        super(KeywordInfoReport, self).__init__(username, password, token)
        self.fmap = {
                "f_source":"f_source",
                "f_company_id":"f_company_id",
                "f_email":"f_email",
                "账户":"f_account",
                "日期":"f_date",
                "账户ID":"f_account_id",
                "设备":"f_device",
                "campaignId":"f_campaign_id",
                "f_campaign":"f_campaign",
                "adgroupId":"f_set_id",
                "f_set":"f_set",
                "keywordId":"f_keyword_id",
                "keyword":"f_keyword",
                "matchType":"f_matched_type",
                "price":"f_keyword_offer_price",
                "pcQuality":"f_keyword_quality",
                "pcDestinationUrl":"f_pc_url",
                "mobileDestinationUrl":"f_mobile_url",
                }

    def get_data(self, startDate, endDate, dbinfo):
        self.task_id = dbinfo['f_task_id']
        account_id = self.get_user_id()
        getProfessionalReportIdRequest = {
                'reportRequestType':{
                    'performanceData':['cost','cpc','click','impression','ctr','cpm','conversion', 'position'],
                    'startDate': startDate,
                    'endDate': endDate,
                    'levelOfDetails':11,
                    'unitOfTime':5,
                    'reportType':14
                                }
                            }
        df =  self.get_report_df(getProfessionalReportIdRequest)
        if df.empty:
            return 0
        bag = {}
        for device in (1, 2):
            str_device = '计算机' if device == 1 else '移动'
            temp_df = df[df['设备']==str_device]
            bag[device] = self.get_keyword_info(temp_df)
            bag[device]['设备'] = str_device
        df1, df2 = bag[1], bag[2]
        fres = pd.concat([df1,df2])
        fres['日期'] = endDate
        fres['账户ID'] = account_id
        fres['账户'] = self.username
        count = self.deal_res(fres, dbinfo)
        return count


    def get_keyword_info(self, df):
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
            tres = self.report_obj.getWord(getWordRequest)
            data_list += tres['body']['data']
        fdf = pd.read_json(json.dumps(data_list))
        return fdf

    def get_user_id(self):
        test = sms_service_AccountService(self.username, self.password, self.token)
        getAccountInfoRequest = {
                "accountFields": ["userId"]
                }
        res = test.getAccountInfo(getAccountInfoRequest)
        if res['header']['status'] != 0:
            raise Exception('%s' % res['header']['failures'][0]['message'])
        userId = res['body']['data'][0]['userId']
        return userId

if __name__=='__main__':
    username = 'ptengine'
    password = 'H7i9H0'
    token = '764cc17aa8f1094457a3016c7161e05d'
    data = KeywordInfoReport(username, password, token)
    print(len(data))
