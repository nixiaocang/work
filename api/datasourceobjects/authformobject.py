from api.datasourceobjects.abstractobject import AbstractObject


class AuthFormObject(AbstractObject):

    def __init__(self):
        super(AuthFormObject).__init__()

    class Field(AbstractObject.Field):
        union_id = 'union_id'
        account = 'account'
        success = 'success'
        form_params = 'form_params'

    _field_types = {
        'union_id': 'string',
        'account': 'string',
        'success': 'bool',
        'form_params': 'map<string, string>'
    }

    @classmethod
    def _get_field_enum_info(cls):
        return {}