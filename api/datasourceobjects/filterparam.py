from api.datasourceobjects.abstractobject import AbstractObject


class FilterParam(AbstractObject):

    def __init__(self):
        super(FilterParam, self).__init__()

    class Field(AbstractObject.Field):
        self_id = 'id'
        operator = 'operator'
        values = 'values'

    _field_types = {
        'self_id': 'string',
        'operator': 'string',
        'values': 'list<string>'
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info
