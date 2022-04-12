from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/project'
db = SQLAlchemy(app)
connection = db.engine.connect()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
from frontend import routes
