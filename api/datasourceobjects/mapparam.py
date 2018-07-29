from api.datasourceobjects.abstractobject import AbstractObject
import enum


class MapParam(AbstractObject):

    def __init__(self):
        super(MapParam, self).__init__()

    class Field(AbstractObject.Field):
        map_type = 'map type'
        map_code = 'map code'

    class MapType(enum.Enum):
        ASC = 'COUNTRY'
        DESC = 'WORLD'

    _field_types = {
        'map_type': 'MapType',
        'map_code': 'string',
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        field_enum_info['MapType'] = MapParam.MapType.__dict__.values()
        return field_enum_info