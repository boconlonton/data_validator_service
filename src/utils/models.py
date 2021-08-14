province = {
    'Ha Noi': 1,
    'TPHCM': 2,
    'Dong Nai': 3
}

user_type_choices = {
    'Staff': 1,
    'Teacher': 2
}

gender_choices = {
    'Male': 0,
    'Female': 1,
    'Others': 2
}

working_status_choices = {
    'Probation': 0,
    'Working': 1
}


class User:

    def __init__(self, instance):
        self.first_name = instance.first_name
        self.middle_name = instance.middle_name
        self.last_name = instance.last_name
        self.staff_id = instance.staff_id
        self.dob = instance.dob
        self.work_email = instance.work_email
        self.phone_number = instance.phone_number
        self.tax_code = instance.tax_code
        self.social_code = instance.social_code
        self.gov_id = instance.gov_id
        self.gov_date = instance.gov_date
        self.gov_place = instance.gov_place
        self.passport_id = instance.passport_id
        self.passport_date = instance.passport_date
        self.passport_place = instance.passport_place
        self.start_working_date = instance.start_working_date
        self.end_working_date = instance.end_working_date
        self.user_type = instance.user_type
        self.gender = instance.gender
        self.working_status = instance.working_status

    @property
    def gov_place(self):
        return self._gov_place

    @gov_place.setter
    def gov_place(self, value):
        self._gov_place = province.get(value)

    @property
    def passport_place(self):
        return self._passport_place

    @passport_place.setter
    def passport_place(self, value):
        if value:
            self._passport_place = province.get(value)

    @property
    def user_type(self):
        return self._user_type

    @user_type.setter
    def user_type(self, value):
        self._user_type = user_type_choices.get(value)

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = gender_choices.get(value)

    @property
    def working_status(self):
        return self._working_status

    @working_status.setter
    def working_status(self, value):
        self._working_status = working_status_choices.get(value)
