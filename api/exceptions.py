# TODO


class DatasourceBaseError(Exception):
    pass


class DatasourceBadObjectError(DatasourceBaseError):
    pass


class DatasourceObjectParseError(DatasourceBaseError):
    pass


class DatasourceBadParameterTypeError(DatasourceBaseError):
    """Raised when a parameter or field is set with improper type."""
    pass
