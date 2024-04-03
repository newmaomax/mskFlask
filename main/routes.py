import os
from main import app, photos
from flask import render_template, redirect, url_for, flash, request, send_from_directory, jsonify
from main.models import (Item, User,
                         General, Title, Nationality, Religion,
                         RegisterAddress, ActualAddress, Subdistrict, District, Provinces,
                         Father, Mother, Clan, Family, Marital_status, Education_level, EducationRecord,
                         WorkHistory, HealthData, BloodGroup, EmergencyContact, Talent)

from main.forms import (RegisterForm, LoginForm, PurchaseItemForm, SellItemForm,
                        GeneralForm, ImageUploadForm, RegisterAddressForm, ActualAddressForm,
                        FatherForm, MotherForm, ClanForm, FamilyForm, HealthDataForm, EmergencyContactForm,
                        TalentForm, TupleForm)
from main import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime


@app.route('/')
@app.route('/home')
# @login_required
def home_page():
    return render_template('home.html')


books = []


@app.route('/book', methods=['POST', 'GET'])
def book():
    if request.method == 'POST':
        body = request.get_json()
        books.append(body)

        return {"message": "Book already add to database", "body": body}, 201
    elif request.method == 'GET':
        return {"books": books}, 200


@app.route('/employee', methods=['GET', 'POST'])
@login_required
def employee_page():
    return render_template('employee.html')


@app.route('/thaiEmployee')
@login_required
def thai_employee_page():
    return render_template('thaiEmployee.html')


@app.route('/<filename>')
@login_required
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/save', methods=['GET', 'POST'])
def save(): #โมดูลแสดงข้อมูล
    tuple_form = TupleForm()
    general_form = GeneralForm()

    # getEducation = request.form.get('educationTuple')
    getEducation = tuple_form.educationTuple.data
    # getEducation = "test"
    getWorkHistory = request.form.get('workHistoryTuple')

    # x = request.args.get('employee_id')

    """qry = db.session.query(General).filter(
        General.employee_id == 'msk-670018')
    data = qry.first()"""

    """nationalities = [(nationality.code, nationality.name_th) for nationality in
                     Nationality.query.filter(Nationality.code.in_([98, 99, 264, 265, 266])).all()]"""

    # return f"employee_id= {x}"
    return getEducation

@app.route('/addThaiEmployee', methods=['GET', 'POST'])
@login_required
def add_thai_employee_page():
    test_date = datetime.utcnow()
    # css var
    main_card = "card card-body col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11 col-xxl-11  mx-3 my-3 myForm"
    date_group = " col-11 col-sm-11 col-md-11 col-lg-3 col-xl-2 col-xxl-2 mx-0"

    # calling form
    image_form = ImageUploadForm()
    general_form = GeneralForm()
    register_address_form = RegisterAddressForm()
    actual_address_form = ActualAddressForm()
    father_form = FatherForm()
    mother_form = MotherForm()
    clan_form = ClanForm()
    family_form = FamilyForm()
    health_data_form = HealthDataForm()
    emergency_contact_form = EmergencyContactForm()
    talent_form = TalentForm()
    tuple_form = TupleForm()

    # call resource
    titles = [(t.code, t.name_th) for t in Title.query.all()]
    general_form.title.choices = titles
    father_form.father_title.choices = titles
    mother_form.mother_title.choices = titles
    family_form.spouse_title.choices = titles
    emergency_contact_form.emergency_contact_title.choices = titles

    nationalities = [(nationality.code, nationality.name_th) for nationality in Nationality.query.filter(Nationality.code.in_(['TH', 'LA', 'MM', 'KH'])).all()]
    general_form.nationality.choices = nationalities

    ethnicities = [(nationality.code, nationality.name_th) for nationality in Nationality.query.all()]
    general_form.ethnicity.choices = ethnicities
    # ethnicities = Nationality.query.filter(Nationality.th_name.like('%ไทย%'))

    religions = [(religion.code, religion.name_th) for religion in Religion.query.all()]
    general_form.religion.choices = religions

    subdistricts = [(subdistrict.code, f"{subdistrict.zipcode}-{subdistrict.name_th}") for subdistrict in Subdistrict.query.all()]
    register_address_form.register_address_subdistrict.choices = subdistricts
    actual_address_form.actual_address_subdistrict.choices = subdistricts
    emergency_contact_form.emergency_contact_subdistrict.choices = subdistricts

    districts = [(district.code, district.name_th) for district in District.query.all()]
    register_address_form.register_address_district.choices = districts
    actual_address_form.actual_address_district.choices = districts
    emergency_contact_form.emergency_contact_district.choices = districts

    provinces = [(province.code, province.name_th) for province in Provinces.query.all()]
    register_address_form.register_address_province.choices = provinces
    actual_address_form.actual_address_province.choices = provinces
    emergency_contact_form.emergency_contact_province.choices = provinces

    maritalStatus = [(m.code, m.name) for m in Marital_status.query.all()]
    family_form.marital_status.choices = maritalStatus

    education_level_code = [e.code for e in Education_level.query.all()]
    education_level_name = [e.name for e in Education_level.query.all()]

    bloodGroup = [(b.code, b.name) for b in BloodGroup.query.all()]
    health_data_form.blood_group.choices = bloodGroup

    getEducation = request.form.get('educationTuple')
    getWorkHistory = request.form.get('workHistoryTuple')

    eduModel = []
    worModel = []

    get_thaiTypingCheck = request.form.get('thaiTypingCheck')
    get_engTypingCheck = request.form.get('engTypingCheck')
    get_computerCheck = request.form.get('computerCheck')
    get_carCheck = request.form.get('carCheck')
    get_motorcycleCheck = request.form.get('motorcycleCheck')
    get_forkliftCheck = request.form.get('forkliftCheck')
    get_weldingCheck = request.form.get('weldingCheck')
    get_cementCheck = request.form.get('cementCheck')
    get_electricalCheck = request.form.get('electricalCheck')
    get_maintenanceCheck = request.form.get('maintenanceCheck')
    get_qcCheck = request.form.get('qcCheck')
    get_sewingCheck = request.form.get('sewingCheck')

    # if general_form.validate_on_submit():
    if request.method == "POST":
        check_em_id = General.query.filter(General.employee_id.like(general_form.employee_id.data)).all()
        get_ssoCheck = request.form.get('ssoCheck')
        if check_em_id:
            flash(f'เลขที่ประจำตัวพนักงานถูกใช้แล้ว{check_em_id}//{get_ssoCheck}', category='danger')
            file_url = None
            return redirect(url_for(f'add_thai_employee_page'))
        else:
            # Enter data in the general table.
            general_to_create = General(
                employee_id=general_form.employee_id.data,
                title=general_form.title.data,
                first_name_th=general_form.first_name_th.data,
                last_name_th=general_form.last_name_th.data,
                first_name=general_form.first_name.data,
                last_name=general_form.last_name.data,
                birth_date=general_form.birth_date.data,
                height=general_form.height.data,
                weight=general_form.weight.data,
                telephone=general_form.telephone.data,
                nationality=general_form.nationality.data,
                ethnicity=general_form.ethnicity.data,
                religion=general_form.religion.data,
                personal_id=general_form.personal_id.data,
                issue_date=general_form.issue_date.data,
                expired_date=general_form.expired_date.data
            )
            db.session.add(general_to_create)

            # Enter data in the register_address table.
            register_address_to_create = RegisterAddress(
                employee_id=general_form.employee_id.data,
                register_address_house_number=register_address_form.register_address_house_number.data,
                register_address_village_number=register_address_form.register_address_village_number.data,
                register_address_subdistrict=register_address_form.register_address_subdistrict.data,
                register_address_district=register_address_form.register_address_district.data,
                register_address_province=register_address_form.register_address_province.data
            )
            db.session.add(register_address_to_create)

            # Enter data in the actual_address table.
            actual_address_to_create = ActualAddress(
                employee_id=general_form.employee_id.data,
                actual_address_house_number=actual_address_form.actual_address_house_number.data,
                actual_address_village_number=actual_address_form.actual_address_village_number.data,
                actual_address_subdistrict=actual_address_form.actual_address_subdistrict.data,
                actual_address_district=actual_address_form.actual_address_district.data,
                actual_address_province=actual_address_form.actual_address_province.data
            )
            db.session.add(actual_address_to_create)

            # Enter data in the father table.
            father_to_create = Father(
                employee_id=general_form.employee_id.data,
                father_title=father_form.father_title.data,
                father_first_name=father_form.father_first_name.data,
                father_last_name=father_form.father_last_name.data,
                father_age=father_form.father_age.data,
                father_occupation=father_form.father_occupation.data,
                father_telephone=father_form.father_telephone.data
            )
            db.session.add(father_to_create)

            # Enter data in the mother table.
            mother_to_create = Mother(
                employee_id=general_form.employee_id.data,
                mother_title=mother_form.mother_title.data,
                mother_first_name=mother_form.mother_first_name.data,
                mother_last_name=mother_form.mother_last_name.data,
                mother_age=mother_form.mother_age.data,
                mother_occupation=mother_form.mother_occupation.data,
                mother_telephone=mother_form.mother_telephone.data
            )
            db.session.add(mother_to_create)

            # Enter data in the clan table.
            clan_to_create = Clan(
                employee_id=general_form.employee_id.data,
                sibling_number=clan_form.sibling_number.data,
                brother_number=clan_form.brother_number.data,
                sister_number=clan_form.sister_number.data
            )
            db.session.add(clan_to_create)

            # Enter data in the family table.
            family_to_create = Family(
                employee_id=general_form.employee_id.data,
                marital_status=family_form.marital_status.data,
                children_number=family_form.children_number.data,
                son_number=family_form.son_number.data,
                daughter_number=family_form.daughter_number.data,
                spouse_title=family_form.spouse_title.data,
                spouse_first_name=family_form.spouse_first_name.data,
                spouse_last_name=family_form.spouse_last_name.data,
                spouse_age=family_form.spouse_age.data,
                spouse_telephone=family_form.spouse_telephone.data
            )
            db.session.add(family_to_create)

            # Enter data in the health data table.
            if health_data_form.blood_group.data == "":
                blood_group = "9"
            else:
                blood_group = health_data_form.blood_group.data

            if request.form.get('ssoCheck') == None:
                get_ssoCheck = "0"
                health_data_form.sso_hospital.data = "-"
            else:
                get_ssoCheck = request.form.get('ssoCheck')

            if request.form.get('sickAndAccidentCheck') == None:
                get_sickAndAccidentCheck = "0"
                health_data_form.sick_accident_cause.data = "-"
            else:
                get_sickAndAccidentCheck = request.form.get('sickAndAccidentCheck')

            if request.form.get('congenitalDiseaseCheck') == None:
                get_congenitalDiseaseCheck = "0"
                health_data_form.congenital_disease_name.data = "-"
            else:
                get_congenitalDiseaseCheck = request.form.get('congenitalDiseaseCheck')

            if request.form.get('disabilityCheck') == None:
                get_disabilityCheck = "0"
                health_data_form.disability_organ.data = "-"
            else:
                get_disabilityCheck = request.form.get('disabilityCheck')



            health_data_to_create = HealthData(
                employee_id=general_form.employee_id.data,
                blood_group=blood_group,
                sso= get_ssoCheck,
                sso_hospital=health_data_form.sso_hospital.data,
                sick_accident=get_sickAndAccidentCheck,
                sick_accident_cause=health_data_form.sick_accident_cause.data,
                congenital_disease=get_congenitalDiseaseCheck,
                congenital_disease_name=health_data_form.congenital_disease_name.data,
                disability=get_disabilityCheck,
                disability_organ=health_data_form.disability_organ.data
            )
            db.session.add(health_data_to_create)

            # Enter data in the emergency contact table.
            emergency_contact_to_create = EmergencyContact(
                employee_id=general_form.employee_id.data,
                emergency_contact_title=emergency_contact_form.emergency_contact_title.data,
                emergency_contact_first_name=emergency_contact_form.emergency_contact_first_name.data,
                emergency_contact_last_name=emergency_contact_form.emergency_contact_last_name.data,
                emergency_contact_relationship=emergency_contact_form.emergency_contact_relationship.data,
                emergency_contact_occupation=emergency_contact_form.emergency_contact_occupation.data,
                emergency_contact_house_number=emergency_contact_form.emergency_contact_house_number.data,
                emergency_contact_village_number=emergency_contact_form.emergency_contact_village_number.data,
                emergency_contact_subdistrict=emergency_contact_form.emergency_contact_subdistrict.data,
                emergency_contact_district=emergency_contact_form.emergency_contact_district.data,
                emergency_contact_province=emergency_contact_form.emergency_contact_province.data,
                emergency_contact_telephone=emergency_contact_form.emergency_contact_telephone.data
            )
            db.session.add(emergency_contact_to_create)

            # Enter data in the education record table.
            """if getEducation!="None":
                educationList = getEducation.split("&&")
                for i in educationList:
                    data = EducationRecord(
                        employee_id=i.split(",")[0],
                        education_level=i.split(",")[1],
                        school_name=i.split(",")[2],
                        graduation_year=i.split(",")[3],
                        faculty=i.split(",")[4],
                        major=i.split(",")[5],
                        average_grade=i.split(",")[6]
                    )
                    eduModel.append(data)
                db.session.add_all(eduModel)"""

            # Enter data in the work history table.
            """if getWorkHistory != "None":
                workHistoryList = getWorkHistory.split("&&")
                for i in workHistoryList:
                    data = WorkHistory(
                        employee_id=i.split(",")[0],
                        company_name=i.split(",")[1],
                        position=i.split(",")[2],
                        begin_year=i.split(",")[3],
                        end_year=i.split(",")[4],
                        reason=i.split(",")[5]
                    )
                    worModel.append(data)
                db.session.add_all(worModel)"""

            # Enter data in the talent table.
            talent_to_create = Talent(
                employee_id=general_form.employee_id.data,
                thai_typing=get_thaiTypingCheck,
                thai_typing_time=talent_form.thai_typing_time.data,
                eng_typing=get_engTypingCheck,
                eng_typing_time=talent_form.eng_typing_time.data,
                computer=get_computerCheck,
                program=talent_form.program.data,
                driving=get_carCheck,
                driving_license=talent_form.driving_license.data,
                motorcycling=get_motorcycleCheck,
                motorcycle_license=talent_form.motorcycle_license.data,
                forklift_driving=get_forkliftCheck,
                forklift_trained_from=talent_form.forklift_trained_from.data,
                welding=get_weldingCheck,
                cement=get_cementCheck,
                electrical=get_electricalCheck,
                maintenance=get_maintenanceCheck,
                qc=get_qcCheck,
                sewing=get_sewingCheck
            )
            db.session.add(talent_to_create)

            db.session.commit()

            # save employee image
            f_path = photos.path(f"{general_form.employee_id.data}.jpg")
            #f_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads', f"{general_form.employee_id.data}.jpg")

            if os.path.exists(f_path):
                os.remove(f_path)

            filename = photos.save(image_form.photo.data, name=f"{general_form.employee_id.data}.jpg")
            file_url = url_for('get_file', filename=filename)

            # Check errors from general_form
            if general_form.errors != {}:
                for err_msg in general_form.errors.values():
                    flash(f'เกิดข้อผิดพลาดในการสร้าง : {err_msg}//{general_form.employee_id.data}', category='danger')
                    # return redirect(url_for('add_thai_employee_page'))
            else:
                flash(f'ข้อมูลพนักงานของ {general_to_create.employee_id}/{f_path}//{general_form.employee_id.data}', category='success')

            employee_id = general_to_create.employee_id
            # return redirect(url_for('edit_thai_employee_page', employee_id=employee_id))
            return redirect(url_for('show_thai_employee_page', employee_id=employee_id))
    else:
        file_url = None

    return render_template(
        'addThaiEmployee.html',
        image_form=image_form,
        general_form=general_form,
        register_address_form=register_address_form,
        actual_address_form=actual_address_form,
        father_form=father_form,
        mother_form=mother_form,
        clan_form=clan_form,
        family_form=family_form,
        health_data_form=health_data_form,
        emergency_contact_form=emergency_contact_form,
        talent_form=talent_form,
        tuple_form=tuple_form,

        file_url=file_url,
        education_level_code=education_level_code,
        education_level_name=education_level_name
    )


@app.route('/showThaiEmployee/<employee_id>', methods=['GET', 'POST'])
@login_required
def show_thai_employee_page(employee_id):
    # calling form
    image_form = ImageUploadForm()
    general_form = GeneralForm()
    register_address_form = RegisterAddressForm()
    actual_address_form = ActualAddressForm()
    father_form = FatherForm()
    mother_form = MotherForm()
    clan_form = ClanForm()
    family_form = FamilyForm()
    health_data_form = HealthDataForm()
    emergency_contact_form = EmergencyContactForm()
    talent_form = TalentForm()
    tuple_form = TupleForm()

    # call resource
    employee_id = employee_id
    titles = [(t.code, t.name_th) for t in Title.query.all()]
    nationalities = [(nationality.code, nationality.name_th) for nationality in Nationality.query.filter(Nationality.code.in_([98, 99, 264, 265, 266])).all()]
    ethnicities = [(nationality.code, nationality.name_th) for nationality in Nationality.query.all()]
    religions = [(religion.code, religion.name_th) for religion in Religion.query.all()]
    subdistricts = [(subdistrict.code, f"{subdistrict.zipcode}-{subdistrict.name_th}") for subdistrict in Subdistrict.query.all()]
    districts = [(district.code, district.name_th) for district in District.query.all()]
    provinces = [(province.code, province.name_th) for province in Provinces.query.all()]
    maritalStatus = [(m.code, m.name) for m in Marital_status.query.all()]
    bloodGroup = [(b.code, b.name) for b in BloodGroup.query.all()]
    education_level_code = [e.code for e in Education_level.query.all()]
    education_level_name = [e.name for e in Education_level.query.all()]

    getEducation = request.form.get('educationTuple')
    getWorkHistory = request.form.get('workHistoryTuple')

    general_data = db.session.query(General).filter(General.employee_id == employee_id).first()
    ge_title = db.session.query(Title).filter(Title.code == general_data.title).first()
    em_nationality = db.session.query(Nationality).filter(Nationality.code == general_data.nationality).first()
    em_ethnicity = db.session.query(Nationality).filter(Nationality.code == general_data.ethnicity).first()
    em_religion = db.session.query(Religion).filter(Religion.code == general_data.religion).first()

    register_address_data = db.session.query(RegisterAddress).filter(RegisterAddress.employee_id == employee_id).first()
    re_subdistrict = db.session.query(Subdistrict).filter(Subdistrict.code == register_address_data.register_address_subdistrict).first()
    re_district = db.session.query(District).filter(District.code == register_address_data.register_address_district).first()
    re_province = db.session.query(Provinces).filter(Provinces.code == register_address_data.register_address_province).first()

    """re_subdistrict = db.session.query(Subdistrict).filter(Subdistrict.code == "342504").first()
    re_district = db.session.query(District).filter(District.code == "1008").first()
    re_province = db.session.query(Provinces).filter(Provinces.code == "14").first()"""

    actual_address_data = db.session.query(ActualAddress).filter(ActualAddress.employee_id == employee_id).first()
    ac_subdistrict = db.session.query(Subdistrict).filter(Subdistrict.code == actual_address_data.actual_address_subdistrict).first()
    ac_district = db.session.query(District).filter(District.code == actual_address_data.actual_address_district).first()
    ac_province = db.session.query(Provinces).filter(Provinces.code == actual_address_data.actual_address_province).first()

    clan_data = db.session.query(Clan).filter(Clan.employee_id == employee_id).first()
    father_data = db.session.query(Father).filter(Father.employee_id == employee_id).first()
    fa_title = db.session.query(Title).filter(Title.code == father_data.father_title).first()

    mother_data = db.session.query(Mother).filter(Mother.employee_id == employee_id).first()
    mo_title = db.session.query(Title).filter(Title.code == mother_data.mother_title).first()

    family_data = db.session.query(Family).filter(Family.employee_id == employee_id).first()
    fa_maritalStatus = db.session.query(Marital_status).filter(Marital_status.code == family_data.marital_status).first()
    sp_title = db.session.query(Title).filter(Title.code == family_data.spouse_title).first()

    health_data = db.session.query(HealthData).filter(HealthData.employee_id == employee_id).first()
    b_group = db.session.query(BloodGroup).filter(BloodGroup.code == health_data.blood_group).first()

    emergency_contact_data = db.session.query(EmergencyContact).filter(EmergencyContact.employee_id == employee_id).first()
    em_title = db.session.query(Title).filter(Title.code == emergency_contact_data.emergency_contact_title).first()
    em_subdistrict = db.session.query(Subdistrict).filter(Subdistrict.code == emergency_contact_data.emergency_contact_subdistrict).first()
    em_district = db.session.query(District).filter(District.code == emergency_contact_data.emergency_contact_district).first()
    em_province = db.session.query(Provinces).filter(Provinces.code == emergency_contact_data.emergency_contact_province).first()

    education_data = db.session.query(EducationRecord).where(EducationRecord.employee_id == employee_id).all()
    education_level = db.session.query(Education_level).all()

    work_history_data = db.session.query(WorkHistory).where(WorkHistory.employee_id == employee_id).all()
    talent_data = db.session.query(Talent).where(Talent.employee_id == employee_id).first()

    if general_data:
        general_form = GeneralForm(formdata=request.form, obj=general_data)
        general_form.title.choices = titles
        general_form.nationality.choices = nationalities
        general_form.ethnicity.choices = ethnicities
        general_form.religion.choices = religions

        register_address_form = RegisterAddressForm(formdata=request.form, obj=register_address_data)
    else:
        flash(f'เกิดข้อผิดพลาด {employee_id}', category='danger')

    if register_address_data:
        register_address_form = RegisterAddressForm(formdata=request.form, obj=register_address_data)
        register_address_form.register_address_subdistrict.choices = subdistricts
        register_address_form.register_address_district.choices = districts
        register_address_form.register_address_province.choices = provinces
    else:
        flash(f'เกิดข้อผิดพลาด {register_address_data}', category='danger')

    if actual_address_data:
        actual_address_form = ActualAddressForm(formdata=request.form, obj=actual_address_data)
        actual_address_form.actual_address_subdistrict.choices = subdistricts
        actual_address_form.actual_address_district.choices = districts
        actual_address_form.actual_address_province.choices = provinces
    else:
        flash(f'เกิดข้อผิดพลาด {actual_address_data}', category='danger')

    if clan_data:
        clan_form = ClanForm(formdata=request.form, obj=clan_data)
    else:
        flash(f'เกิดข้อผิดพลาด {clan_data}', category='danger')

    if father_data:
        father_form = FatherForm(formdata=request.form, obj=father_data)
        father_form.father_title.choices = titles
    else:
        flash(f'เกิดข้อผิดพลาด {father_data}', category='danger')

    if mother_data:
        mother_form = MotherForm(formdata=request.form, obj=mother_data)
        mother_form.mother_title.choices = titles
    else:
        flash(f'เกิดข้อผิดพลาด {father_data}', category='danger')

    if family_data:
        family_form = FamilyForm(formdata=request.form, obj=family_data)
        family_form.spouse_title.choices = titles
        family_form.marital_status.choices = maritalStatus
    else:
        flash(f'เกิดข้อผิดพลาด {family_data}', category='danger')

    if health_data:
        health_data_form = HealthDataForm(formdata=request.form, obj=health_data)
        health_data_form.blood_group.choices = bloodGroup
    else:
        flash(f'เกิดข้อผิดพลาด {health_data}', category='danger')

    if emergency_contact_data:
        emergency_contact_form = EmergencyContactForm(formdata=request.form, obj=emergency_contact_data)
        emergency_contact_form.emergency_contact_title.choices = titles
        emergency_contact_form.emergency_contact_subdistrict.choices = subdistricts
        emergency_contact_form.emergency_contact_district.choices = districts
        emergency_contact_form.emergency_contact_province.choices = provinces
    else:
        flash(f'เกิดข้อผิดพลาด {emergency_contact_data}', category='danger')

    if talent_data:
        talent_form = TalentForm(formdata=request.form, obj=talent_data)
    else:
        flash(f'เกิดข้อผิดพลาด {talent_data}', category='danger')

    return render_template(
        'showThaiEmployee.html',
        image_form=image_form,
        general_form=general_form,
        register_address_form=register_address_form,
        actual_address_form=actual_address_form,
        father_form=father_form,
        mother_form=mother_form,
        clan_form=clan_form,
        family_form=family_form,
        health_data_form=health_data_form,
        emergency_contact_form=emergency_contact_form,
        talent_form=talent_form,
        tuple_form=tuple_form,

        getEducation=getEducation,
        getWorkHistory=getWorkHistory,

        employee_id=employee_id,
        general_data=general_data,
        ge_title=ge_title,
        em_nationality=em_nationality,
        em_ethnicity=em_ethnicity,
        em_religion=em_religion,

        register_address_data=register_address_data,
        re_subdistrict=re_subdistrict,
        re_district=re_district,
        re_province=re_province,

        actual_address_data=actual_address_data,
        ac_subdistrict=ac_subdistrict,
        ac_district=ac_district,
        ac_province=ac_province,

        clan_data=clan_data,
        father_data=father_data,
        fa_title=fa_title,
        mother_data=mother_data,
        mo_title=mo_title,

        family_data=family_data,
        fa_maritalStatus=fa_maritalStatus,
        sp_title=sp_title,

        health_data=health_data,
        b_group=b_group,

        emergency_contact_data=emergency_contact_data,
        em_title=em_title,
        em_subdistrict=em_subdistrict,
        em_district=em_district,
        em_province=em_province,

        education_data=education_data,
        education_level=education_level,
        education_level_code=education_level_code,
        education_level_name=education_level_name,

        work_history_data=work_history_data,
        talent_data=talent_data,
    )


@app.route('/foreigner', methods=['GET', 'POST'])
@login_required
def foreigner_page():
    return render_template('foreigner.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()

        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased{p_item_object.name} for {p_item_object.price}", category='success')
            else:
                flash(f"Unfortunately!, you don't have enough money to purchased{p_item_object.name}", category='danger')

        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    regis_form = RegisterForm()

    if regis_form.validate_on_submit():
        user_to_create = User(
            username=regis_form.username.data,
            email_address=regis_form.email_address.data,
            password=regis_form.password1.data,
            employee_id=regis_form.employee_id.data,
            user_lavel=regis_form.user_lavel.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('home_page'))

    if regis_form.errors != {}:
        for err_msg in regis_form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=regis_form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():

    login_form = LoginForm()

    if login_form.validate_on_submit():

        attempted_user = User.query.filter_by(username=login_form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=login_form.password.data):

            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')

            next = request.args.get('next')

            return redirect(next or url_for('home_page'))

        else:

            flash('Username and Password are not match!! Please try again', category='danger')

    return render_template('login.html', form=login_form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!!!", category='info')
    return redirect(url_for('home_page'))

