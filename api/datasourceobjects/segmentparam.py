from api.datasourceobjects.abstractobject import AbstractObject


class SegmentParam(AbstractObject):

    def __init__(self):
        super(SegmentParam, self).__init__()

    class Field(AbstractObject.Field):
        dynamic_model = 'dynamic model'
        segment = 'segment'

    _field_types = {
        'dynamic_model': 'bool',
        'segment': 'string',
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info