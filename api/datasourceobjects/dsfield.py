from api.datasourceobjects.abstractobject import AbstractObject
import enum


class DsField(AbstractObject):

    def __init__(self):
        super(DsField, self).__init__()

    class Field(AbstractObject.Field):
        self_id = 'self_id'
        name = 'name'
        uniname = 'uniname'
        field_type = 'field_type'
        data_type = 'data_type'

        field_unit = 'field_unit'
        is_allow_filter = 'is_allow_filter'

        original_data_type = 'original_data_type'
        original_extra = 'original_extra'
        children = 'children'

    class DataType(enum.Enum):
        NUMBER = 'NUMBER'
        STRING = 'STRING'
        DATE = 'DATE'
        DATETIME = 'DATETIME'
        PERCENT = 'PERCENT'
        TIME = 'TIME'
        TIMESTAMP = 'TIMESTAMP'
        TEXT = 'TEXT'
        CURRENCY = 'CURRENCY'
        DURATION = 'DURATION'

    class FieldType(enum.Enum):
        METRIC = 'METRIC'
        DIMENSION = 'DIMENSION'
        SEGMENT = 'SEGMENT'

    _field_types = {
        'self_id': 'string',
        'name': 'string',
        'uniname': 'string',
        'field_type': 'FieldType',
        'data_type': 'DataType',
        'field_unit': 'string',
        'is_allow_filter': 'bool',
        'original_data_type': 'string',
        'original_extra': 'map<string, Object>',
        'children': 'list'
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        field_enum_info['DataType'] = DsField.DataType.__dict__.values()
        field_enum_info['FieldType'] = DsField.FieldType.__dict__.values()
        return field_enum_info