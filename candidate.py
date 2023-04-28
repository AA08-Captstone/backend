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
from models import User,Job
from __init__ import db, UPLOAD_FOLDER, PROFILEPIC_FOLDER
from werkzeug.utils import secure_filename
from utils import allowed_file , parse_resume
import os


candidate = Blueprint('candidate', __name__)

@candidate.route('/candidateProfile') # profile page that return 'profile'
@login_required
def profile():
    user = User.query.filter_by(email=current_user.email).first() # if this returns a user, then the email already exists in database
    if not user.profile_setup:
        return redirect(url_for('candidate.profile_setup'))
    else:
        resume_content = ""
        try:
            resume_content = parse_resume(f"{UPLOAD_FOLDER}/{user.current_resume}")
        except:
            print("Resume not parsed")
        return render_template('profile.html', name=current_user.name, resume_content=resume_content)


@candidate.route('/profile_setup', methods=['POST','GET']) # profile page that return 'profile'
@login_required
def profile_setup():
    if request.method=='POST':
        user = User.query.filter_by(email=current_user.email).first()
        user.first_name = request.form.get('first_name')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.location = "Canada"
        user.bio = request.form.get('bio')
        user.profile_setup = True
        try:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            user.current_resume = filename
        except Exception:
            print("")
        try:
            file = request.files['pfp']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(PROFILEPIC_FOLDER, filename))
            user.profile_pic = filename
        except Exception:
            print("")
        db.session.commit()
        return redirect(url_for('candidate.profile'))
    if request.method=='GET':
        return render_template('profileSetup.html', name=current_user.name)

@candidate.route('/candidateHome') # profile page that return 'profile'
@login_required
def candidate_home():
    return render_template('candidateHome.html', name=current_user.name)

@candidate.route('/jobsearch') # profile page that return 'profile'
@login_required
def candidate_job_search():
    job_list = Job.query.all()
    return render_template('jobSearchTable.html', name=current_user.name,job_list=job_list)

@candidate.route('/mapview') # profile page that return 'profile'
@login_required
def candidate_map():
    return render_template('map.html')

@candidate.route('/recommendation') # profile page that return 'profile'
@login_required
def candidate_recommendation():
    return render_template('recommendation.html')

@candidate.route('/community') # profile page that return 'profile'
@login_required
def candidate_community():
    return render_template('community.html')