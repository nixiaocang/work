from api.datasourceobjects.abstractobject import AbstractObject


class DateRange(AbstractObject):

    def __init__(self):
        super(DateRange, self).__init__()

    class Field(AbstractObject.Field):
        field_id = 'id'
        start_date = 'start date'
        end_date = 'end date'

    _field_types = {
        'field_id': 'string',
        'start_date': 'string',
        'end_date': 'string'
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
