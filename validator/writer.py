import os

from typing import List
from typing import Any

from tempfile import NamedTemporaryFile

from openpyxl import Workbook

from openpyxl.styles import NamedStyle
from openpyxl.styles import PatternFill

from validator.loader import file_nt

error_style = NamedStyle(name='error')
error_style.fill = PatternFill(start_color='00FF0000',
                               end_color='00FF0000',
                               fill_type='solid')


class ExcelWriter:

    def __init__(self,
                 *,
                 headers: List[str],
                 stream: List[Any],
                 obj_key: file_nt,
                 duplicate_file: bool = False):
        self.headers = headers
        self.obj_key = obj_key
        self.duplicated_file = duplicate_file
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = 'Data'
        self.ws.append([
            " ".join(field.split('_')).capitalize()
            for field in self.headers
        ])
        self.write_sheet(stream)

    @property
    def duplicated_file(self):
        return self._duplicated

    @duplicated_file.setter
    def duplicated_file(self, value):
        self._duplicated = value
        if not value:
            self.headers.append('error_details')

    def write_sheet(self, stream):
        for row_idx, item in enumerate(stream):
            self.write_rows_excel(row_idx=row_idx + 2, data=item)

    def write_rows_excel(self, *, row_idx, data: dict):
        """Write a row to the Worksheet

        Args:
            data (dict): specify row data
            row_idx (int): specify row index
        """
        col_idx = 1
        temp = data.get('data')._asdict()
        errors = data.pop('errors', None)
        for name, value in temp.items():
            cell = self.ws.cell(column=col_idx, row=row_idx, value=value)
            if errors and name in errors:
                cell.style = error_style
            col_idx += 1
        self.ws.cell(column=col_idx,
                     row=row_idx,
                     value=data.get('error_msg'))

    def upload_to_s3(self, *, client, bucket_name):
        if self.duplicated_file:
            post_fix = 'duplicates'
        else:
            post_fix = 'errors'
        obj_key = (f'output/{self.obj_key.task_id}'
                   f'/{self.obj_key.file.name}_{post_fix}.xlsx')
        with NamedTemporaryFile() as tmp:
            self.wb.save(tmp.name)
            tmp.seek(0)
            client.upload_fileobj(tmp,
                                  bucket_name,
                                  obj_key)


class DBWriter:

    def __int__(self,
                *,
                task_id: str,
                cursor):
        self.task_id = task_id
        self._cursor = cursor
