from . import db
from .auth.models import User
from datetime import datetime

class Menu(db.Model):

    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(64), nullable=False)


    def __repr__(self):
        return f'<User {self.name}>'


class Sell(db.Model):

    __tablename__ = 'sell'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sell_number = db.Column(db.String(64), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    final_price = db.Column(db.Float, nullable=False)


    def __init__(self, user_id, sell_number, final_price):
        self.user_id = user_id
        self.sell_number = sell_number
        self.final_price = final_price


    def __repr__(self):
        return f'<Sell {self.id}>'