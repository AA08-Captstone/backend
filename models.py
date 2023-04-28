from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = False) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    profile_setup = db.Column(db.Boolean, default=False, nullable=False)
    current_resume = db.Column(db.String(1000))
    profile_pic = db.Column(db.String(1000))
    resume_parsed = db.Column(db.Boolean, default=False, nullable=False)
    #edu
    #exp
    #skills
    location = db.Column(db.String(1000))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    bio = db.Column(db.String(10000))

class Employer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = False) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    profile_setup = db.Column(db.Boolean, default=False, nullable=False)

class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = False) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Job(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    title = db.Column(db.String(1000))
    #skill
    link = db.Column(db.String(5000), unique=False)


