from collections import namedtuple

import openpyxl


from src.models import Validator


wb = openpyxl.load_workbook('input/data.xlsx')

ws = wb['Data']
headers = [cell.value.lower().replace(' ', '_') for cell in ws[1]]
print(headers)
user_nt = namedtuple('User', field_names=headers)

for row in ws.iter_rows(min_row=2,
                        max_col=ws.max_column,
                        max_row=ws.max_row,
                        values_only=True):
    record = user_nt(*row)
    obj = Validator(record)

print(Validator.valid_stream)
print(Validator.bad_stream)
print(Validator.stats.get('total'))
print(Validator.stats.get('failed'))
