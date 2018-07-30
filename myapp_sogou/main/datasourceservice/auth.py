from myapp_sogou.libs.exceptions import *
from myapp_sogou.libs.decorators import AuthResponse
from suds.client import Client


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

    def conn(self, username, password, token):
        url = 'http://api.agent.sogou.com/sem/sms/v1/AccountService?wsdl'
        client = Client(url)
        header = client.factory.create('ns0:AuthHeader')
        header.username = username
        header.password = password
        header.token = token
        client.set_options(soapheaders=[header,])
        try:
            res = client.service.getAccountInfo()
            fres = client.last_received()
            code, message = deal_res(fres)
            if str(code) != 'SUCCESS':
                raise Exception(message)
        except Exception as e:
            raise e
        return {'code': code, 'message': message}

def deal_res(res):
    res = str(res)
    if '<ns3:desc>failure' in res:
        code = res.split('<ns3:code>')[1].split('</ns3:code>')[0]
        message = res.split('<ns3:message>')[1].split('</ns3:message>')[0]
    elif '<ns3:desc>success' in res:
        code = 'SUCCESS'
        message = ''
    else:
        code = 'FAIL'
        message = '未知错误'
    return code, message


