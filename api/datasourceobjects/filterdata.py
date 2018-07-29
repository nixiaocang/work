from api.datasourceobjects.abstractobject import AbstractObject


class FilterData(AbstractObject):

    def __init__(self):
        super(FilterData, self).__init__()

    class Field(AbstractObject.Field):
        self_id = 'id'
        name = 'name'

    _field_types = {
        'self_id': 'string',
        'name': 'string',
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info
