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
    df = pd.read_csv("../output/linkedin-jobs.csv")

    for i in range(len(df)):
        title= i[0]
        company = i[1]
        location = i[2]
        link = i[3]
        new_job = Job(title=title, company=company, location=location, link=link)
        db.session.add(new_job)
        db.session.commit()
        
