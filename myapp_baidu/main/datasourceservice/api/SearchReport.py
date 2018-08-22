#coding:utf-8
import time
import json
import numpy as np
import pandas as pd
import requests
from myapp_baidu.main.datasourceservice.apisdk.sms_service_ReportService import sms_service_ReportService

class SearchReport(sms_service_ReportService):
    def __init__(self, username, password, token):
        super(SearchReport, self).__init__(username, password, token)
        self.table = 't_search'
        self.fmap = {
                "f_source":"f_source",
                "f_company_id":"f_company_id",
                "f_email":"f_email",
                "账户":"f_account",
                "日期":"f_date",
                "账户ID":"f_account_id",
                "推广计划ID":"f_campaign_id",
                "推广计划":"f_campaign",
                "推广单元ID":"f_set_id",
                "推广单元":"f_set",
                "创意ID":"f_creative_id",
                "创意标题":"f_creative",
                "关键词keywordID":"f_kkeyword_id",
                "关键词ID":"f_keyword_id",
                "关键词":"f_keyword",
                "显示URL":"f_url",
                "搜索词":"f_search_word",
                "展现量":"f_impression_count",
                "点击量":"f_click_count",
                "消费":"f_cost",
                "点击率":"f_cpc_rate",
                "搜索引擎":"f_search_engine",
                "精确匹配扩展(地域词扩展)触发":"f_accurate_trigger",
                "设备":"f_device",
                "创意描述1":"f_creative_memo1",
                "创意描述2":"f_creative_memo2",
                }

    def get_data(self, startDate, endDate, dbinfo):
        self.task_id = dbinfo['f_task_id']
        # get report id
        getProfessionalReportIdRequest = {
                'reportRequestType':{
                    'performanceData':['cost','click','impression','ctr'],
                    'startDate': startDate,
                    'endDate': endDate,
                    'levelOfDetails':12,
                    'unitOfTime':5,
                    'reportType':6
                                }
                            }
        fres = self.get_report_df(getProfessionalReportIdRequest)
        if fres.empty:
            return 0
        fres['点击率'] = pd.to_numeric(fres['点击率'].str.split('%',expand=True)[0])/100
        count = self.deal_res(fres, dbinfo)
        return count

