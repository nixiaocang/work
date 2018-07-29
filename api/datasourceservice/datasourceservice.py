from abc import ABCMeta, abstractmethod
from typing import Any, List, Dict

from api.datasourceobject import DataRequestSaasParam, DataRequestFileParam
from api.datasourceobject import FilterData, FilterValueParam
from api.datasourceobject import DsField, TimeField

__name__ = "dsservicerest.abc"


class DsServiceRest(metaclass=ABCMeta):
    __slots__ = ()


    @abstractmethod
    def get_widget_editor_config(self, widget_step_config_list: list = None) -> Dict[Any, Any]:
        """
        an abstract method need to be implemented
        """

    @abstractmethod
    def read_profile_list(self, instance_id: str = None) -> List[Any]:
        """
        an abstract method need to be implemented
        """

    @abstractmethod
    def read_report_list(self, instance_id: str = None, profile_id: str = None) -> List[Any]:
        """
        an abstract method need to be implemented
        """

    @abstractmethod
    def read_metrics(self, instance_id: str = None, profile_id: str = None, report_id: str = None) -> List[DsField]:
        """
        an abstract method need to be implemented
        """

    @abstractmethod
    def read_dimensions(self, instance_id: str = None, profile_id: str = None, report_id: str = None) -> List[DsField]:
        """
        an abstract method need to be implemented
        """

    @abstractmethod
    def read_filter_values(self, filter_value_param: FilterValueParam = None) -> List[FilterData]:
        """
        an abstract method need to be implemented
        """

    @abstractmethod
    def read_time_fields_list(self, instance_id: str = None, profile_id: str = None) -> List[TimeField]:
        """
        an abstract method need to be implemented
        """

    @abstractmethod
    def get_excel_sheets(self, instance_id: str = None, coordinate: str = None) -> List[Any]:
        """
        an abstract method need to be implemented
        """

    @abstractmethod
    def get_saas_data(self, data_request_param: DataRequestSaasParam = None, callback: str = None):
        """
        an abstract method need to be implemented
        """

    @abstractmethod
    def get_file_data(self, data_request_param: DataRequestFileParam = None, callback: str = None):
        """
        an abstract method need to be implemented
        """


class DsServiceSaas(metaclass=DsServiceRest):

    def get_file_data(self, data_request_file_param, callback):
        raise NotImplementedError

    def get_excel_sheets(self, instance_id, coordinate):
        raise NotImplementedError


class DsServiceDB(metaclass=DsServiceRest):

    def get_saas_data(self, data_request_param, callback):
        raise NotImplementedError

    def get_file_data(self, data_request_file_param, callback):
        raise NotImplementedError

    def get_excel_sheets(self, instance_id, coordinate):
        raise NotImplementedError


class DsServiceFile(metaclass=DsServiceRest):

    def read_filter_values(self, filter_value_param):
        raise NotImplementedError

    def read_dimensions(self, instance_id, profile_id, report_id):
        raise NotImplementedError

    def read_metrics(self, instance_id, profile_id, report_id):
        raise NotImplementedError

    def get_saas_data(self, data_request_param, callback):
        raise NotImplementedError


class DsServiceForm(metaclass=DsServiceRest):
    pass

