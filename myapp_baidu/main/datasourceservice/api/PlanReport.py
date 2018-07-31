#coding:utf-8
import time
import json
import pandas as pd
from myapp_baidu.main.datasourceservice.apisdk.sms_service_ReportService import sms_service_ReportService

class PlanReport(sms_service_ReportService):
    def __init__(self, username, password, token):
        super(PlanReport, self).__init__(username, password, token)

    def get_data(self, startDate, endDate):
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
        for device in (1, 2):
            getProfessionalReportIdRequest['device'] = device
            pres = test.getProfessionalReportId(getProfessionalReportIdRequest)
            preportId = pres['body']['data'][0]['reportId']
            count = 0
            report_param = {
                'reportId':preportId
                }
            while count < 3:
                psres = test.getReportState(report_param)
                pstatus = psres['body']['data'][0]['isGenerated']
                if pstatus != 3:
                    time.sleep(5)
                    count += 1
                    if count == 3:
                        raise Exception('报告获取失败')
                else:
                    break
            pures = test.getReportFileUrl(report_param)
            purl = pures['body']['data'][0]['reportFilePath']
            res = requests.get(url)
            with open("/tmp/%s_%s.csv" % (reportId, device), "wb") as code:
                code.write(res.content)
        df1 = pd.read_csv('/tmp/%s_1.csv' % reportId, sep='\t', encoding='gbk')
        df1['设备'] = '计算机'
        df1['推广渠道'] = '百度推广'
        df2 = pd.read_csv('/tmp/%s_2.csv' % reportId, sep='\t', encoding='gbk')
        df2['设备'] = '移动'
        df2['推广渠道'] = '百度推广'
        fres = pd.concat(df1,df2)
        fjosn = pd.to_json(orient='records')
        data = json.loads(fjosn)
        return data

if __name__=='__main__':
    username = 'ptengine'
    password = 'H7i9H0'
    token = '764cc17aa8f1094457a3016c7161e05d'
    data = PlanReport(username, password, token)
    print len(data)
