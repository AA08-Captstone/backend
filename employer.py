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


employer = Blueprint('employer', __name__)

@employer.route('/employerprofile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('employerProfile.html', name=current_user.name)