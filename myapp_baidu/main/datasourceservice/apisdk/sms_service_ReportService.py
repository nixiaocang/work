#coding=utf-8
from ApiSDKJsonClient import *


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



if __name__=='__main__':
    username = 'baidu-罗技2113872'
    password = 'Bcda1234'
    token = '3ac60d07196b5196c2617cc8c6243140'
    test = sms_service_ReportService(username, password, token)
    getProfessionalReportIdRequest = {
            'reportRequestType':{
            'performanceData':['cost','cpc','click','impression','ctr','cpm'],
            'startDate':'2014-04-01',
            'endDate':'2014-04-03',
            'levelOfDetails':3,
            'unitOfTime':7,
            'reportType':10
            }
            }
    #res = test.getProfessionalReportId(getProfessionalReportIdRequest)
    getReportStateRequest = {
            'reportId':'9b09b5404dc2883cd76a5c438b3bf3c3'
            }

    getReportFileUrlRequest = {
            'reportId':'9b09b5404dc2883cd76a5c438b3bf3c3'
            }
    res = test.getReportFileUrl(getReportFileUrlRequest)
    print res

