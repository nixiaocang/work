from api.datasourceobjects.abstractobject import AbstractObject


class FilterValueParam(AbstractObject):

    def __init__(self):
        super(FilterValueParam).__init__()

    class Field(AbstractObject.Field):
        instance_id = 'instance_id'
        profile_id = 'profile_id'
        report_id = 'report_id'
        dimension_field_id = 'dimension_field_id'
        date_range = 'date_range'

    _field_types = {
        'instance_id': 'string',
        'profile_id': 'string',
        'report_id': 'string',
        'dimension_field_id': 'string',
        'date_range': 'DateRange'
    }

    @classmethod
    def _get_field_enum_info(cls):
        return {}