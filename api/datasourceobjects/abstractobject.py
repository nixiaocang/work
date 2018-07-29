
from api.typechecker import TypeChecker
from api.exceptions import DatasourceBadObjectError

import collections
import json


class AbstractObject(collections.MutableMapping):

    _default_read_fields = []
    _field_types = {}

    class Field:
        pass

    def __init__(self):
        self._data = {}
        self._field_checker = TypeChecker(self._field_types, self._get_field_enum_info())

    def __getitem__(self, key):
        return self._data[str(key)]

    def __setitem__(self, key, value):
        if key.startswith('_'):
            self.__setattr__(key, value)
        else:
            self._data[key] = self._field_checker.get_typed_value(key, value)
            self.__setattr__(key, self._field_checker.get_typed_value(key, value))


    def __eq__(self, other):
        return other is not None and 'export_all_data' in other and \
            self.export_all_data() == other.export_all_data()

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __unicode__(self):
        return self._data

    def __repr__(self):
        return "<%s> %s" % (
            self.__class__.__name__,
            json.dumps(
                self.export_value(self._data),
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            ),
        )

    #reads in data from json object
    def _set_data(self, data):
        if hasattr(data, 'items'):
            for key, value in data.items():
                self[key] = value
        else:
            raise DatasourceBadObjectError("Bad data to set object data")
        self._json = data

    def _set_data_after_check(self, data):
        if hasattr(data, 'items'):
            for key, value in data.items():
                self.__setitem__(key, value)
        else:
            raise DatasourceBadObjectError("Bad data to set object data")
        self._json = data

    @classmethod
    def _get_field_enum_info(cls):
        """Returns info for fields that use enum values
        Should be implemented in subclasses
        """
        return {}

    @classmethod
    def get_endpoint(cls):
        """Returns the endpoint name.
        Raises:
            NotImplementedError if the method is not implemented in a class
                that derives from this abstract class.
        """
        raise NotImplementedError(
            "%s must have implemented get_endpoint." % cls.__name__,
        )

    @classmethod
    def get_default_read_fields(cls):
        """Returns the class's list of default fields to read."""
        return cls._default_read_fields

    @classmethod
    def set_default_read_fields(cls, fields):
        """Sets the class's list of default fields to read.
        Args:
            fields: list of field names to read by default without specifying
                them explicitly during a read operation either via EdgeIterator
                or via AbstractCrudObject.read.
        """
        cls._default_read_fields = fields

    @classmethod
    def _assign_fields_to_params(cls, fields, params):
        """Applies fields to params in a consistent manner."""
        if fields is None:
            fields = cls.get_default_read_fields()
        if fields:
            params['fields'] = ','.join(fields)

    def set_data(self, data, type_check):
        """
        For an AbstractObject, we do not need to keep history.
        """
        if not type_check:
            self._set_data(data)
        else:
            self._set_data_after_check(data)

    def export_value(self, data):
        if isinstance(data, AbstractObject):
            data = data.export_all_data()
        elif isinstance(data, dict):
            data = dict((k, self.export_value(v))
                        for k, v in data.items()
                        if v is not None)
        elif isinstance(data, list):
            data = [self.export_value(v) for v in data]
        return data

    def export_data(self):
        """
        Deprecated. Use export_all_data() instead.
        """
        return self.export_all_data()

    def export_all_data(self):
        return self.export_value(self._data)

    @classmethod
    def create_object(cls, data, type_check=False):
        new_object = cls()
        if type_check:
            new_object._set_data_after_check(data)
        else:
            new_object._set_data(data)
        return new_object
