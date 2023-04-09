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
from flask_login import login_required, current_user,logout_user
from __init__ import create_app, db
from utils import upload_jobs


main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def index():
    logout_user() 
    #upload_jobs()
    return render_template('landingPage.html')

@main.route('/features')
def features_page():
    return render_template("features.html")

@main.route('/faq') # profile page that return 'profile'
def faq_page():
    return render_template('faq.html')

@main.route('/contact') # profile page that return 'profile'
def contact_page():
    return render_template('contact.html')

@main.route('/about') # profile page that return 'profile'
def about_page():
    return render_template('about.html')

@main.route('/OurTeam') # profile page that return 'profile'
def our_team_page():
    return render_template('about.html')

@main.route('/portal/<string:method>',methods=['GET']) # profile page that return 'profile'
def login_portal(method):
    if method == "login":
        return render_template('loginPortal.html',links=["/candidateProfile","/employerprofile"],text=["Candidate","Employer"])
    elif method == "signup":
        return render_template('loginPortal.html',links=["/signup","/EmployerSignup"],text=["I'm looking for a Job","I'm an Employer"])

#Remove this??
@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html')

app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    app.run(debug=True) # run the flask app on debug mode
    