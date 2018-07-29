from api.datasourceobjects.abstractobject import AbstractObject


class DimensionParam(AbstractObject):

    def __init__(self):
        super(DimensionParam, self).__init__()

    class Field(AbstractObject.Field):
        self_id = 'id'
        data_type = 'data type'
        granularity = 'granularity'

    _field_types = {
        'self_id': 'string',
        'data_type': 'string',
        'granularity': 'DimensionGranularity'
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info