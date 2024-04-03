from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, SelectField, RadioField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, InputRequired
from main import photos
from main.models import User


class RegisterForm(FlaskForm):

	def validate_username(self, username_to_check):
		user = User.query.filter_by(username=username_to_check.data).first()
		if user:
			raise ValidationError('User already exists! Please try a different username')

	def validate_email_address(self, email_address_to_check):
		email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
		if email_address:
			raise ValidationError('Email Address already exists! Please try a different Email Address')

	username = StringField('', [Length(min=2, max=30), DataRequired()])
	email_address = EmailField('', validators=[Email(), DataRequired()])
	password1 = PasswordField('', [Length(min=6), DataRequired()])
	confirm = PasswordField('', [EqualTo('password1', 'รหัสผ่านไม่ตรงกัน')])
	employee_id = StringField('', [Length(max=10), DataRequired()])
	user_lavel = StringField('', [Length(max=1), DataRequired()])
	submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
	username = StringField('', [DataRequired()])
	password = PasswordField('', [DataRequired()])
	submit = SubmitField(label='Sign in')


class PurchaseItemForm(FlaskForm):
	submit = SubmitField(label='Purchase Item')


class SellItemForm(FlaskForm):
	submit = SubmitField(label='Sell Item')


class ImageUploadForm(FlaskForm):
	photo = FileField(
				label='+',
				validators=[
					FileAllowed(photos, 'Only images are allowed'),
					FileRequired('File field should not be empty')
				]
			)
	submit = SubmitField('Upload')


class GeneralForm(FlaskForm):
	employee_id = StringField('', validators=[Length(min=10, max=13), InputRequired(message="กรุณากรอกข้อมูล")])
	title = SelectField('', [DataRequired()], coerce=str)
	first_name_th = StringField('', [Length(max=30), DataRequired()])
	last_name_th = StringField('', [Length(max=50), DataRequired()])
	first_name = StringField('', [Length(max=30)])
	last_name = StringField('', [Length(max=50)])
	birth_date = StringField('', [Length(max=10)])
	height = StringField('', [Length(max=6)])
	weight = StringField('', [Length(max=6)])
	telephone = StringField('', [Length(max=12)])
	nationality = SelectField('', [DataRequired()], coerce=str)
	ethnicity = SelectField('', [DataRequired()], coerce=str)
	religion = SelectField('', coerce=str)
	personal_id = StringField('', [Length(max=17), DataRequired()])
	issue_date = StringField('', [Length(max=10)])
	expired_date = StringField('', [Length(max=10)])


class RegisterAddressForm(FlaskForm):
	register_address_house_number = StringField('', [Length(min=1, max=10), DataRequired()])
	register_address_village_number = StringField('', [Length(max=3)])
	register_address_subdistrict = SelectField('', [DataRequired()], coerce=str)
	register_address_district = SelectField('', [DataRequired()], coerce=str)
	register_address_province = SelectField('', [DataRequired()], coerce=str)


class ActualAddressForm(FlaskForm):
	actual_address_house_number = StringField('', [Length(min=1, max=10), DataRequired()])
	actual_address_village_number = StringField('', [Length(max=3)])
	actual_address_subdistrict = SelectField('', [DataRequired()], coerce=str)
	actual_address_district = SelectField('', [DataRequired()], coerce=str)
	actual_address_province = SelectField('', [DataRequired()], coerce=str)


class FatherForm(FlaskForm):
	father_title = SelectField('', coerce=str)
	father_first_name = StringField('', [Length(max=30), DataRequired()])
	father_last_name = StringField('', [Length(max=50), DataRequired()])
	father_age = IntegerField('', [Length(max=3)])
	father_occupation = StringField('', [Length(max=30)])
	father_telephone = StringField('', [Length(max=12)])


class MotherForm(FlaskForm):
	mother_title = SelectField('', coerce=str)
	mother_first_name = StringField('', [Length(max=30), DataRequired()])
	mother_last_name = StringField('', [Length(max=50), DataRequired()])
	mother_age = IntegerField('', [Length(max=3)])
	mother_occupation = StringField('', [Length(max=30)])
	mother_telephone = StringField('', [Length(max=12)])


class ClanForm(FlaskForm):
	sibling_number = StringField('', [Length(max=2)], default='0')
	brother_number = StringField('', [Length(max=2)], default='0')
	sister_number = StringField('', [Length(max=2)], default='0')


class FamilyForm(FlaskForm):
	marital_status = RadioField('', coerce=str)
	children_number = StringField('', [Length(max=2)], default='0')
	son_number = StringField('', [Length(max=2)], default='0')
	daughter_number = StringField('', [Length(max=2)], default='0')
	spouse_title = SelectField('', coerce=str)
	spouse_first_name = StringField('', [Length(max=30)])
	spouse_last_name = StringField('', [Length(max=50)])
	spouse_age = IntegerField('', [Length(max=3)])
	spouse_telephone = StringField('', [Length(max=12)])


class HealthDataForm(FlaskForm):
	blood_group = SelectField('', coerce=str)
	sso = SelectField('', coerce=str)
	sso_hospital = StringField('', [Length(max=30)])
	sick_accident = SelectField('', coerce=str)
	sick_accident_cause = StringField('', [Length(max=30)])
	congenital_disease = SelectField('', coerce=str)
	congenital_disease_name = StringField('', [Length(max=30)])
	disability = SelectField('', coerce=str)
	disability_organ = StringField('', [Length(max=30)])


class EmergencyContactForm(FlaskForm):
	emergency_contact_title = SelectField('', coerce=str)
	emergency_contact_first_name = StringField('', [Length(max=30)])
	emergency_contact_last_name = StringField('', [Length(max=50)])
	emergency_contact_occupation = StringField('', [Length(max=30)])
	emergency_contact_relationship = StringField('', [Length(max=30)])
	emergency_contact_house_number = StringField('', [Length(min=1, max=10), DataRequired()])
	emergency_contact_village_number = StringField('', [Length(max=3)])
	emergency_contact_subdistrict = SelectField('', [DataRequired()], coerce=str)
	emergency_contact_district = SelectField('', [DataRequired()], coerce=str)
	emergency_contact_province = SelectField('', [DataRequired()], coerce=str)
	emergency_contact_telephone = StringField('', [Length(max=12)])


class TalentForm(FlaskForm):
	thai_typing_time = StringField('', [Length(max=3)])
	eng_typing_time = StringField('', [Length(max=3)])
	program = StringField('', [Length(max=100)])
	driving_license = StringField('', [Length(max=8)])
	motorcycle_license = StringField('', [Length(max=8)])
	forklift_trained_from = StringField('', [Length(max=50)])


class TupleForm(FlaskForm):
	educationTuple = StringField('', [Length(max=200)])
	workHistoryTuple = StringField('', [Length(max=200)])