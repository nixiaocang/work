# coding=utf-8
import time
import numpy as np
import pandas as pd
import requests
from myapp_baidu.main.datasourceservice.apisdk.ApiSDKJsonClient import *
from myapp_baidu.main.datasourceservice.model.Meta import write_data


class sms_service_ReportService(ApiSDKJsonClient):

    def __init__(self, username, password, token):
        ApiSDKJsonClient.__init__(self, 'ReportService', username, password, token)

    def getRealTimeQueryData(self, getRealTimeQueryDataRequest=None):
        return self.execute('getRealTimeQueryData', getRealTimeQueryDataRequest)

    def getRealTimePairData(self, getRealTimePairDataRequest=None):
        return self.execute('getRealTimePairData', getRealTimePairDataRequest)

    def getProfessionalReportId(self, getProfessionalReportIdRequest=None):
        return self.execute('getProfessionalReportId', getProfessionalReportIdRequest)

    def getReportState(self, getReportStateRequest=None):
        return self.execute('getReportState', getReportStateRequest)

    def getReportFileUrl(self, getReportFileUrlRequest=None):
        return self.execute('getReportFileUrl', getReportFileUrlRequest)

    def getRealTimeData(self, getRealTimeDataRequest=None):
        return self.execute('getRealTimeData', getRealTimeDataRequest)

    def get_report_df(self, getProfessionalReportIdRequest):
        bag = {}
        for device in (1, 2):
            str_device = '计算机' if device == 1 else '移动'
            getProfessionalReportIdRequest['reportRequestType']['device'] = device
            pres = self.getProfessionalReportId(getProfessionalReportIdRequest)
            preportId = pres['body']['data'][0]['reportId']
            count = 0
            report_param = {'reportId':preportId}
            while count < 5:
                try:
                    psres = self.getReportState(report_param)
                    pstatus = psres['body']['data'][0]['isGenerated']
                    if pstatus != 3:
                        raise Exception('报告还未生成')
                    break
                except Exception as e:
                    time.sleep(10)
                    count += 1
                    if count == 5:
                        raise e
            pures = self.getReportFileUrl(report_param)
            purl = pures['body']['data'][0]['reportFilePath']
            res = requests.get(purl)
            with open("/tmp/%s_%s.csv" % (preportId, device), "wb") as code:
                code.write(res.content)
            bag[device] = pd.read_csv('/tmp/%s_%s.csv' % (preportId, device),sep='\t', encoding='gbk')
            bag[device]['设备'] = str_device
        fres = pd.concat([bag[1],bag[2]])
        return fres

    def deal_res(self, fres, dbinfo):
        fres['f_source'] = "baidu"
        fres['f_company_id'] = dbinfo['pt_company_id']
        fres['f_email'] = dbinfo['pt_email']
        cols = [col for col in fres]
        new_cols = []
        for col in cols:
            if col not in self.fmap.keys():
                del fres[col]
            else:
                new_cols.append(self.fmap[col])
        fres.columns = new_cols
        write_data(fres, dbinfo, self.table)
        return fres.shape[0]
