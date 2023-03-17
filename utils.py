from flask import (
Flask,
request, 
redirect,
jsonify,
url_for,
Blueprint,
render_template, 
flash,
)

from dotenv import load_dotenv
import os 
from models import AdminUser, Job
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
import pandas as pd
import pickle 
import json

model = pickle.load(open('final_model.pkl', 'rb'))

def create_super_admin():
    # creating super admin
    username = os.getenv("ADMIN_USERNAME")
    admin_check = AdminUser.query.filter_by(username=username).first() 
    if admin_check == None:
        password = os.getenv("ADMIN_PASSWORD")
        super_admin = AdminUser(username=username, name="Super Admin", password=generate_password_hash(password, method='sha256'))
        db.session.add(super_admin)
        db.session.commit()

def new_job_card(jobtitle):
    jobtitle = Job.query.filter_by(title = jobtitle).first()
    if jobtitle == None:
        link = Job.query.filter_by(link=link).first()
        company = Job.query.filter_by(company = company).first()
        location = Job.query.filter_by(location = location).first()
        job = Job(title=jobtitle, company=company, location=location, link=link)
        db.session.add(job)
        db.session.commit()

def get_job_cards(title):
    df = pd.read_csv("linkedin-jobs.csv")
    df.loc[df['Title'].isnull(), 'Title'] = df['Title'].value_counts().index[0] # Preprocessing to remove null data
    title_list = df.loc[df['Title'] == title]
    cards = new_job_card(title_list)
    return cards
