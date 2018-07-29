from api.datasourceobjects.abstractobject import AbstractObject


class AuthNormalObject(AbstractObject):

    def __init__(self):
        super(AuthNormalObject).__init__()

    class Field(AbstractObject.Field):
        union_code = 'union_code'
        redirect_url = 'redirect_url'

    _field_types = {
        'union_code': 'string',
        'redirect_url': 'string'
    }

    @classmethod
    def _get_field_enum_info(cls):
        return {}