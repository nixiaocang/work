#coding:utf-8
import time
import json
import numpy as np
import pandas as pd
import requests
from myapp_baidu.main.datasourceservice.apisdk.sms_service_ReportService import sms_service_ReportService
from myapp_baidu.main.datasourceservice.model.Meta import write_data

class PlanReport(sms_service_ReportService):
    def __init__(self, username, password, token):
        super(PlanReport, self).__init__(username, password, token)
        self.fmap = {
                "f_source":"f_source",
                "f_company_id":"f_company_id",
                "f_email":"f_email",
                "账户":"f_account",
                "日期":"f_date",
                "账户ID":"f_account_id",
                "展现量":"f_impression_count",
                "点击量":"f_click_count",
                "消费":"f_cost",
                "点击率":"f_cpc_rate",
                "平均点击价格":"f_cpc_avg_price",
                "千次展现消费":"f_k_cpm_cost",
                "设备":"f_device",
                #"推广计划ID":"f_campaign_id",
                #"推广计划":"f_campaign",
                #"转化(网页)":"trans",
                #"小时":"hour",
                }

    def get_data(self, startDate, endDate, dbinfo):
        # get report id
        getProfessionalReportIdRequest = {
                'reportRequestType':{
                    'performanceData':['cost','cpc','click','impression','ctr','cpm','conversion'],
                    'startDate': startDate,
                    'endDate': startDate,
                    'levelOfDetails':3,
                    'unitOfTime':7,
                    'reportType':10
                                }
                            }
        # 分设备获取
        # device = 1 PC  device=2 移动
        bag = {}
        for device in (1, 2):
            getProfessionalReportIdRequest['device'] = device
            pres = self.getProfessionalReportId(getProfessionalReportIdRequest)
            preportId = pres['body']['data'][0]['reportId']
            count = 0
            report_param = {
                'reportId':preportId
                }
            while count < 3:
                psres = self.getReportState(report_param)
                pstatus = psres['body']['data'][0]['isGenerated']
                if pstatus != 3:
                    time.sleep(5)
                    count += 1
                    if count == 3:
                        raise Exception('报告获取失败')
                else:
                    break
            pures = self.getReportFileUrl(report_param)
            purl = pures['body']['data'][0]['reportFilePath']
            res = requests.get(purl)
            with open("/tmp/%s_%s.csv" % (preportId, device), "wb") as code:
                code.write(res.content)
            bag[device] = pd.read_csv('/tmp/%s_%s.csv' % (preportId, device), sep='\t', encoding='gbk')

        df1 = bag[1]
        df2 = bag[2]
        if not df1.empty:
            df1['设备'] = '计算机'
        if not df2.empty:
            df2['设备'] = '移动'
        fres = pd.concat([df1,df2])
        if fres.empty:
            return 0
        fres['点击率'] = pd.to_numeric(fres['点击率'].str.split('%',expand=True)[0])/100
        fres['f_source'] = "baidu"
        fres['f_company_id'] = dbinfo['pt_company_id']
        fres['f_email'] = dbinfo['pt_email']
        cols =  [col for col in fres]
        new_cols = []
        for col in cols:
            if col not in self.fmap.keys():
                del fres[col]
            else:
                new_cols.append(self.fmap[col])
        print([col for col in fres])
        print(new_cols)
        print("********")
        fres.columns = new_cols
        write_data(fres, dbinfo, 't_campaign_report')
        return fres.shape[0]

