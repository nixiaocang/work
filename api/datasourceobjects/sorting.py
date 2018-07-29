from api.datasourceobjects.abstractobject import AbstractObject
import enum


class Sorting(AbstractObject):

    def __init__(self):
        super(Sorting, self).__init__()

    class Field(AbstractObject.Field):
        field_id = 'field id'
        sort_by = 'sortby type'

    class SortbyType(enum.Enum):
        ASC = 'ASC'
        DESC = 'DESC'

    _field_types = {
        'field_id': 'string',
        'sort_by': 'SortbyType',
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        field_enum_info['SortbyType'] = Sorting.SortbyType.__dict__.values()
        return field_enum_info