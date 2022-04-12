from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/project'
db = SQLAlchemy(app)
connection = db.engine.connect()

from frontend import routes
