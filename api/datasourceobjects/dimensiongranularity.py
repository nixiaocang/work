from api.datasourceobjects.abstractobject import AbstractObject


class DimensionGranularity(AbstractObject):

    def __init__(self):
        super(DimensionGranularity, self).__init__()

    class Field(AbstractObject.Field):
        self_type = 'type'
        value = 'value'

    _field_types = {
        'self_type': 'string',
        'value': 'string',
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info