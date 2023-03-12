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
from __init__ import create_app, db

main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/userdash')
def userhome():
    return render_template('candidatehome.html')

@main.route('/jobsearchpage') # subpage that return 'jobsearch'
def jobsearch():
    return render_template('jobsearch.html')

@main.route('/userdatapage') # datapage that return 'result'
def searchresults():
    return render_template('result.html')

@main.route('/empdash')
def userhome():
    return render_template('employerhome.html')

@main.route('/empsearchpage') # subpage that return 'jobsearch'
def jobsearch():
    return render_template('candidatesearch.html')

@main.route('/empdatapage') # datapage that return 'result'
def searchresults():
    return render_template('employresult.html')

app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    app.run(debug=True) # run the flask app on debug mode
    