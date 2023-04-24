from dotenv import load_dotenv
import os 
from models import AdminUser,Job
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
import pandas as pd


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def create_super_admin():
    # creating super admin
    username = os.getenv("ADMIN_USERNAME")
    admin_check = AdminUser.query.filter_by(username=username).first() 
    if admin_check == None:
        password = os.getenv("ADMIN_PASSWORD")
        super_admin = AdminUser(username=username,
                    name="Super Admin", 
                    password=generate_password_hash(password, method='sha256'))
        db.session.add(super_admin)
        db.session.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_jobs():
    print("Reading file")
    df = pd.read_csv("../output/linkedin-jobs.csv")
    print("file read")
    for i in range(len(df)):
        print("getting info")
        title= df["Title"][i]
        company = df["Company"][i]
        location = df["Location"][i]
        link = df["Apply"][i]
        print("here")
        new_job = Job(title=title, company=company, location=location, link=link)
        print("here")
        db.session.add(new_job)
        print("here?")
        db.session.commit()
        print("commited")
        
