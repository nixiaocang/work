from api.datasourceobjects.abstractobject import AbstractObject


class DataRequestSaasParam(AbstractObject):

    def __init__(self):
        super(DataRequestSaasParam, self).__init__()

    class Field(AbstractObject.Field):
        need_aggregate = 'need_aggregate'
        instance_id = 'instance_id'
        profile_id = 'profile_id'
        report_id = 'report_id'
        metric_list = 'metric_list'
        dimension_list = 'dimension_list'
        filter_param = 'filter_param'
        segment_param = 'segment_param'
        sort = 'sort'
        daterange = 'daterange'
        daterange_original_time = 'daterange_original_time'
        page_info = 'page_info'
        map_param = 'map_param'
        extra_param = 'extra_param'
        graph_type = 'graph_type'

    _field_types = {
        'need_aggregate': 'bool',
        'instance_id': 'string',
        'profile_id': 'string',
        'report_id': 'string',
        'metric_list': 'list<MetricParam>',
        'dimension_list': 'list<DimensionParam>',
        'filter_param': 'list<FilterParam>',
        'segment_param': 'SegmentParam',
        'sort': 'Sorting',
        'daterange': 'DateRange',
        'daterange_original_time': 'DateRangeOriginal',
        'page_info': 'PageInfo',
        'map_param': 'MapParam',
        'extra_param': 'map<string, Object>',
        'graph_type': 'GraphType'
    }

    @classmethod
    def _get_field_enum_info(cls):
        return {}
