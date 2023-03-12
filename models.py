from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Employer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Job(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    company = db.Column(db.String(100), unique=True)
    location = db.Column(db.String(100))
    title = db.Column(db.String(1000))
    link = db.Column(db.nvarchar(max), unique=True)
    # desc = db.Column(db.nvarchar(max), unique=True)

# class resumeInfo():
    #https://pypi.org/project/resume-parser/
# class profile():
