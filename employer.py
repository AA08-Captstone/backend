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