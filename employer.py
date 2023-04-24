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
from flask_login import login_required, current_user
from models import Employer
from __init__ import db

employer = Blueprint('employer', __name__)

@employer.route('/employerprofile') # profile page that return 'profile'
@login_required
def employer_profile():
    emp = Employer.query.filter_by(email=current_user.email).first() # if this returns a user, then the email already exists in database
    if not emp.profile_setup:
        return redirect(url_for('employer.employer_profile_setup'))
    else:
        return render_template('employerProfile.html', name=current_user.name)


@employer.route('/employerprofilesetup', methods=['POST','GET']) # profile page that return 'profile'
@login_required
def employer_profile_setup():
    if request.method=='POST':
        user = Employer.query.filter_by(email=current_user.email).first()
        user.first_name = request.form.get('first_name')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.location = "Canada"
        user.bio = request.form.get('bio')
        user.profile_setup = True
        db.session.commit()
        return redirect(url_for('employer.profile'))
    if request.method=='GET':
        return render_template('employerSetup.html', name=current_user.name)
    
@employer.route('/employerHome') # profile page that return 'profile'
@login_required
def employer_homepage():
    return render_template("")