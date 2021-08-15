import os
import io
import logging

from collections import namedtuple

import boto3

from openpyxl import load_workbook

from validator.loader import get_key_from_event
from validator.loader import get_info_from_key

from validator.writer import ExcelWriter

from validator.engine import Validator

from validator.engine.errors import MissingHeadersError
from validator.engine.errors import TaskError

client = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, *args, **kwargs):
    original_key = get_key_from_event(event=event)
    try:
        file_obj = get_info_from_key(key=original_key)
    except TaskError as e:
        # TODO: UpdateDB (status=Completed, msg = FILE_NAME_ERROR, details=e)
        logger.warning(f'FILE_NAME_ERROR: {e}')
        return
    response = client.get_object(
        Bucket=os.environ.get('S3_BUCKET'),
        Key=original_key,
    )
    body = response.get('Body')
    wb = load_workbook(io.BytesIO(body.read()))
    ws = wb['Data']
    if not ws:
        # TODO: UpdateDB (status=Completed, msg = MISSING_DATA_SHEET)
        logger.warning(f'MISSING_DATA_SHEET')
        return
    headers = [cell.value.lower().replace(' ', '_') for cell in ws[1]]

    try:
        Validator.validate_headers(headers=headers)
    except MissingHeadersError as e:
        logger.warning(f'MISSING_HEADERS: {e}')
        # TODO: UpdateDB (status=Completed, msg = MISSING_HEADERS, details=e)
        return
    builder = namedtuple('Builder', field_names=headers)
    for row in ws.iter_rows(min_row=2,
                            max_col=ws.max_column,
                            max_row=ws.max_row,
                            values_only=True):
        obj = Validator(builder(*row))
        obj.validate()
    Validator.check_duplicate()
    if Validator.bad_stream:
        error_file = ExcelWriter(headers=headers,
                                 stream=Validator.bad_stream,
                                 obj_key=file_obj)
        # TODO: upload_to_s3(os.environ.get(client, 'S3_BUCKET'))
    if Validator.duplicate_stream:
        duplicate_stream = list(Validator.duplicate_stream)
        Validator.stats['duplicated'] = len(duplicate_stream)
        duplicated_file = ExcelWriter(headers=headers,
                                      stream=duplicate_stream,
                                      obj_key=file_obj,
                                      duplicate_file=True)
        # TODO: upload_to_s3(os.environ.get(client, 'S3_BUCKET'))
    print(Validator.stats.get('total'))
    print(Validator.stats.get('failed'))
    print(Validator.stats.get('duplicated'))
    # TODO: UpdateDB (status=Completed, total, failed, duplicated)
    # logger.info(f'COMPLETED:Task(id={},total={},failed={},duplicated={})')
    logger.info('COMPLETED')
    return
