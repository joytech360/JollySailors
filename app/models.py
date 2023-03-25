import jwt
import sys
from flask import redirect, url_for, flash
from time import time as ttime

from datetime import datetime, timedelta, time

from app import app, db, login
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(id)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    phone_no = db.Column(db.String(64))
    join_date = db.Column(db.Date)
    password_hash = db.Column(db.String(128))
    street = db.Column(db.String(64))
    city = db.Column(db.String(32))
    province = db.Column(db.String(8))
    postal_code = db.Column(db.String(16))
    country = db.Column(db.String(32))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': ttime() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')#.decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_id_token(self, expires_in=1800):
        return jwt.encode(
            {'user_id': self.id, 'exp': ttime() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_id_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['user_id']
        except:
            return
        return User.query.get(id)

    def full_address(self):
        return f"{self.street}, {self.city} {self.province} {self.postal_code} {self.country}"

    def is_daycare_admin(self):
        is_daycare_admin = self.daycare_staff.filter(daycare_staff.c.user_id == self.id).count() > 0
        return is_daycare_admin

    def my_daycare(self):
        daycare = self.daycare_staff.first()
        return daycare


class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    birth_date = db.Column(db.Date)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    parent = db.relationship('User', backref=db.backref('children', lazy='dynamic'))

    def current_daycare(self):
        daycare = DaycareStudent.query.filter_by(child_id=self.id, date_left=None).first()
        if daycare:
            return daycare.daycare
        return 'No Daycare Linked'


daycare_staff = db.Table('daycare_staff',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('daycare_id', db.Integer, db.ForeignKey('daycare.id')),
)


class Daycare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    phone_no = db.Column(db.String(64))
    date_joined = db.Column(db.Date)
    street = db.Column(db.String(64))
    city = db.Column(db.String(32))
    province = db.Column(db.String(8))
    postal_code = db.Column(db.String(16))
    country = db.Column(db.String(32))
    lat = db.Column(db.Numeric(10, 6))
    lng = db.Column(db.Numeric(10, 6))
    capacity = db.Column(db.Integer)
    opening_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)
    about = db.Column(db.String(1028))
    profile_pic = db.Column(db.String(128))

    staffs = db.relationship(
        'User', secondary='daycare_staff',
        backref=db.backref('daycare_staff', lazy='dynamic'), lazy='dynamic'
    )

    def full_address(self):
        return f"{self.street}, {self.city} {self.province} {self.postal_code}"

    def student_count(self):
        student_count = DaycareStudent.query.filter_by(daycare_id=self.id, date_left=None).count()
        return student_count


class DaycareStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    daycare_id = db.Column(db.Integer, db.ForeignKey('daycare.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    date_joined = db.Column(db.Date)
    date_left = db.Column(db.Date)

    daycare = db.relationship('Daycare', backref=db.backref('children', lazy='dynamic'))
    child = db.relationship('Child', backref=db.backref('daycare', lazy='dynamic'))


class ChildRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    daycare_id = db.Column(db.Integer, db.ForeignKey('daycare.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    date_requested = db.Column(db.Date)
    message = db.Column(db.String(512))

    daycare = db.relationship('Daycare', backref=db.backref('children_requests', lazy='dynamic'))
    child = db.relationship('Child', backref=db.backref('daycare_requests', lazy='dynamic'))

