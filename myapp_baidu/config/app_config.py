import traceback
import sys


def load_config(version):
    """LOAD CONFIG FOR FLASK"""
    try:
        module = sys.modules[__name__]
        klass_name = "Config{}".format(version.capitalize())
        klass = getattr(module, klass_name)
        return klass
    except Exception:
        raise ValueError(traceback.format_exc())


class Config(object):
    APP_NAME = 'baidu'


class ConfigProduct(Config):
    """ eurake-service related configuration """
    EURAKE = True
    PORT = '8700'
    IP_ADDR = '192.168.3.141'
    HOSTNAME = '192.168.3.141'
    EUREKA_URL = 'http://ptmind:Ptmind123qwe@192.168.2.161:8010/'
    # INSTANCE_ID = ''
    # HEALTH_CHECK_URL = ''
    # STATUS_PAGE_URL = ''

    """ data-manager-service related configuration """
    AUTH_CALLBACK_URL = 'https://test.auth.ptone.com/datadeck-app-datasource/py-datasource-service-google-search-console/auth/tokenCallback'

    """ datasource-Oauth2-service related configuration """
    # CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), 'client_secret_oauth.json')
    # SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly", "https://www.googleapis.com/auth/userinfo.email"]

    """ datasource-data-service related configuration """
    # API_SERVICE_NAME = 'webmasters'
    # API_VERSION = 'v3'

    """ database config """
    DATABASE = 'dm_shangwutong_dev'
    USER = 'dm_shangwutong_dev_user'
    PASSWORD = '12#$56&*YUhj'
    HOST = '221.122.89.102'
    PORT = "5432"


class ConfigStaging(Config):
    """ eurake-service related configuration """
    EURAKE = True
    PORT = '8700'
    IP_ADDR = '192.168.3.141'
    HOSTNAME = '192.168.3.141'
    EUREKA_URL = 'http://ptmind:Ptmind123qwe@192.168.2.161:8010/'
    # INSTANCE_ID = ''
    # HEALTH_CHECK_URL = ''
    # STATUS_PAGE_URL = ''

    """ data-manager-service related configuration """
    AUTH_CALLBACK_URL = 'https://test.auth.ptone.com/datadeck-app-datasource/py-datasource-service-google-search-console/auth/tokenCallback'

    """ datasource-Oauth2-service related configuration """
    # CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), 'client_secret_oauth.json')
    # SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly", "https://www.googleapis.com/auth/userinfo.email"]

    """ datasource-data-service related configuration """
    # API_SERVICE_NAME = 'webmasters'
    # API_VERSION = 'v3'

    """ database config """
    DATABASE = 'dm_shangwutong_dev'
    USER = 'dm_shangwutong_dev_user'
    PASSWORD = '12#$56&*YUhj'
    HOST = '221.122.89.102'
    PORT = "5432"


class ConfigDevelop(Config):
    """ eurake-service related configuration """
    EURAKE = False
    PORT = '8700'
    IP_ADDR = '192.168.3.141'
    HOSTNAME = '192.168.3.141'
    EUREKA_URL = 'http://ptmind:Ptmind123qwe@192.168.2.161:8010/'
    # INSTANCE_ID = ''
    # HEALTH_CHECK_URL = ''
    # STATUS_PAGE_URL = ''

    """ data-manager-service related configuration """
    AUTH_CALLBACK_URL = 'https://test.auth.ptone.com/datadeck-app-datasource/py-datasource-service-google-search-console/auth/tokenCallback'

    """ datasource-Oauth2-service related configuration """
    # CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), 'client_secret_oauth.json')
    # SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly", "https://www.googleapis.com/auth/userinfo.email"]

    """ datasource-data-service related configuration """
    # API_SERVICE_NAME = 'webmasters'
    # API_VERSION = 'v3'

    """ database config """
    DATABASE = 'dm_shangwutong_dev'
    USER = 'dm_shangwutong_dev_user'
    PASSWORD = '12#$56&*YUhj'
    HOST = '221.122.89.102'
    PORT = "5432"


class ConfigLocal(Config):
    """ eurake-service related configuration """
    EURAKE = False
    PORT = '8700'
    IP_ADDR = '115.28.9.49' #'192.168.3.141'
    HOSTNAME = '115.28.9.49' #'192.168.3.141'
    EUREKA_URL = 'http://ptmind:Ptmind123qwe@testsource.datadeck.cn'
    # INSTANCE_ID = ''
    # HEALTH_CHECK_URL = ''
    # STATUS_PAGE_URL = ''

    """ data-manager-service related configuration """
    AUTH_CALLBACK_URL = 'https://test.auth.ptone.com/datadeck-app-datasource/py-datasource-service-google-search-console/auth/tokenCallback'

    """ datasource-Oauth2-service related configuration """
    # CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), 'client_secret_oauth.json')
    # SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly", "https://www.googleapis.com/auth/userinfo.email"]

    """ datasource-data-service related configuration """
    # API_SERVICE_NAME = 'webmasters'
    # API_VERSION = 'v3'

    """ database config """
    DATABASE = 'dm_shangwutong_dev'
    USER = 'dm_shangwutong_dev_user'
    PASSWORD = '12#$56&*YUhj'
    HOST = '221.122.89.102'
    PORT = "5432"
