from api.datasourceobjects.abstractobject import AbstractObject
import enum


class TimeField(AbstractObject):

    def __init__(self):
        super(TimeField, self).__init__()

    class Field(AbstractObject.Field):
        self_id = 'self_id'
        name = 'name'
        data_format = 'data_format'
        data_type = 'data_type'

    _field_types = {
        'self_id': 'string',
        'name': 'string',
        'data_format': 'string',
        'data_type': 'string'
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info