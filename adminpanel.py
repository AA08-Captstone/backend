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
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db
from utils import create_super_admin


adminpanel = Blueprint('adminpanel', __name__)

@adminpanel.route('/admin')
@login_required
def admin():
    create_super_admin()
    return render_template('admin.html', name=current_user.name)

