from api.datasourceobjects.abstractobject import AbstractObject


class DataRequestFileParam(AbstractObject):

    def __init__(self):
        super(DataRequestFileParam).__init__()

    class Field(AbstractObject.Field):
        instance_id = 'instance_id'
        profile_id = 'profile_id'
        report_id = 'report_id'
        field_id = 'field_id'
        typee = 'typee'
        file_type = 'file_type'
        sheet_name = 'sheet_name'
        source = 'source'
        is_convert = 'is_convert'

    _field_types = {
        'instance_id': 'string',
        'profile_id': 'string',
        'report_id': 'string',
        'field_id': 'string',
        'typee': 'string',
        'file_type': 'string',
        'sheet_name': 'string',
        'source': 'string',
        'is_convert': 'bool'
    }

    @classmethod
    def _get_field_enum_info(cls):
        return {}