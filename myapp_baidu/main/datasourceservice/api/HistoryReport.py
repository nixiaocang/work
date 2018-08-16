#coding:utf-8
import time
import json
import numpy as np
import pandas as pd
import requests
from myapp_baidu.main.datasourceservice.apisdk.sms_service_ReportService import sms_service_ReportService

class HistoryReport(sms_service_ReportService):
    def __init__(self, username, password, token):
        super(HistoryReport, self).__init__(username, password, token)
        self.table='t_billing_report'
        self.fmap = {
                "f_source":"f_source",
                "f_company_id":"f_company_id",
                "f_email":"f_email",
                "账户":"f_account",
                "日期":"f_date",
                "国家":"f_country",
                "地域ID":"f_subdivition_id",
                "地域":"f_subdivition",
                "城市ID":"f_city_id",
                "城市":"f_city",
                "账户ID":"f_account_id",
                "推广计划ID":"f_campaign_id",
                "推广计划":"f_campaign",
                "推广单元ID":"f_set_id",
                "推广单元":"f_set",
                "创意ID":"f_creative_id",
                "创意标题":"f_creative",
                "关键词keywordID":"f_kkeyword_id",
                "关键词":"f_keyword",
                "首页第1~4位展现":"f_impr_count",
                "第1位展现":"f_impr1",
                "第2位展现":"f_impr2",
                "第3位展现":"f_impr3",
                "第4位展现":"f_impr4",
                "f_impr_top13":"f_impr_top13",
                "f_impr_top_rate13":"f_impr_top_rate13",
                "f_impr_f_impr_top_rate13":"f_impr_f_impr_top_rate13",
                "f_impr_left18":"f_impr_left18",
                "设备":"f_device",
                }

    def get_data(self, startDate, endDate, dbinfo):
        self.task_id = dbinfo['f_task_id']
        getProfessionalReportIdRequest = {
                'reportRequestType':{
                    'performanceData':['rank1shows','rank2shows','rank3shows','rank4shows','rank1to4shows'],
                    'startDate': startDate,
                    'endDate': endDate,
                    'levelOfDetails':11,
                    'unitOfTime':5,
                    'reportType':38
                                }
                            }
        fres = self.get_report_df(getProfessionalReportIdRequest)
        if fres.empty:
            return 0
        count = self.deal_res(fres, dbinfo)
        return count
