from flask import Flask, render_template, url_for, redirect, flash
from frontend import app, connection, db
from frontend.forms import CrimeForm, RegistrationForm, LoginForm
from sqlalchemy.sql import text
from flask import request
from frontend.models import Admin
from flask_login import login_user, current_user, logout_user, login_required
import re


@app.route('/')
def home():
    # connection.execute(text(
    #     r'insert into victim VALUES (2, "asd", "asd", 24, "male", 802374234, 3243511)'))
    # result = connection.execute(text("SELECT * FROM victim"))
    # print(result.mappings().all())
    return render_template('index.html')


@app.route('/view')
@login_required
def view():
    message = []
    results = []
    if(category := request.values.get('search')):
        try:
            temp = connection.execute(text(f"SELECT * FROM {category}")).mappings().all()
            message.append(f"{category} values: ")
            results.append({'values': temp, 'name': category})
        except Exception:
            message = f"Table {category} does not exist!"
    else:
        for i in ['officer_record', 'police_station', 'complainer', 'witness', 'accused', 'section', 'victim', 'crime_register', 'victim_fir', 'act_section', 'accused_fir', 'witness_fir']:
            temp = connection.execute(text(f"SELECT * FROM {i}")).mappings().all()
            results.append({'values': temp, 'name': i})
    return render_template('db.html', results=results, message=message)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        admin = Admin(username=form.username.data, password=form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        # connection.execute(text("INSERT INTO admin (username, password) VALUES (:username, :password)"),
        #                         {"username": form.username.data, "password": form.password.data})
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and form.password.data == admin.password:
            login_user(admin)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    form = CrimeForm()
    if request.method == "POST":
        values = request.form.to_dict()
        if form.validate_on_submit():
            connection.execute(text(
                f"insert into officer_record (name, address, age, gender, phone, email_id, qualification, aadhar) values (:o_name, :o_address, :o_age, :o_gender, :o_phone, :o_email_id, :o_qualification, :o_aadhar)"), values)
            officer_id = connection.execute(text(
                f"select * from officer_record where aadhar=:o_aadhar;"), values).mappings().all()[0]['officer_id']
            values['officer_id'] = officer_id

            if not connection.execute(text(f'select * from police_station where name=:ps_name'), values).mappings().all():
                connection.execute(text(
                    f"insert into police_station (name, address, phone, officer_id) values (:ps_name, :ps_address, :ps_phone, :officer_id)"), values)
            ps_id = connection.execute(text(
                f"select * from police_station where name=:ps_name;"), values).mappings().all()[0]['ps_id']
            values['ps_id'] = ps_id

            if not connection.execute(text(f'select * from complainer where aadhar=:c_aadhar'), values).mappings().all():
                connection.execute(text(
                    f"insert into complainer (name, address, age, gender, phone, aadhar) values (:c_name, :c_address, :c_age, :c_gender, :c_phone, :c_aadhar)"), values)
            complainer_id = connection.execute(text(
                f"select * from complainer where aadhar=:c_aadhar;"), values).mappings().all()[0]['complainer_id']
            values['complainer_id'] = complainer_id

            for i in values:
                if re.match(r"w_.*", i) or re.match(r"a_.*", i) or re.match(r"v_.*", i) or re.match(r"s_.*", i):
                    values[i] = [x.strip() for x in values[i].split(',')]

            values['witness_id'] = []
            for i in range(len(values['w_aadhar'])):
                if not values['w_aadhar']:
                    break
                if not connection.execute(text(f'select * from witness where aadhar=:w_aadhar'), {'w_aadhar': values['w_aadhar'][i]}).mappings().all():
                    connection.execute(text(f"insert into witness (name, address, age, gender, phone, aadhar) values (:w_name, :w_address, :w_age, :w_gender, :w_phone, :w_aadhar)"),
                                       {
                        'w_name': values['w_name'][i],
                        'w_address': values['w_address'][i],
                        'w_age': values['w_age'][i],
                        'w_aadhar': values['w_aadhar'][i],
                        'w_gender': values['w_gender'][i],
                        'w_phone': values['w_phone'][i]
                    })

                witness_id = connection.execute(text(f'select * from witness where aadhar=:w_aadhar'), {
                                                'w_aadhar': values['w_aadhar'][i]}).mappings().all()[0]['witness_id']
                values['witness_id'].append(witness_id)

            values['accused_id'] = []
            for i in range(len(values['a_aadhar'])):
                if not connection.execute(text(f'select * from accused where aadhar=:a_aadhar'), {'a_aadhar': values['a_aadhar'][i]}).mappings().all():
                    connection.execute(text(f"insert into accused (name, address, age, gender, phone, aadhar) values (:a_name, :a_address, :a_age, :a_gender, :a_phone, :a_aadhar)"),
                    {
                        'a_name': values['a_name'][i],
                        'a_address': values['a_address'][i],
                        'a_age': values['a_age'][i],
                        'a_aadhar': values['a_aadhar'][i],
                        'a_gender': values['a_gender'][i],
                        'a_phone': values['a_phone'][i]
                    })
                    print("check")

                accused_id = connection.execute(text(f'select * from accused where aadhar=:a_aadhar'), {
                                                'a_aadhar': values['a_aadhar'][i]}).mappings().all()[0]['accused_id']
                values['accused_id'].append(accused_id)
            

            values['victim_id'] = []
            for i in range(len(values['v_aadhar'])):
                if not connection.execute(text(f'select * from victim where aadhar=:v_aadhar'), {'v_aadhar': values['v_aadhar'][i]}).mappings().all():
                    connection.execute(text(f"insert into victim (name, address, age, gender, phone, aadhar) values (:v_name, :v_address, :v_age, :v_gender, :v_phone, :v_aadhar)"),
                    {
                        'v_name': values['v_name'][i],
                        'v_address': values['v_address'][i],
                        'v_age': values['v_age'][i],
                        'v_aadhar': values['v_aadhar'][i],
                        'v_gender': values['v_gender'][i],
                        'v_phone': values['v_phone'][i]
                    })
                    print("check")

                victim_id = connection.execute(text(f'select * from victim where aadhar=:v_aadhar'), {
                                                'v_aadhar': values['v_aadhar'][i]}).mappings().all()[0]['victim_id']
                values['victim_id'].append(victim_id)

            for i in range(len(values['s_id'])):
                if not connection.execute(text(f'select * from section where section_id=:s_id'), {"s_id" : values['s_id'][i]}).mappings().all():
                    connection.execute(text(
                        f"insert into section values (:s_id, :s_desc)"), {"s_id" : values['s_id'][i], "s_desc" : values['s_desc'][i]})
            

            connection.execute(text(f'insert into crime_register (date_of_offence, fir_no, ps_id, date_of_report, case_status, arrested, challan_id, officer_id, case_description, complainer_id)' +
                             ' values (:date_of_offence, :fir_no, :ps_id, :date_of_report, :case_status, :arrested, :challan_id, :officer_id, :case_description, :complainer_id)'),
                             values)
            crime_id = connection.execute(text(f'select * from crime_register where fir_no=:fir_no'), values).mappings().all()[0]['crime_id']

            for i in values['witness_id']:
                connection.execute(text(f'insert into witness_fir values (:witness_id, :crime_id)'),
                                   {'witness_id': i, 'crime_id': crime_id})

            for i in values['victim_id']:
                connection.execute(text(f'insert into victim_fir values (:victim_id, :crime_id)'), {'victim_id': i, 'crime_id': crime_id})

            for i in values['accused_id']:
                connection.execute(text(f'insert into accused_fir values (:accused_id, :crime_id)'), {'accused_id': i, 'crime_id': crime_id})

            for i in values['s_id']:
                connection.execute(text(f'insert into act_section values (:s_id, :crime_id)'), {'crime_id': crime_id, 's_id': i})
            return redirect(url_for('add'))
        print(form.errors.items())
    return render_template('add.html', title='Add', form=form)
