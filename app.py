import os
import io

from collections import namedtuple

import boto3

from openpyxl import load_workbook

from validator.loader import get_key_from_event
from validator.loader import get_info_from_key

from validator.writer import ExcelWriter

from validator.engine import Validator

client = boto3.client('s3')


def handler(event, *args, **kwargs):
    original_key = get_key_from_event(event=event)
    file_obj = get_info_from_key(key=original_key)
    response = client.get_object(
        Bucket=os.environ.get('S3_BUCKET'),
        Key=original_key,
    )
    body = response.get('Body')
    wb = load_workbook(io.BytesIO(body.read()))
    ws = wb['Data']
    headers = [cell.value.lower().replace(' ', '_') for cell in ws[1]]
    Validator.validate_headers(headers=headers)
    builder = namedtuple('Builder', field_names=headers)
    for row in ws.iter_rows(min_row=2,
                            max_col=ws.max_column,
                            max_row=ws.max_row,
                            values_only=True):
        obj = Validator(builder(*row))
        obj.validate()
    print(Validator.stats.get('total'))
    print(Validator.stats.get('failed'))

    error_file = ExcelWriter(headers=headers,
                             stream=Validator.bad_stream,
                             obj_key=file_obj,
                             duplicate_file=False)
    duplicated_file = ExcelWriter(headers=headers,
                                  stream=Validator.bad_stream,
                                  obj_key=file_obj,
                                  duplicate_file=True)
