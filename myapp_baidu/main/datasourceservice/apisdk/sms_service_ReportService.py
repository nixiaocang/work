# coding=utf-8
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
