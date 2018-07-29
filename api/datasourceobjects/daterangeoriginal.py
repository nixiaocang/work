from api.datasourceobjects.abstractobject import AbstractObject


class DateRangeOriginal(AbstractObject):

    def __init__(self):
        super(DateRangeOriginal, self).__init__()

    class Field(AbstractObject.Field):
        code = 'code'
        value = 'value'
        is_include_today = 'does include today'

    _field_types = {
        'code': 'string',
        'value': 'string',
        'is_include_today': 'bool'
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info

    def build_time_data(self, date_range_original):
        # TODO
        return NotImplementedError

    def build_date_key(self, date_range_original):
        # TODO
        return NotImplementedError