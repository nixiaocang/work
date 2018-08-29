# coding=utf-8
import os
import json
import time
import numpy as np
import pandas as pd
import requests
from myapp_baidu.main.datasourceservice.apisdk.ApiSDKJsonClient import *
from myapp_baidu.main.datasourceservice.model.Meta import write_data
from myapp_baidu.libs.logger import runtime_logger
from myapp_baidu.config.app_config import load_config

version=os.environ.get('ENV', 'Local')
config_obj = load_config(version)
file_path = config_obj.FILE_PATH
if not os.path.exists(file_path):
    os.makedirs(file_path)





class sms_service_ReportService(ApiSDKJsonClient):

    def __init__(self, username, password, token):
        ApiSDKJsonClient.__init__(self, 'ReportService', username, password, token)
        self.logger = runtime_logger()

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
        self.logger.info("task:%s 开始获取工作表:%s 的数据" % (self.task_id, self.table))
        bag = {}
        for device in (1, 2):
            str_device = '计算机' if device == 1 else '移动'
            getProfessionalReportIdRequest['reportRequestType']['device'] = device
            pres = self.getProfessionalReportId(getProfessionalReportIdRequest)
            self.logger.info("task:%s 开始获取工作表:%s 的%s数据,返回结果为:%s" % (self.task_id, self.table, str_device, json.dumps(pres)))
            if pres['header']['status'] != 0:
                raise Exception('出现异常:%s' % pres['header']['failures'][0]['message'])

            preportId = pres['body']['data'][0]['reportId']
            self.logger.info("task:%s 开始获取工作表:%s 的%s数据,reportId为:%s" % (self.task_id, self.table, str_device, preportId))
            count = 0
            report_param = {'reportId':preportId}
            while count < 5:
                try:
                    psres = self.getReportState(report_param)
                    self.logger.info("task:%s 第%s次开始获取工作表:%s 的%s数据reportId:%s 生成状态,返回结果为:%s" % (self.task_id,count, self.table, str_device, preportId, json.dumps(psres)))
                    if psres['header']['status'] != 0:
                        raise Exception('出现异常:%s' % psres['header']['failures'][0]['message'])
                    pstatus = psres['body']['data'][0]['isGenerated']
                    if pstatus != 3:
                        self.logger.info("task:%s 第%s次获取reportId:%s 生成状态, 此时报告还未生成" % (self.task_id,count,preportId))
                        raise Exception("task:%s 第%s次获取reportId:%s 生成状态, 此时报告还未生成" % (self.task_id,count,preportId))
                    break
                except Exception as e:
                    time.sleep(10)
                    count += 1
                    if count == 5:
                        raise e
            pures = self.getReportFileUrl(report_param)
            self.logger.info("task:%s 开始获取工作表:%s 的%s数据reportId:%s 的下载链接,返回结果为:%s" % (self.task_id,self.table, str_device, preportId, json.dumps(pures)))
            if pures['header']['status'] != 0:
                raise Exception('出现异常:%s' % pures['header']['failures'][0]['message'])
            purl = pures['body']['data'][0]['reportFilePath']
            self.logger.info("task:%s 开始获取工作表:%s 的%s数据下载链接为:%s" % (self.task_id, self.table, str_device, purl))
            res = requests.get(purl)
            filename = "%s/%s_%s.csv"% (file_path, preportId, device)
            with open(filename, "wb") as code:
                code.write(res.content)
            self.logger.info("task:%s 工作表:%s 的%s数据保存为:%s" % (self.task_id, self.table, str_device, filename))
            bag[device] = pd.read_csv(filename,sep='\t', encoding='gbk')
            self.logger.info("task:%s 工作表:%s 的%s数据转化为df完成" % (self.task_id, self.table, str_device))
            bag[device]['设备'] = str_device
        fres = pd.concat([bag[1],bag[2]])
        return fres

    def deal_res(self, fres, dbinfo):
        fres = fres.fillna("-")
        fres['f_source'] = dbinfo['pt_source']
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
        self.logger.info("task:%s 工作表:%s 的数据开始写入数据库" % (self.task_id, self.table))
        write_data(fres, dbinfo, self.table)
        self.logger.info("task:%s 工作表:%s 的数据写入数据库完成,一共%s行" % (self.task_id, self.table, fres.shape[0]))
        return fres.shape[0]
