from collections import Counter

from marshmallow import ValidationError

from src.validator.schema import UserSchema
from src.validator.schema import _HEADERS

from src.validator.errors import MissingHeadersError


class Validator:

    valid_stream = list()
    bad_stream = list()
    duplicate_stream = list()
    stats = Counter()
    _PROVINCES = {}
    _DISTRICTS = {}
    _WARDS = {}
    _WORKING_STATUS = {}
    _USER_TYPE = {}
    _GENDER = {}
    _PERMISSION_PROFILE = {}
    _CONTRACT = {}
    _ETHNICS = {}
    _RELIGION = {}
    _TEACHING_TITLE = {}
    _ACADEMIC_TITLE = {}
    _DEGREE = {}
    _EMAILS = set()

    def __init__(self, instance):
        self.first_name = instance.first_name
        self.middle_name = instance.middle_name
        self.last_name = instance.last_name
        self.code = instance.staff_id
        self.dob = instance.date_of_birth
        self.work_email = instance.work_email
        self.phone = instance.phone_number
        self.tax_code = instance.tax_code
        self.social_code = instance.social_code
        self.gov_id = instance.government_id
        self.gov_date = instance.government_issued_date
        self.gov_place = instance.government_issued_place
        self.passport_id = instance.passport_id
        self.passport_date = instance.passport_issued_date
        self.passport_place = instance.passport_issued_place
        self.start_working_date = instance.start_working_date
        self.end_working_date = instance.end_working_date
        self.type = instance.user_type
        self.gender = instance.gender
        self.working_status_id = instance.working_status
        self.permission_profile_id = instance.permission_profile
        self.employment_contract_id = instance.employment_contract
        self.birthplace = instance.birthplace
        self.hometown = instance.hometown
        self.ethnics_id = instance.ethnics
        self.religion_id = instance.religion
        self.permanent_address = instance.permanent_address
        self.permanent_address_province_id = instance.permanent_address_province
        self.permanent_address_district_id = instance.permanent_address_district
        self.permanent_address_ward_id = instance.permanent_address_ward
        self.mailing_address = instance.mailing_address
        self.mailing_address_province_id = instance.mailing_address_province
        self.mailing_address_district_id = instance.mailing_address_district
        self.mailing_address_ward_id = instance.mailing_address_ward
        self.communist_party_status = instance.communist_party_status
        self.communist_party_entry_date = instance.communist_party_entry_date
        self.union_party_status = instance.trade_union_status
        self.union_party_entry_date = instance.trade_union_entry_date
        self.teaching_title_id = instance.teaching_title
        self.academic_title_id = instance.academic_title
        self.degree_id = instance.degree
        self.validate()

    @property
    def gov_place(self):
        return self._gov_place

    @gov_place.setter
    def gov_place(self, value):
        self._gov_place = self._PROVINCES.get(value)

    @property
    def passport_place(self):
        return self._passport_place

    @passport_place.setter
    def passport_place(self, value):
        if value:
            self._passport_place = self._PROVINCES.get(value)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = self._USER_TYPE.get(value)

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = self._GENDER.get(value)

    @property
    def working_status_id(self):
        return self._working_status_id

    @working_status_id.setter
    def working_status_id(self, value):
        self._working_status_id = self._WORKING_STATUS.get(value)

    @property
    def permission_profile_id(self):
        return self._permission_profile_id

    @permission_profile_id.setter
    def permission_profile_id(self, value):
        self._permission_profile_id = self._PERMISSION_PROFILE.get(value)

    @property
    def employment_contract_id(self):
        return self._employment_contract_id

    @employment_contract_id.setter
    def employment_contract_id(self, value):
        self._employment_contract_id = self._CONTRACT.get(value)

    @property
    def birthplace(self):
        return self._birthplace

    @birthplace.setter
    def birthplace(self, value):
        self._birthplace = self._PROVINCES.get(value)

    @property
    def hometown(self):
        return self._hometown

    @hometown.setter
    def hometown(self, value):
        self._hometown = self._PROVINCES.get(value)

    @property
    def ethnics_id(self):
        return self._ethnics_id

    @ethnics_id.setter
    def ethnics_id(self, value):
        self._ethnics_id = self._ETHNICS.get(value)

    @property
    def religion_id(self):
        return self._religion_id

    @religion_id.setter
    def religion_id(self, value):
        self._religion_id = self._ETHNICS.get(value)

    @property
    def permanent_address_province_id(self):
        return self._permanent_address_province_id

    @permanent_address_province_id.setter
    def permanent_address_province_id(self, value):
        self._permanent_address_province_id = self._PROVINCES.get(value)

    @property
    def permanent_address_district_id(self):
        return self._permanent_address_district_id

    @permanent_address_district_id.setter
    def permanent_address_district_id(self, value):
        self._permanent_address_district_id = self._DISTRICTS.get(value)

    @property
    def permanent_address_ward_id(self):
        return self._permanent_address_ward_id

    @permanent_address_ward_id.setter
    def permanent_address_ward_id(self, value):
        self._permanent_address_ward_id = self._WARDS.get(value)

    @property
    def mailing_address_province_id(self):
        return self._mailing_address_province_id

    @mailing_address_province_id.setter
    def mailing_address_province_id(self, value):
        self._mailing_address_province_id = self._PROVINCES.get(value)

    @property
    def mailing_address_district_id(self):
        return self._mailing_address_district_id

    @mailing_address_district_id.setter
    def mailing_address_district_id(self, value):
        self._mailing_address_district_id = self._DISTRICTS.get(value)

    @property
    def mailing_address_ward_id(self):
        return self._mailing_address_ward_id

    @mailing_address_ward_id.setter
    def mailing_address_ward_id(self, value):
        self._mailing_address_ward_id = self._WARDS.get(value)

    @property
    def teaching_title_id(self):
        return self._teaching_title_id

    @teaching_title_id.setter
    def teaching_title_id(self, value):
        self._teaching_title_id = self._TEACHING_TITLE.get(value)

    @property
    def academic_title_id(self):
        return self._academic_title_id

    @academic_title_id.setter
    def academic_title_id(self, value):
        self._academic_title_id = self._ACADEMIC_TITLE.get(value)

    @property
    def degree_id(self):
        return self._degree_id

    @degree_id.setter
    def degree_id(self, value):
        self._degree_id = self._DEGREE.get(value)

    def validate(self):
        validator = UserSchema()
        temp = validator.dump(self)
        try:
            self.stats['total'] += 1
            obj = validator.load(temp)
        except ValidationError as e:
            self.bad_stream.append({
                'data': self,
                'errors': e.messages
            })
            self.stats['failed'] += 1
        else:
            self.valid_stream.append(obj)

    def check_duplicate(self):
        return filter(
            lambda record: record.get('work_email') in self._EMAILS,
            self.valid_stream
        )

    @staticmethod
    def validate_headers(headers):
        missing_headers = _HEADERS.difference(headers)
        if missing_headers:
            msg = (
                " ".join(field.split('_')).capitalize()
                for field in missing_headers
            )
            raise MissingHeadersError(f'{",".join(msg)}')
