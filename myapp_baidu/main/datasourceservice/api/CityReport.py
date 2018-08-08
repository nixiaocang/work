#coding:utf-8
import time
import json
import numpy as np
import pandas as pd
import requests
from myapp_baidu.main.datasourceservice.apisdk.sms_service_ReportService import sms_service_ReportService

class CityReport(sms_service_ReportService):
    def __init__(self, username, password, token):
        super(CityReport, self).__init__(username, password, token)

    def get_data(self, startDate, endDate, metricList):
        # get report id
        getProfessionalReportIdRequest = {
                'reportRequestType':{
                    'performanceData':['cost','cpc','click','impression','ctr','cpm','conversion', 'position'],
                    'startDate': startDate,
                    'endDate': startDate,
                    'levelOfDetails':2,
                    'unitOfTime':5,
                    'reportType':5
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
            df1['推广渠道'] = '百度推广'
        if not df2.empty:
            df2['设备'] = '移动'
            df2['推广渠道'] = '百度推广'
        fres = pd.concat([df1,df2])
        fres['点击率'] = pd.to_numeric(fres['点击率'].str.split('%',expand=True)[0])/100
        data = self.deal_data(fres, metricList)
        print(len(data))
        return data

    def deal_data(self, fres, metricList):
        fields = [item['id'] for item in metricList]
        clos  =[column for column in fres]
        print(fields)
        print(clos)
        if fields:
            for k in clos:
                if k not in fields:
                    del fres[k]
            fres = fres.ix[:,fields]
        data = np.array(fres).tolist()
        return data

if __name__=='__main__':
    username = 'ptengine'
    password = 'H7i9H0'
    token = '764cc17aa8f1094457a3016c7161e05d'
    data = CityReport(username, password, token)
    print(len(data))
