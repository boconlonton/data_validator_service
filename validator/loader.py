"""This module contains helper functions for interacting with
database & excel file"""
import io
import json
import typing

from collections import namedtuple
from contextlib import ExitStack

from typing import Any
from typing import Set

from aurora_data_api import connect

from validator.engine.errors import ObjectKeyError
from validator.engine.errors import TaskError

file_nt = namedtuple('DataFile', 'parent task_id file', defaults=None)
file_name_nt = namedtuple('FileName', 'name extension')


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
    temp = key.split('/')
    file_name_obj = extract_file_name(file_name=temp[-1])
    temp[-1] = file_name_obj
    file_obj = file_nt(*temp)
    if not file_obj.task_id:
        raise TaskError('MISSING_TASK_ID')
    if not file_obj.task_id.isnumeric():
        raise TaskError('INVALID_TASK_ID')
    return file_obj


def get_data_from_s3(client, *, bucket: str, key: str) -> dict:
    """Return a dictionary contains data from S3 file

    Args:
        client:
        bucket (str): specify bucket name
        key (str): specify object key
    """
    response = client.get_object(
        Bucket=bucket,
        Key=key,
    )
    body = response.get('Body')
    return json.load(io.BytesIO(body.read()))


def get_existed_emails(*,
                       instance_arn: str,
                       secret_arn: str,
                       db_name: str) -> Set:
    """Return a set of existed emails in database

    Args:
        instance_arn (str): specify Aurora Instance ARN
        secret_arn (str): specify Secret Manger ARN
        db_name (str): specify database name
    """
    with ExitStack() as stack:
        conn = stack.enter_context(
            connect(
                instance_arn,
                secret_arn,
                database=db_name
            )
        )
        cursor = stack.enter_context(conn.cursor())
        query = 'SELECT work_email FROM "public"."users"'
        cursor.execute(query)
        temp = cursor.fetchall()
    return {item[0] for item in temp}


def get_headers(*, worksheet) -> typing.List:
    """Return list of headers of a worksheet

    Args:
        worksheet: specify the worksheet
    """
    return [cell.value.lower().replace(' ', '_') for cell in worksheet[1]]
