from datetime import date

from collections import namedtuple

from marshmallow import ValidationError

from src.utils.schema import UserSchema
from src.utils.models import User

headers = [
    'first_name',
    'middle_name',
    'last_name',
    'staff_id',
    'dob',
    'work_email',
    'phone_number',
    'tax_code',
    'social_code',
    'gov_id',
    'gov_date',
    'gov_place',
    'passport_id',
    'passport_date',
    'passport_place',
    'start_working_date',
    'end_working_date',
    'user_type',
    'gender',
    'working_status',
]

user_nt = namedtuple('User', field_names=headers)

data_list = [
    (
        'Romeo',
        None,
        'Juliet',
        '123123',
        date(2021, 7, 23),
        'romeo.juliett@gmail.com',
        '21321312',
        None,
        None,
        '2131231',
        date(2021, 7, 23),
        'Ha Noi',
        None,
        None,
        None,
        date(2021, 7, 23),
        None,
        'Staff',
        'Male',
        'Probation',
    ),
    (
        'None'*200,
        None,
        'Juliet',
        '123123',
        date(2021, 7, 23),
        'romeo.juliett@gmail.com',
        '21321312',
        None,
        None,
        '2131231',
        date(2021, 7, 23),
        'Kingdom',
        None,
        None,
        None,
        date(2021, 7, 23),
        None,
        'Staff',
        'Male',
        'Probation',
    ),
    (
        None,
        None,
        'Juliet',
        '123123',
        date(2021, 7, 23),
        'romeo.juliett@gmail.com',
        '21321312',
        None,
        None,
        '2131231',
        date(2021, 7, 23),
        'Kingdom',
        None,
        None,
        None,
        date(2021, 7, 23),
        None,
        'Staff',
        'Male',
        'Probation',
    ),
]

validator = UserSchema()
for data in data_list:
    record = user_nt(*data)
    temp = validator.dump(User(record))
    try:
        obj = validator.load(temp)
    except ValidationError as e:
        print(e)
