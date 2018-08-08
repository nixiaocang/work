from myapp_baidu.libs.exceptions import *
from myapp_baidu.libs.decorators import ServiceResponse
from myapp_baidu.main.datasourceservice.api.PlanReport import PlanReport
from myapp_baidu.main.datasourceservice.api.KeywordReport import KeywordReport
from myapp_baidu.main.datasourceservice.api.KeywordInfoReport import KeywordInfoReport
from myapp_baidu.main.datasourceservice.api.CityReport import CityReport
from myapp_baidu.main.datasourceservice.api.CreativeReport import CreativeReport
from myapp_baidu.main.datasourceservice.api.HistoryReport import HistoryReport
from myapp_baidu.main.datasourceservice.api.SearchReport import SearchReport
import datetime
import json


class_map = {
        "plan":PlanReport,
        "keyword":KeywordReport,
        "keywordinfo":KeywordInfoReport,
        "city":CityReport,
        "creative":CreativeReport,
        "history":HistoryReport,
        "search":SearchReport
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
        print(args)
        instanceTokenData = args[0]["instanceTokenData"]
        info = json.loads(instanceTokenData)
        return info

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

    def get_plan_data(self, data_request_param):
        username = data_request_param.get('username')
        password = data_request_param.get('password')
        token = data_request_param.get('token')
        if not (username and password and token):
            raise Exception('缺少用户信息参数')
        yesterday = datetime.datetime.today()-datetime.timedelta(days=1)
        yesterday = str(yesterday)[:10]
        startDate = data_request_param.get('startDate', yesterday)
        endDate = data_request_param.get('endDate', yesterday)
        print(data_request_param)
        if endDate < startDate:
            raise Exception('日期不合法')
        try:
            data = PlanReport(username, password, token).get_data(startDate, endDate)
        except Exception as e:
            print(e)
            raise e
        return {'code':'SUCCESS', 'data':data}
