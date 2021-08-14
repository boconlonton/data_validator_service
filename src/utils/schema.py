from marshmallow import Schema
from marshmallow import fields
from marshmallow import validates_schema
from marshmallow import validate
from marshmallow import ValidationError
from marshmallow import post_load


class UserSchema(Schema):
    first_name = fields.String(validate=validate.Length(min=1, max=50))
    middle_name = fields.String(validate=validate.Length(min=1, max=50), allow_none=True)
    last_name = fields.String(validate=validate.Length(min=1, max=50))
    staff_id = fields.String(validate=validate.Length(min=1, max=15))
    dob = fields.Date(format='%d-%m-%Y')
    work_email = fields.Email(validate=validate.Length(min=5, max=50))
    phone_number = fields.String(validate=validate.Length(min=8, max=20))
    tax_code = fields.String(validate=validate.Length(min=5, max=12), allow_none=True)
    social_code = fields.String(validate=validate.Length(min=5, max=12), allow_none=True)
    gov_id = fields.String(validate=validate.Length(min=1, max=20))
    gov_date = fields.Date(format='%d-%m-%Y')
    gov_place = fields.Integer(allow_none=True)
    passport_id = fields.String(validate=validate.Length(min=1, max=20), allow_none=True)
    passport_date = fields.Date(format='%d-%m-%Y', allow_none=True)
    passport_place = fields.Integer(allow_none=True)
    start_working_date = fields.Date(format='%d-%m-%Y')
    end_working_date = fields.Date(format='%d-%m-%Y', allow_none=True)
    user_type = fields.Integer()
    gender = fields.Integer()
    working_status = fields.String()

    # @validates_schema
    # def validate_choices(self, data):
    #     # TODO: Define validation for optional fields if exists
    #     # gov_place, passport_place
    #     # working_status
    #     pass

    @validates_schema
    def validate_end_working_data(self, data, **kwargs):
        if data.get('end_working_date'):
            if data['end_working_date'] < data['start_working_date']:
                raise ValidationError('End working date must be greater than or equal Start working date')

    @post_load
    def transform_date(self, data, **kwargs):
        data['dob'] = int(data['dob'].strftime('%s'))
        data['gov_date'] = int(data['gov_date'].strftime('%s'))
        data['start_working_date'] = int(data['start_working_date'].strftime('%s'))
        if data.get('passport_date'):
            data['passport_date'] = int(data['passport_date'].strftime('%s'))
        if data.get('end_working_date'):
            data['end_working_date'] = int(data['end_working_date'].strftime('%s'))
        return data
