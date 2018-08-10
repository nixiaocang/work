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
        self.table = 't_campaign_report'
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
                "推广计划ID":"f_campaign_id",
                "推广计划":"f_campaign",
                #"转化(网页)":"trans",
                #"小时":"hour",
                }

    def get_data(self, startDate, endDate, dbinfo):
        # get report id
        self.task_id = dbinfo['f_task_id']
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
        fres = self.get_report_df(getProfessionalReportIdRequest)
        if fres.empty:
            return 0
        fres['点击率'] = pd.to_numeric(fres['点击率'].str.split('%',expand=True)[0])/100
        count = self.deal_res(fres, dbinfo)
        return count

