import enum


class TaskMessage(enum.Enum):
    MISSING_HEADERS = 'MISSING_HEADER'
    FILE_NAME_ERROR = 'FILE_NAME_ERROR'
    MISSING_DATA_SHEET = 'MISSING_DATA_SHEET'
    ENGINE_ERROR = 'ENGINE_ERROR'


class ExtensionError(Exception):
    pass


class TaskError(Exception):
    pass


class ObjectKeyError(Exception):
    pass


class MissingHeadersError(Exception):
    pass
