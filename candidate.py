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

from models import User, Job
import numpy as np
import pickle

# Displaying the jobs to the candidate
# Blueprints are app states (Candidate state)
candidate = Blueprint('candidate', __name__) # create a Blueprint object that we name 'candidate'
model = pickle.load(open('final_model.pkl', 'rb'))
@candidate.route('/jobcard', methods=['GET', 'POST'])
def job_disp(): # Define job display function
    if request.method == 'GET':
      return render_template('candidatehome.html')
    else:
       title = request.form.get('title')
       job = Job.query.filter_by(title=title).first()
      #  Check if the job exists
       if not job:
        flash("This job does not exist in the database")
      # Do something here to display the job card
       return redirect(url_for('main.userhome'))

@candidate.route('/carddisp', methods=['GET', 'POST'])
def card_display():
  # Use the loaded pickle model to get the top predicted class, 
  # then display the job to the user
  return redirect(url_for('main.userhome'))

@candidate.route('/jobsearch', methods=['GET', 'POST'])
def job_search():
  if request.method == 'GET':
    return render_template('jobsearch.html')
  else:
    jobtitle = request.form.get("jobtitle")
    dateposted = request.form.get("dateposted")
    jobtype = request.form.get("jobtype")
    location = request.form.get("location")
    if not jobtitle:
      flash("Please enter a job title!")
      return redirect(url_for('candidate.job_search'))
    elif not dateposted:
      flash("Please enter the recency of job postings!")
    elif not jobtype:
      flash("Please enter the job type!")
    elif not location:
      flash("Please enter the relative location!")
    model_predict(jobtitle)
    return redirect(url_for('main.searchresults'))

@candidate.route('/prediction')
def model_predict(to_predict_list):
  to_predict = np.array(to_predict_list).reshape(1, 12)
  loaded_model = pickle.load(open(filename, 'rb'))
  res = loaded_model.predict(to_predict)
  return res[0]

@candidate.route('/result', methods=['POST'])
def results():
  if request.method == 'POST':
    to_predict_list = request.form.to_dict()
    to_predict_list = list(to.predict_list.values())
    to_predict_list = list(map(int, to_predict_list))
    res = model_predict(to_predict_list)
    if int(res) == 1:
      prediction = res
    else:
      prediction = 'The entered job title did not produce accurate enough results to be displayed'
    return render_template('result.html', prediction = prediction)