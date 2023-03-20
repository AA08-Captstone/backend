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
    return render_template('index.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    app.run(debug=True) # run the flask app on debug mode
    