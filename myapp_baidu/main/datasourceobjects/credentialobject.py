# from api.datasourceobjects.abstractobject import AbstractObject
#
#
# class CredentialObject(AbstractObject):
#
#     def __init__(self):
#         super(CredentialObject, self).__init__()
#
#     class Field(AbstractObject.Field):
#         pass
#
#     _field_types = {
#         'instanceTokenDataUpdate': 'bool',
#         'instanceTokenKey': 'string',
#         'instanceTokenData': 'InstanceTokenObject',
#         'accountTokenDataUpdate': 'bool',
#         'accountTokenData': 'string'
#     }
#
#     @classmethod
#     def _get_field_enum_info(cls):
#         return {}
#
#     """ custom methods """
#
#     def refresh(self):
#         raise NotImplementedError
#
#     def revoke(self):
#         raise NotImplementedError