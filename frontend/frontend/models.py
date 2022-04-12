from frontend import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


@login_manager.user_loader
def load_admin(id):
    return Admin.query.get(int(id))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin('{self.username}', '{self.image_file}')"
