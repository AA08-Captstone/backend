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
from __init__ import db
from auth import logout_user
from utils import upload_jobs


adminpanel = Blueprint('adminpanel', __name__)

@adminpanel.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        if request.form.get('upload_jobs') == 'true':
            try:
                print("Running upload jobs")
                upload_jobs()
            except:
                flash("could not upload jobs")
    return render_template('admin.html', name=current_user.name)
