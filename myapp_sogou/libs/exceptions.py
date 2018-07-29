import json
import traceback
from myapp_sogou.libs.const import ResponseCode as responseCode


class BaseError(Exception):
    """base exception"""

    def __init__(self,
                 code=responseCode.error,
                 msg='Base Error',
                 debug_msg=traceback.format_exc(),
                 payload=None
                 ):
        self._code = code
        self._msg = msg
        self._debug_msg = debug_msg
        self._payload = payload
        self._repr_init()

    def _repr_init(self):
        dict_obj_repr = {'extra_msg': self._payload} if self._payload and isinstance(self._payload, dict) else {}
        dict_obj_repr.update({'code': self._code, 'msg': self._msg, 'debugMsg': self._debug_msg})
        self._object_repr = dict_obj_repr
        self._json_repr = json.dumps(dict_obj_repr)

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return self._msg

    @property
    def debug_msg(self):
        return self._debug_msg

    @property
    def payload(self):
        return self._payload

    @property
    def object_repr(self):
        return self._object_repr

    @property
    def json_repr(self):
        return self._json_repr


class AuthURLError(BaseError):
    """Auth url retrieving error"""
    def __init__(self, msg='Authorization URL Retrieving Failure', payload=None):
        super(AuthURLError, self).__init__(
            responseCode.error,
            msg,
            debug_msg=traceback.format_exc(),
            payload=payload
        )


class OAuthTokenError(BaseError):
    """Token exchange error"""
    def __init__(self, msg='Authorization Token Retrieving Failure', payload=None):
        super(OAuthTokenError, self).__init__(
            responseCode.error,
            msg,
            debug_msg=traceback.format_exc(),
            payload=payload
        )


class TokenReleaseError(BaseError):
    """Token release error"""
    def __init__(self, msg='Authorization Token Revoking Failure', payload=None):
        super(TokenReleaseError, self).__init__(
            responseCode.error,
            msg,
            debug_msg=traceback.format_exc(),
            payload=payload
        )


class AuthorizationError(BaseError):
    """Token invalid"""
    def __init__(self, msg='Authorization Token Revoking Failure', payload=None):
        super(AuthorizationError, self).__init__(
            responseCode.error,
            msg,
            debug_msg=traceback.format_exc(),
            payload=payload
        )


class DataSourceServiceError(BaseError):
    """Token invalid"""
    def __init__(self, msg='Data Source Service Error', payload=None):
        super(DataSourceServiceError, self).__init__(
            responseCode.error,
            msg,
            debug_msg=traceback.format_exc(),
            payload=payload
        )


class DataSourceResourceNotFoundError(BaseError):
    """Token invalid"""
    def __init__(self, msg='Data Source Service Error', payload=None):
        super(DataSourceResourceNotFoundError, self).__init__(
            responseCode.error,
            msg,
            debug_msg=traceback.format_exc(),
            payload=payload
        )


# class AError(BaseError):
#     """A error"""
#     def __init__(self, msg=None, payload=None):
#         super(AError, self).__init__(
#             responseCode.error,
#             msg or errorMsg.AError,
#             debug_msg=traceback.format_exc(),
#             payload=payload
#         )
#
#
# class BError(BaseError):
#     """B error"""
#     def __init__(self, msg=None, payload=None):
#         super(BError, self).__init__(
#             responseCode.error,
#             msg or errorMsg.BError,
#             debug_msg=traceback.format_exc(),
#             payload=payload
#         )
#