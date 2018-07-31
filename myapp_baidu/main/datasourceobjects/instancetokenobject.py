# from api.datasourceobjects.abstractobject import AbstractObject
#
#
# class InstanceTokenObject(AbstractObject):
#     def __init__(self):
#         super(InstanceTokenObject, self).__init__()
#
#     class Field(AbstractObject.Field):
#         pass
#
#     _field_types = {
#         'instanceTokenDataUpdate': 'bool',
#         'instanceTokenKey': 'string',
#         'instanceTokenData': 'string',
#         'accountTokenDataUpdate': 'bool',
#         'accountTokenData': 'string'
#     }
#
#     @classmethod
#     def _get_field_enum_info(cls):
#         return {}