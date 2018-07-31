from api.exceptions import DatasourceBadParameterTypeError
import os
import six
import importlib


class TypeChecker:
    primitive_types = set(["unsigned int", "int", "bool", "string", "Object",
        "datetime", "float"])

    def __init__(self, type_check_info, type_check_enum):
        self._type_check_info = type_check_info
        self._enum_data = type_check_enum

    def is_primitive_type(self, type):
        return (type in self.primitive_types) or (type in self._enum_data)

    def convert_string_to_prim_type(self, primitive_type, value):
        if primitive_type in self._enum_data:
            return value
        elif primitive_type in ("unsigned int", "int"):
            return int(value)
        elif primitive_type == "bool":
            if value in ("false", "0", "null"):
                return False
            return True
        elif primitive_type == "float":
            return float(value)
        elif primitive_type == "datetime":
            return value
        elif primitive_type == "string":
            return str(value)
        elif primitive_type == "Object":
            return value
        else:
            raise DatasourceBadParameterTypeError('Fail to convert from ' +
                                                  value.__class__.__name__ + ' to ' + str(primitive_type))

    def get_type(self, param):
        if param not in self._type_check_info:
            return None
        return self._type_check_info[param]

    def is_valid_key(self, param):
        return param in self._type_check_info

    def is_valid_pair(self, param, value):
        if self.is_valid_key(param):
            value_type = self._type_check_info[param]
            return self.is_type(value_type, value)
        else:
            return True

    def is_type_collection(self, value_type, collection_name):
        return collection_name == value_type[:len(collection_name)]

    def get_type_from_collection(self, value_type, collection_name):
        return [s.strip() for s in
                value_type[len(collection_name):].strip("<>").split(',')]

    def is_type(self, value_type, value, allow_dict_as_obj=True):
        if value is None or value_type is None:
            return True

        if value_type in self._enum_data:
            return value in self._enum_data[value_type]
        if value_type == 'file':
            return os.path.isfile(value)
        if value_type == 'list':
            return isinstance(value, list)
        if isinstance(value, dict) and value_type in ['map', 'Object']:
            return True
        if isinstance(value, bool):
            return value_type in ['bool']
        if isinstance(value, six.string_types):
            return value_type in ['string', 'unicode', 'file', 'datetime']
        if isinstance(value, (int, float)):
            return value_type in ['int', 'unsigned int', 'float']

        if self.is_type_collection(value_type, 'list'):
            if not isinstance(value, list):
                return False
            sub_type = self.get_type_from_collection(value_type, 'list')[0]
            return all([self.is_type(sub_type, item) for item in value])
        if self.is_type_collection(value_type, 'map'):
            if not isinstance(value, dict):
                return False
            sub_types = self.get_type_from_collection(value_type, 'map')
            sub_type_key = sub_types[0]
            sub_type_value = sub_types[1]
            return all([self.is_type(sub_type_key, k) and
                self.is_type(sub_type_value, v) for k, v in value.items()])

        if (type(value).__name__ == value_type or
                    hasattr(value, '_is' + value_type)):
            return True

        if allow_dict_as_obj and isinstance(value, dict):
            return self._type_is_ad_object(value_type)

    def is_list_param(self, param):
        if self.is_valid_key(param):
            return self.is_type_collection(self._type_check_info[param], "list")
        return False

    def is_map_param(self, param):
        if self.is_valid_key(param):
            return self.is_type_collection(self._type_check_info[param], "map")
        return False

    def is_file_param(self, param):
        if param == "filename":
            return True
        if self.is_valid_key(param):
            return self._type_check_info[param] == "file"
        return False

    # TODO importing customized module
    def _type_is_ad_object(self, value_type):
        try:
            mod = importlib.import_module(
                "api.datasourceobjects." + value_type.lower())
            # if not mod:
            #     importlib.import_module(
            #         "{{your module name}}.main.datasourceobjects." + value_type.lower())
            return mod is not None
        except:
            return False

    # TODO importing customized module
    @staticmethod
    def _create_field_object(field_type, data=None):
        mod = importlib.import_module(
            "api.datasourceobjects." + field_type.lower())
        # if not mod:
        #     importlib.import_module(
        #         "{{your module name}}.main.datasourceobjects." + value_type.lower())
        if mod is not None and hasattr(mod, field_type):
            obj = (getattr(mod, field_type))()
            if data is not None:
                obj._set_data(data)
            return obj
        return None

    def get_typed_value(self, key, value):
        if not self.is_valid_key(key):
            raise DatasourceBadParameterTypeError('Bad key: %s: %s' % (key, value))

        field_type = self.get_type(key)
        if self.is_type(field_type, value):
            return value

        if self.is_primitive_type(field_type) and isinstance(value, six.text_type):
            typed_value = self.convert_string_to_prim_type(field_type, value)
        elif self.is_type_collection(field_type, "list"):
            sub_type = self.get_type_from_collection(field_type, "list")[0]
            if isinstance(value, list):
                typed_value = [self.get_typed_value(sub_type, v) for v in value]
            else:
                typed_value = [self.get_typed_value(sub_type, value)]
        elif self.is_type_collection(field_type, "map"):
            sub_types = self.get_type_from_collection(field_type, "map")
            if len(sub_types) == 2:
                sub_type_key = sub_types[0]
                sub_type_value = sub_types[1]
            else:
                sub_type_key = 'string'
                sub_type_value = sub_types[0]
            typed_value = dict(
                (self.get_typed_value(sub_type_key, k),
                self.get_typed_value(sub_type_value, v))
                for (k, v) in value.items()
            )
        elif isinstance(value, dict):
            try:
                typed_value = self._create_field_object(field_type, value)
            except:
                typed_value = value
        else:
            typed_value = value

        if not self.is_type(field_type, typed_value):
            raise DatasourceBadParameterTypeError('Bad type %s:%s' % (field_type, typed_value))
        return typed_value