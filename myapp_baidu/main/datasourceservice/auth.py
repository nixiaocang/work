from myapp_baidu.libs.exceptions import *
from myapp_baidu.libs.decorators import AuthResponse


class DatasourceAuth(object):

    def __init__(self, state):
        self._state = state
        super(DatasourceAuth, self).__init__()

    @property
    def state(self):
        return self._state

    @AuthResponse
    def oauth_init(self):
        try:
            return {
                "redirectUrl": ""
                , "uniqueCode": self.state
            }
        except Exception:
            raise AuthURLError('Retrieving Authorization URL failed.')

    def authorization_url_generate(self):
        raise NotImplementedError

    @AuthResponse
    def oauth_callback(self, *args, **kwargs):
        try:
            return {
                "accountTokenData": ""
                , "instanceTokenData": ""
                , 'uniqueId': ""
                , 'account': ""
                , 'uniqueCode': self.state
            }
        except Exception:
            raise OAuthTokenError('Authorization token exchanging failed.')

    @staticmethod
    def credentials_authenticate(authorization_response_url):
        """
        exchange token with code in authorization_response_url
        :param authorization_response_url: str
        :return: credentials [object or dict]
        """
        raise NotImplementedError

    @staticmethod
    def credentials_account_retrieve(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return: customer's datasource account (usually an email) [object or str]
        """
        return NotImplementedError

    @staticmethod
    def revoke(*args, **kwargs):
        """
        release token
        :param credentials:
        :return: Boolean
        """
        raise NotImplementedError