from flask import Flask, render_template, url_for, redirect, flash
from frontend import app, connection, db
from frontend.forms import RegistrationForm, LoginForm
from sqlalchemy.sql import text
from flask import request
from frontend.models import Admin
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    # connection.execute(text(
    #     r'insert into victim VALUES (2, "asd", "asd", 24, "male", 802374234, 3243511)'))
    result = connection.execute(text("SELECT * FROM victim"))
    print(result.mappings().all())
    return render_template('index.html')


@app.route('/view')
@login_required
def view():
    message = ""
    results = []
    if(category := request.values.get('search')):
        try:
            temp = connection.execute(text(f"SELECT * FROM {category}"))
            message = "Table values: "
            results.append(temp.mappings().all())
        except Exception:
            message = "Table does not exist!"
    else:
        for i in ['crime_register', 'victim']:
            temp = connection.execute(text(f"SELECT * FROM {i}"))
            results.append(temp.mappings().all())
            message = "Table values: "
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
        # print(user)
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