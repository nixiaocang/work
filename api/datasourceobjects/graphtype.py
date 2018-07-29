from api.datasourceobjects.abstractobject import AbstractObject
import enum


class GraphType(AbstractObject):

    def __init__(self):
        super(GraphType, self).__init__()

    class Field(AbstractObject.Field):
        name = 'name'
        graph_type = 'graph type'

    class _GraphType(enum.Enum):
        LINE = 'LINE'
        AREA = 'AREA'
        STACKCOLUMN = 'STACKCOLUMN'
        STACKBAR = 'STACKBAR'
        DOUBLEAXIS = 'DOUBLEAXIS'
        AREASPLINE = 'AREASPLINE'
        COLUMN = 'COLUMN'
        BAR = 'BAR'
        PIE = 'PIE'
        NUMBER = 'NUMBER'
        PROGRESSBAR = 'PROGRESSBAR'
        TABLE = 'TABLE'
        MAP = 'MAP'
        TEXT = 'TEXT'

    _field_types = {
        'name': 'string',
        'graph_type': 'GraphType',
    }

    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        field_enum_info['GraphType'] = GraphType._GraphType.__dict__.values()
        return field_enum_info

    def is_highchart_graph(self, gtype):
        return gtype in self._GraphType.__dict__.values()
