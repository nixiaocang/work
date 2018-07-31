from myapp_baidu.libs.exceptions import *
from myapp_baidu.libs.decorators import ServiceResponse
from myapp_baidu.main.datasourceservice.api.PlanReport import PlanReport
import datetime


class DatasourceService(object):

    def __init__(self, token_process_info):
        self._token_process_info = token_process_info
        #self._credentials = self._get_credentials(token_process_info)
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
        raise NotImplementedError

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
        raise NotImplementedError

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
