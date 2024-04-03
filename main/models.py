from main import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    employee_id = db.Column(db.String(length=10), nullable=False)
    user_lavel = db.Column(db.Integer(), nullable=False, default=1)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}฿"
        else:
            return f"{self.budget}฿"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items


# general data for employee
class General(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=False, unique=True)  # รหัสพนักงาน
    title = db.Column(db.String(length=3),nullable=False)  # คำนำหน้าชื่อ
    first_name_th = db.Column(db.String(length=30), nullable=False)
    last_name_th = db.Column(db.String(length=50), nullable=False)
    first_name = db.Column(db.String(length=30), nullable=True)
    last_name = db.Column(db.String(length=50), nullable=True)
    birth_date = db.Column(db.String(length=10), nullable=False)
    height = db.Column(db.String(length=6), nullable=True)
    weight = db.Column(db.String(length=6), nullable=True)
    telephone = db.Column(db.String(length=12), nullable=True)
    nationality = db.Column(db.String(length=3), nullable=False)  # สัญชาติ
    ethnicity = db.Column(db.String(length=3), nullable=False)  # เชิ้อชาติ
    religion = db.Column(db.String(length=2), nullable=False)  # ศาสนา
    personal_id = db.Column(db.String(length=17), nullable=False)  # เลขบัตรประชาชน
    issue_date = db.Column(db.String(length=10), nullable=True)  # วันที่ออกบัตร
    expired_date = db.Column(db.String(length=10), nullable=True)  # วันที่บัตรหมดอายุ


# Address information registered on the national ID card
class RegisterAddress(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=False, unique=True)  # รหัสพนักงาน
    register_address_house_number = db.Column(db.String(length=10), nullable=False)
    register_address_village_number = db.Column(db.String(length=3), nullable=False)
    register_address_subdistrict = db.Column(db.String(length=6), nullable=False)
    register_address_district = db.Column(db.String(length=4), nullable=False)
    register_address_province = db.Column(db.String(length=2), nullable=False)


# Actual address information
class ActualAddress(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=False, unique=True)  # รหัสพนักงาน
    actual_address_house_number = db.Column(db.String(length=10), nullable=False)
    actual_address_village_number = db.Column(db.String(length=3), nullable=False)
    actual_address_subdistrict = db.Column(db.String(length=6), nullable=False)
    actual_address_district = db.Column(db.String(length=4), nullable=False)
    actual_address_province = db.Column(db.String(length=2), nullable=False)


# Information of employee's father
class Father(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=False, unique=True)
    father_title = db.Column(db.String(length=3), nullable=False)
    father_first_name = db.Column(db.String(length=30), nullable=False)
    father_last_name = db.Column(db.String(length=50), nullable=False)
    father_age = db.Column(db.Integer(), nullable=True)
    father_occupation = db.Column(db.String(length=30), nullable=True)
    father_telephone = db.Column(db.String(length=12), nullable=True)


# Information of employee's father
class Mother(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=False, unique=True)
    mother_title = db.Column(db.String(length=3), nullable=False)
    mother_first_name = db.Column(db.String(length=30), nullable=False)
    mother_last_name = db.Column(db.String(length=50), nullable=False)
    mother_age = db.Column(db.Integer(), nullable=True)
    mother_occupation = db.Column(db.String(length=30), nullable=True)
    mother_telephone = db.Column(db.String(length=12), nullable=True)


# Information of employee's father
class Clan(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=False, unique=True)
    sibling_number = db.Column(db.String(length=2), nullable=True)
    brother_number = db.Column(db.String(length=2), nullable=True)
    sister_number = db.Column(db.String(length=2), nullable=True)


# Information of employee's family
class Family(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=False, unique=True)
    marital_status = db.Column(db.String(length=1), nullable=True)
    children_number = db.Column(db.String(length=2), nullable=True)
    son_number = db.Column(db.String(length=2), nullable=True)
    daughter_number = db.Column(db.String(length=2), nullable=True)
    spouse_title = db.Column(db.String(length=3), nullable=True)
    spouse_first_name = db.Column(db.String(length=30), nullable=True)
    spouse_last_name = db.Column(db.String(length=50), nullable=True)
    spouse_age = db.Column(db.Integer(), nullable=True)
    spouse_telephone = db.Column(db.String(length=12), nullable=True)


# Information of employee's education
class EducationRecord(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    employee_id = db.Column(db.String(length=13), nullable=True,)
    education_level = db.Column(db.String(length=1), nullable=True)
    school_name = db.Column(db.String(length=60), nullable=True)
    graduation_year = db.Column(db.String(length=4), nullable=True)
    faculty = db.Column(db.String(length=60), nullable=True)
    major = db.Column(db.String(length=60), nullable=True)
    average_grade = db.Column(db.String(length=5), nullable=True)


# Information of employee's work history
class WorkHistory(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    employee_id = db.Column(db.String(length=13), nullable=True)
    company_name = db.Column(db.String(length=60), nullable=True)
    position = db.Column(db.String(length=60), nullable=True)
    begin_year = db.Column(db.String(length=4), nullable=True)
    end_year = db.Column(db.String(length=4), nullable=True)
    reason = db.Column(db.String(length=100), nullable=True)


# Information of employee's health data
class HealthData(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=True, unique=True)
    blood_group = db.Column(db.String(length=1), nullable=True)
    sso = db.Column(db.String(length=1), nullable=True)
    sso_hospital = db.Column(db.String(length=30), nullable=True)
    sick_accident = db.Column(db.String(length=1), nullable=True)
    sick_accident_cause = db.Column(db.String(length=30), nullable=True)
    congenital_disease = db.Column(db.String(length=1), nullable=True)
    congenital_disease_name = db.Column(db.String(length=30), nullable=True)
    disability = db.Column(db.String(length=1), nullable=True)
    disability_organ = db.Column(db.String(length=30), nullable=True)


# Information of employee's mergency contact
class EmergencyContact(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=True, unique=True)
    emergency_contact_title = db.Column(db.String(length=3), nullable=False)
    emergency_contact_first_name = db.Column(db.String(length=30), nullable=False)
    emergency_contact_last_name = db.Column(db.String(length=50), nullable=False)
    emergency_contact_relationship = db.Column(db.String(length=30), nullable=True)
    emergency_contact_occupation = db.Column(db.String(length=30), nullable=True)
    emergency_contact_house_number = db.Column(db.String(length=10), nullable=False)
    emergency_contact_village_number = db.Column(db.String(length=3), nullable=False)
    emergency_contact_subdistrict = db.Column(db.String(length=6), nullable=False)
    emergency_contact_district = db.Column(db.String(length=4), nullable=False)
    emergency_contact_province = db.Column(db.String(length=2), nullable=False)
    emergency_contact_telephone = db.Column(db.String(length=12), nullable=True)


# Information of employee's talent
class Talent(db.Model):
    employee_id = db.Column(db.String(length=13), primary_key=True, nullable=True, unique=True)
    thai_typing = db.Column(db.String(length=1), nullable=True)
    thai_typing_time = db.Column(db.String(length=3), nullable=True)
    eng_typing = db.Column(db.String(length=1), nullable=True)
    eng_typing_time = db.Column(db.String(length=3), nullable=True)
    computer = db.Column(db.String(length=1), nullable=True)
    program = db.Column(db.String(length=100), nullable=True)
    driving = db.Column(db.String(length=1), nullable=True)
    driving_license = db.Column(db.String(length=8), nullable=True)
    motorcycling = db.Column(db.String(length=1), nullable=True)
    motorcycle_license = db.Column(db.String(length=8), nullable=True)
    forklift_driving = db.Column(db.String(length=1), nullable=True)
    forklift_trained_from = db.Column(db.String(length=50), nullable=True)
    welding = db.Column(db.String(length=1), nullable=True)
    cement = db.Column(db.String(length=1), nullable=True)
    electrical = db.Column(db.String(length=1), nullable=True)
    maintenance = db.Column(db.String(length=1), nullable=True)
    qc = db.Column(db.String(length=1), nullable=True)
    sewing = db.Column(db.String(length=1), nullable=True)


class BloodGroup(db.Model):
    code = db.Column(db.String(length=1), primary_key=True)
    name = db.Column(db.String(length=40), nullable=False)


class Education_level(db.Model):
    code = db.Column(db.String(length=1), primary_key=True)
    name = db.Column(db.String(length=40), nullable=False)


class Marital_status(db.Model):
    code = db.Column(db.String(length=1), primary_key=True)
    name = db.Column(db.String(length=13), nullable=False)


class Subdistrict(db.Model):
    code = db.Column(db.String(length=6), primary_key=True)
    zipcode = db.Column(db.String(length=5), nullable=False)
    name_th = db.Column(db.String(length=30), nullable=False)
    name_eng = db.Column(db.String(length=30), nullable=False)
    district_code = db.Column(db.String(length=4), nullable=False)


class District(db.Model):
    code = db.Column(db.String(length=4), primary_key=True)
    name_th = db.Column(db.String(length=30), nullable=False)
    name_eng = db.Column(db.String(length=30), nullable=False)
    province_code = db.Column(db.String(length=2), nullable=False)


class Provinces (db.Model):
    code = db.Column(db.String(length=2), primary_key=True)
    name_th = db.Column(db.String(length=30), nullable=False)
    name_th_short = db.Column(db.String(length=2), nullable=False)
    name_eng = db.Column(db.String(length=30), nullable=False)
    geography_id = db.Column(db.String(length=1), nullable=False)


class Title(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(length=3), nullable=False)
    name_eng = db.Column(db.String(length=10), nullable=False)
    name_th = db.Column(db.String(length=10), nullable=False)


class Nationality(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(length=3), nullable=False)
    name_th = db.Column(db.String(length=50), nullable=False)
    name_en = db.Column(db.String(length=50), nullable=False)


class Religion(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(length=2), nullable=False)
    name_th = db.Column(db.String(length=50), nullable=False)
    name_en = db.Column(db.String(length=50), nullable=False)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
