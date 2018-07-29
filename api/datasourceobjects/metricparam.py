from api.datasourceobjects.abstractobject import AbstractObject


class MetricParam(AbstractObject):

    def __init__(self):
        super(MetricParam, self).__init__()

    class Field(AbstractObject.Field):
        self_id = 'id'
        data_type = 'data type'
        calculate_type = 'calculate type'

    _field_types = {
        'self_id': 'string',
        'data_type': 'string',
        'calculate_type': 'string'
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info