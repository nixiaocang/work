from abc import ABCMeta
from abc import abstractmethod

__name__ = "datasourceauth.abc"


class DsAuthRest(metaclass=ABCMeta):
    pass


class DsAuthSaas(DsAuthRest):
    @abstractmethod
    def init_auth(self):
        """
        an abstract method need to be implemented
        """

