"""This module contains helper functions for interacting with
database & excel file"""
from collections import namedtuple

from typing import Any


class ExtensionError(Exception):
    pass


class TaskIDError(Exception):
    pass


class ObjectKeyError(Exception):
    pass


def get_key_from_event(*, event: dict) -> str:
    """Return S3 Object's Key from Lambda event

    Args:
        event (dict): Lambda event object
    """
    record = event['Records'][0]
    obj_key = record['s3']['object'].get('key')
    if obj_key:
        return obj_key
    else:
        raise ObjectKeyError('KeyError: "key" not found')


def extract_file_name(*, file_name: Any) -> Any:
    """Validate file extension

    Args:
        file_name (str): specify file name with extension

    Returns:
        (FileName)
            name: File name
            extension: File extension

    Raises:
        ExtensionError: file extension is not supported
    """
    file_name_nt = namedtuple('FileName', 'name extension')
    temp = file_name.split('.')
    file_name_obj = file_name_nt(*temp)
    return file_name_obj


def get_info_from_key(*, key: str) -> Any:
    """Extract information from Object's key

    Args:
        key (str): S3 Object's key

    Returns
        (FileObject)
            task_id (str): Task ID
            file (FileNameObject):
                name (str): File name
                extension (str): File extension

    """
    file_nt = namedtuple('DataFile', 'parent task_id file', defaults=None)
    temp = key.split('/')
    file_obj = file_nt(*temp)
    if not file_obj.task_id:
        raise TaskIDError('Task ID not existed')
    if not file_obj.task_id.isnumeric():
        raise TaskIDError(f'Invalid Task ID: {file_obj.task_id}')
    file_obj.file = extract_file_name(file_name=file_obj.file)
    return file_obj



