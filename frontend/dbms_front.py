from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import pymysql

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/project'
db = SQLAlchemy(app)

connection = db.engine.connect()


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}', '{self.image_file}')"


@app.route('/')
def home():
    # connection.execute(text(
    #     r'insert into victim VALUES (2, "asd", "asd", 24, "male", 802374234, 3243511)'))
    result = connection.execute(text("SELECT * FROM victim"))
    print(result.mappings().all())
    return render_template('index.html')


@app.route('/db')
def db():
    result = connection.execute(text("SELECT * FROM victim"))
    result = result.mappings().all()
    return render_template('db.html', result=result)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
