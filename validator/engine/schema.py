from marshmallow import Schema
from marshmallow import fields
from marshmallow import validates_schema
from marshmallow import validate
from marshmallow import ValidationError
from marshmallow import post_load


_HEADERS = {
    'first_name',
    'middle_name',
    'last_name',
    'code',
    'date_of_birth',
    'work_email',
    'phone_number',
    'tax_code',
    'social_code',
    'government_id',
    'government_issued_date',
    'government_issued_place',
    'passport_id',
    'passport_issued_date',
    'passport_issued_place',
    'start_working_date',
    'end_working_date',
    'user_type',
    'gender',
    'working_status',
    'permission_profile',
    'employment_contract',
    'birthplace',
    'hometown',
    'ethnics',
    'religion',
    'permanent_address',
    'permanent_address_province',
    'permanent_address_district',
    'permanent_address_ward',
    'mailing_address',
    'mailing_address_province',
    'mailing_address_district',
    'mailing_address_ward',
    'communist_party_status',
    'communist_party_entry_date',
    'trade_union_status',
    'trade_union_entry_date',
    'teaching_title',
    'academic_title',
    'degree'
}


class UserSchema(Schema):
    first_name = fields.String(validate=validate.Length(min=1, max=50))
    middle_name = fields.String(validate=validate.Length(min=1, max=50),
                                allow_none=True)
    last_name = fields.String(validate=validate.Length(min=1, max=50))
    code = fields.String(validate=validate.Length(min=1, max=15))
    dob = fields.Date(format='%d-%m-%Y')
    work_email = fields.Email(validate=validate.Length(min=5, max=50))
    phone = fields.String(validate=validate.Length(min=8, max=20))
    tax_code = fields.String(validate=validate.Length(min=5, max=12),
                             allow_none=True)
    social_code = fields.String(validate=validate.Length(min=5, max=12),
                                allow_none=True)
    gov_id = fields.String(validate=validate.Length(min=1, max=20))
    gov_date = fields.Date(format='%d-%m-%Y')
    gov_place = fields.Integer(allow_none=True)
    passport_id = fields.String(validate=validate.Length(min=1, max=20),
                                allow_none=True)
    passport_date = fields.Date(format='%d-%m-%Y', allow_none=True)
    passport_place = fields.Integer(allow_none=True)
    start_working_date = fields.Date(format='%d-%m-%Y')
    end_working_date = fields.Date(format='%d-%m-%Y', allow_none=True)
    type = fields.Integer()
    gender = fields.Integer()
    working_status_id = fields.String()
    permission_profile_id = fields.Integer()
    employment_contract_id = fields.Integer()
    birthplace = fields.Integer()
    hometown = fields.Integer()
    ethnics_id = fields.Integer()
    religion_id = fields.Integer()
    permanent_address = fields.String(allow_none=True)
    permanent_address_province_id = fields.Integer()
    permanent_address_district_id = fields.Integer()
    permanent_address_ward_id = fields.Integer()
    mailing_address = fields.String(allow_none=True)
    mailing_address_province_id = fields.Integer()
    mailing_address_district_id = fields.Integer()
    mailing_address_ward_id = fields.Integer()
    communist_party_status = fields.Boolean(allow_none=True)
    communist_party_entry_date = fields.Date(format='%d-%m-%Y',
                                             allow_none=True)
    union_party_status = fields.Boolean(allow_none=True)
    union_party_entry_date = fields.Date(format='%d-%m-%Y',
                                         allow_none=True)
    teaching_title_id = fields.Integer()
    academic_title_id = fields.Integer()
    degree_id = fields.Integer()

    @validates_schema
    def validate_end_working_date(self, data, **kwargs):
        if data.get('end_working_date'):
            if data['end_working_date'] < data['start_working_date']:
                raise ValidationError('End working date must be greater than '
                                      'or equal Start working date')

    @post_load
    def transform_date(self, data, **kwargs):
        data['dob'] = int(data['dob'].strftime('%s'))
        data['gov_date'] = int(data['gov_date'].strftime('%s'))
        data['start_working_date'] = int(data['start_working_date'].
                                         strftime('%s'))
        if data.get('passport_date'):
            data['passport_date'] = int(data['passport_date'].strftime('%s'))
        if data.get('end_working_date'):
            data['end_working_date'] = int(data['end_working_date'].
                                           strftime('%s'))
        return data
