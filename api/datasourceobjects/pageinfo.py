from api.datasourceobjects.abstractobject import AbstractObject


class PageInfo(AbstractObject):

    def __init__(self):
        super(PageInfo, self).__init__()

    class Field(AbstractObject.Field):
        page_index = 'page index'
        page_size = 'page size'

    _field_types = {
        'page_index': 'int',
        'page_size': 'int',
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info