from dotenv import load_dotenv
import os 
from models import adminUser
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db

def create_super_admin():
    # creating super admin
    username = os.getenv("ADMIN_USERNAME")
    admin_check = adminUser.query.filter_by(username=username).first() 
    if not admin_check:
        password = os.getenv("ADMIN_PASSWORD")
        super_admin = adminUser(username=username, name="Super Admin", password=generate_password_hash(password, method='sha256'))
        db.session(super_admin)
        db.session.commit()