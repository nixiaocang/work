from myapp_baidu.libs.exceptions import *
from myapp_baidu.libs.decorators import ServiceResponse
from myapp_baidu.main.datasourceservice.api.PlanReport import PlanReport
from myapp_baidu.main.datasourceservice.api.KeywordReport import KeywordReport
from myapp_baidu.main.datasourceservice.api.KeywordInfoReport import KeywordInfoReport
from myapp_baidu.main.datasourceservice.api.CityReport import CityReport
from myapp_baidu.main.datasourceservice.api.CreativeReport import CreativeReport
from myapp_baidu.main.datasourceservice.api.HistoryReport import HistoryReport
from myapp_baidu.main.datasourceservice.api.SearchReport import SearchReport
from myapp_baidu.main.datasourceservice.model.Meta import DBModel
import datetime
import random
import json
import time
import traceback
from myapp_baidu.libs.logger import runtime_logger


class_map = {
        "t_campaign_report":PlanReport,
        "t_keyword_report":KeywordReport,
        "t_keyword":KeywordInfoReport,
        "t_region_report":CityReport,
        "t_creative":CreativeReport,
        "t_billing_report":HistoryReport,
        "t_search":SearchReport
        }

class DatasourceService(object):

    def __init__(self, token_process_info):
        self._token_process_info = token_process_info
        self._credentials = self._get_credentials(token_process_info)
        super(DatasourceService, self).__init__()

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, val):
        self._credentials = val

    @property
    def token_process_info(self):
        return self._token_process_info

    @token_process_info.setter
    def token_process_info(self, val):
        self._token_process_info = val

    def _get_credentials(self, *args, **kwargs):

        """
        obtain the valid token structure.
        You could just convert 'token_process_info' into a structure that meets the datasource api's requirment
        without checking its validity, leaving this job to the subsequent each api calling. OR you may check the
        token validity in this method, if you do so, you may refresh the token and update the token_process_info
        when the token is invalid.
        """
        instanceTokenData = args[0]
        return instanceTokenData

    @ServiceResponse(token_process_info)
    def get_profiles(self):
        return self.read_profile_list()

    @ServiceResponse
    def get_reports(self):
        return self.read_report_list()

    @ServiceResponse
    def get_metrics(self, *args, **kwargs):
        return self.read_metrics(*args, **kwargs)

    @ServiceResponse
    def get_dimensions(self, *args, **kwargs):
        return self.read_dimensions(*args, **kwargs)

    @ServiceResponse
    def get_data(self, *args, **kwargs):
        return self.read_data(*args, **kwargs)

    @ServiceResponse
    def get_filter_values(self, *args, **kwargs):
        return self.read_filter_values(*args, **kwargs)

    def read_profile_list(self, *args, **kwargs):
        raise NotImplementedError

    def read_report_list(self, *args, **kwargs):
        raise NotImplementedError

    def read_metrics(self, *args, **kwargs):
        raise NotImplementedError

    def read_dimensions(self, *args, **kwargs):
        raise NotImplementedError

    def read_data(self, data_request_param):
        username = self._credentials.get("username")
        password = self._credentials.get("password")
        token = self._credentials.get("token")
        if not (username and password and token):
            raise Exception('缺少用户信息参数')
        yesterday = datetime.datetime.today()-datetime.timedelta(days=1)
        yesterday = str(yesterday)[:10]
        startDate = data_request_param["dateRange"].get('startDate', yesterday)
        endDate = data_request_param["dateRange"].get('endDate', yesterday)
        if endDate < startDate or endDate > yesterday:
            raise Exception('日期不合法')
        metricList = data_request_param.get('metricList', [])
        obj = class_map.get(data_request_param["reportId"])
        if not obj:
            raise Exception('不支持的报告类型')
        try:
            data = obj(username, password, token).get_data(startDate, endDate, metricList)
        except Exception as e:
            print(e)
            raise e
        res = {
                "tokenProgressInfo": self._token_process_info,
                "dataList":data
                }
        return res


    def read_filter_values(self, data_request_param):
        raise NotImplementedError

    def get_report_data(self, data_request_param):
        rlog = runtime_logger()
        code = "SUCCESS"
        username = self._credentials.get("account")
        password = self._credentials.get("password")
        token = self._credentials.get("token")
        if not (username and password and token):
            rlog.error('缺少用户信息参数')
            raise Exception('缺少用户信息参数')
        yesterday = datetime.datetime.today()-datetime.timedelta(days=1)
        yesterday = str(yesterday)[:10]
        startDate = data_request_param.get('pt_data_from_date', yesterday)
        endDate = data_request_param.get('pt_data_to_date', yesterday)
        retry = data_request_param.get('pt_retry_times')
        interval = data_request_param.get('pt_retry_interval')
        if not retry or not interval:
            rlog.error('缺少重试信息')
            raise Exception('缺少重试信息')
        f_task_id = random.randint(1,1000000000)
        data_request_param['f_task_id'] = f_task_id
        # 插入所需要的数据
        db_helper = DBModel(data_request_param)
        rlog.info("task: %s 开始执行" % f_task_id)
        for report_type in data_request_param['pt_db_table']:
            count = 0
            while count < retry:
                try:
                    data = {
                        'f_table':report_type,
                        'f_account':username,
                        'f_tried_time':count+1
                        }
                    rlog.info("task: %s实例化对应的报告对象" % f_task_id)
                    obj = class_map.get(report_type)
                    rlog.info("task: %s在t_task_trace插入数据" % f_task_id)
                    db_helper.insert(data)
                    rlog.info("task: %s开始获取%s的数据" % (f_task_id, report_type))
                    number = obj(username, password, token).get_data(startDate, endDate, data_request_param)
                    rlog.info("task: %s获取%s的数据共%s条,并开始更新t_task_trace" % (f_task_id, report_type, number))
                    db_helper.update_t_task_trace(number, report_type)
                    rlog.info("task: %s获取%s的记录更新完毕" % (f_task_id, report_type))
                    break
                except Exception as e:
                    time.sleep(interval)
                    count += 1
                    rlog.error("task: %s获取%s的数据时出现错误:%s" % (f_task_id, report_type, str(e)))
                    runtime_logger().error("task:%s, %s" % (f_task_id, traceback.format_exc().replace("\n", "####")))
                    code = "FAIL"
                    data['f_error_msg'] = str(e)
                    data['f_tried_time'] = count
                    db_helper.insert(data)
        rlog.info("task: %s 开始更新t_conf" % f_task_id)
        db_helper.update_t_conf()
        rlog.info("task: %s 执行完毕" % f_task_id)
        del db_helper
        return {"code":code, 'pt_code': 'SUCCESS' if code=='SUCCESS' else 'FAILURE'}
