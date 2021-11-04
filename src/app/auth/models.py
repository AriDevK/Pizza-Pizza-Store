from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    zip_code = db.Column(db.String(5), nullable=True)
    phone_number = db.Column(db.String(10), nullable=True)
    street = db.Column(db.String(80), nullable=True)
    house_number = db.Column(db.String(10), nullable=True)

    def __init__(self, name, email, password, created_at):
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at

    def __repr__(self):
        return f'<User {self.email}>'
