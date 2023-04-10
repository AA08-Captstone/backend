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
from models import User, Job

employer = Blueprint('employer', __name__)

@employer.route('/employerprofile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('employerProfile.html', name=current_user.name)

@employer.route('/employer-setup', methods=['GET', 'POST']) # Route to employer setup page
@login_required
def employer_setup():
    if request.method == 'POST':
        # Get form data
        company_name = request.form['company_name']
        industry = request.form['industry']
        location = request.form['location']
        # Save form data to database or perform other actions here
        return redirect(url_for('employer-setup'))
    return render_template('employersetup.html')

@employer.route('/employer-setup')
def success():
    flash('Employer setup was successful!')
    return render_template('employersetup.html')

@employer.route('/candidateSearch') # candidate search page
@login_required
def candidate_search();
    user_list = User.query.all()
    return render_template('candidateSearch.html', name = current_user.name, userss = user_list)

# create a function to route to employer setup
# if profile is not set up go to employersetup.html, if profile is set up go to employerprofile.html