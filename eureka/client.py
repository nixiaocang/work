"""
Eureka Client Library.

Eureka is a service discovery and registration service
built by Netflix and used in the Spring Cloud stack.
"""
import requests
import atexit
import enum
import uuid
import time
from typing import Optional, Dict, Any
from threading import Thread

try:
    import ujson as json
except ImportError:
    import json

from json import JSONDecodeError

_SESSION = requests.Session()
_SESSION.headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}
atexit.register(_SESSION.close)


class StatusType(enum.Enum):
    """
    Available status types with eureka, these can be used
    for any `EurekaClient.register` call to pl
    """
    UP = 'UP'
    DOWN = 'DOWN'
    STARTING = 'STARTING'
    OUT_OF_SERVICE = 'OUT_OF_SERVICE'
    UNKNOWN = 'UNKNOWN'


class EurekaClient:
    __slots__ = ('_eureka_url', '_app_name', '_port', '_hostname', '_uid',
                 '_ip_addr', '_instance_id', '_health_check_url', '_heartbeat_interval',
                 '_status_page_url', '_lease_duration', '_lease_renewal_interval')

    def __init__(self,
                 app_name: Optional[str] = None,
                 port: Optional[int] = None,
                 ip_addr: Optional[str] = None,
                 *,
                 hostname: Optional[str] = None,
                 eureka_url: str = 'http://localhost:8765',
                 instance_id: Optional[str] = None,
                 uid:Optional[str] = str(uuid.uuid4()),
                 health_check_url: Optional[str] = None,
                 status_page_url: Optional[str] = None,
                 lease_duration: Optional[str] = None,
                 lease_renewal_interval: Optional[str] = None,
                 heartbeat_interval: Optional[int] = 30
                 ):
        """
        Naive eureka client, only supports the base operations.

        :param app_name: Application name, this is used to register/find
                         by name. Only required if you want to register
                         with Eureka.
        :param port: Application port that is accessible. Only required if
                     you want to register with Eureka
        :param ip_addr: IP Address the server is available on. Only required
                        if you want to register with Eureka.
        :param hostname: Host name of the machine, if not reachable by
                         DNS, use the IP. If not provided, the IP is
                         used by default. Only required if you want to register
                         with Eureka
        :param eureka_url: Eureka server url, including path.
        :param instance_id: Server instance ID, you should only really
                            set this if you need to operate on an existing
                            registered service.
        :param health_check_url: Health check URL if available, not required.
                                 But if included it should return 2xx.
        :param status_page_url: URL for server status (info route?), It's
                                required to not crash the Spring Eureka UI,
                                but otherwise not required. If not included -
                                we will just use the server IP with '/info'.
        """
        self._eureka_url = eureka_url.rstrip('/') + '/eureka'
        self._app_name = app_name
        self._port = port
        self._hostname = hostname or ip_addr
        self._ip_addr = ip_addr
        self._health_check_url = health_check_url
        self._instance_id = instance_id
        self._uid = uid
        self._lease_duration = lease_duration
        self._lease_renewal_interval = lease_renewal_interval
        self._heartbeat_interval = heartbeat_interval

        # Not including this crashes the Eureka UI, fixed in later version,
        # not one we can ensure people are using.
        if status_page_url is None:
            status_page_url = 'http://{}:{}/info'.format(self._ip_addr, port)
        self._status_page_url = status_page_url

    def _get_payload(self, metadata: Optional[Dict[str, Any]] = None):
        payload = {
            'instance': {
                'instanceId': self.instance_id,
                'leaseInfo': {
                    # 'evictionDurationSecs': eviction_duration,  # v2?
                    'durationInSecs': self._lease_duration,
                    'renewalIntervalInSecs': self._lease_renewal_interval,
                },
                'port': {
                    '$': self._port,
                    '@enabled': self._port is not None,
                },
                # TODO: Secure Port/Vip
                # 'securePort': {
                #     '$': self._secure_port,
                #     '@enabled': False
                # },
                # 'secureVipAddress': self._app_name,
                'hostName': self._hostname,
                'app': self._app_name,
                'ipAddr': self._ip_addr,
                'vipAddress': self._app_name,
                # TODO: AWS
                'dataCenterInfo': {
                    '@class': 'com.netflix.appinfo.MyDataCenterInfo',
                    'name': 'MyOwn',
                },
            }
        }
        if self._health_check_url is not None:
            payload['instance']['healthCheckUrl'] = self._health_check_url
        if self._status_page_url is not None:
            payload['instance']['statusPageUrl'] = self._status_page_url
        if metadata:
            payload['instance']['metadata'] = metadata
        return payload

    def startup(self, *, metadata: Optional[Dict[str, Any]] = None):
        payload = self._get_payload(metadata)
        is_success = self.register(payload)
        if not is_success:
            raise Exception
        heartbeat_task = Thread(target=self._heartbeat)
        heartbeat_task.daemon = True
        heartbeat_task.start()
        return is_success

    def register(self, payload: Optional[Dict[str, Any]] = None):
        url = '/apps/{}'.format(self._app_name)
        return self._do_req(url, method='POST', data=json.dumps(payload))

    def renew(self):
        """Renews the application's lease with eureka to avoid
        eradicating stale/decommissioned applications."""
        url = '/apps/{}/{}'.format(self._app_name, self.instance_id)
        return self._do_req(url, method='PUT')

    def _heartbeat(self):
        while True:
            time.sleep(self._heartbeat_interval)
            self.renew()

    def deregister(self):
        """Deregister with the remote server, if you forget to do
        this the gateway will be giving out 500s when it tries to
        route to your application."""
        url = '/apps/{}/{}'.format(self._app_name, self.instance_id)
        return self._do_req(url, method='DELETE')

    def set_status_override(self, status: StatusType):
        """Sets the status override, note: this should generally only
        be used to pull services out of commission - not really used
        to manually be setting the status to UP falsely."""
        url = '/apps/{}/{}/status?value={}'.format(self._app_name,
                                                   self.instance_id,
                                                   status.value)
        return self._do_req(url, method='PUT')

    def remove_status_override(self):
        """Removes the status override."""
        url = '/apps/{}/{}/status'.format(self._app_name,
                                          self.instance_id)
        return self._do_req(url, method='DELETE')

    def update_meta(self, key: str, value: Any):
        url = '/apps/{}/{}/metadata?{}={}'.format(self._app_name,
                                                  self.instance_id,
                                                  key, value)
        return self._do_req(url, method='PUT')

    def get_apps(self) -> Dict[str, Any]:
        """Gets a payload of the apps known to the
        eureka server."""
        url = '/apps'
        return self._do_req(url)

    def get_app(self, app_name: Optional[str] = None) -> Dict[str, Any]:
        app_name = app_name or self._app_name
        url = '/apps/{}'.format(app_name)
        return self._do_req(url)

    def get_app_instance(self, app_name: Optional[str] = None,
                         instance_id: Optional[str] = None):
        """Get a specific instance, narrowed by app name."""
        app_name = app_name or self._app_name
        instance_id = instance_id or self.instance_id
        url = '/apps/{}/{}'.format(app_name, instance_id)
        return self._do_req(url)

    def get_instance(self, instance_id: Optional[str] = None):
        """Get a specific instance, without needing to care about
        the app name."""
        instance_id = instance_id or self.instance_id
        url = '/instances/{}'.format(instance_id)
        return self._do_req(url)

    def get_by_vip(self, vip_address: Optional[str] = None):
        """Query for all instances under a particular vip address"""
        vip_address = vip_address or self._app_name
        url = '/vips/{}'.format(vip_address)
        return self._do_req(url)

    def get_by_svip(self, svip_address: Optional[str] = None):
        """Query for all instances under a particular secure vip address"""
        svip_address = svip_address or self._app_name
        url = '/vips/{}'.format(svip_address)
        return self._do_req(url)

    def _do_req(self, path: str, *, method: str = 'GET',
                data: Optional[Any] = None):
        """
        Performs a request against the instance eureka server.
        :param path: URL Path, the hostname is prepended automatically
        :param method: request method (put/post/patch/get/etc)
        :param data: Optional data to be sent with the request, must
                     already be encoded appropriately.
        :return: optional[dict[str, any]]
        """
        url = self._eureka_url + path
        with _SESSION.request(method, url, data=data) as resp:
            if 400 <= resp.status_code < 600:
                # TODO
                raise Exception(resp.status_code)
            try:
                res = resp.json()
            except JSONDecodeError:
                res = True
            return res

    def _generate_instance_id(self) -> str:
        """Generates a unique instance id"""
        instance_id = '{}:{}:{}'.format(
            self._uid, self._app_name, self._port
        )
        return instance_id

    @property
    def instance_id(self) -> str:
        """The instance_id the eureka client is targeting"""
        if self._instance_id is None:
            self._instance_id = self._generate_instance_id()
        # noinspection PyTypeChecker
        return self._instance_id

    @property
    def app_name(self) -> str:
        """The app_name the eureka client is targeting"""
        return self._app_name


class EurekaRegisterError(Exception):
    """An Eureka Registering error occurred."""
