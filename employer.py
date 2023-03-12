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
from utils import new_job_card, get_job_cards

# Displaying the jobs to the employer
# Blueprints are app states (employer state)
employer = Blueprint('employer', __name__) # create a Blueprint object that we name 'employer'
model = pickle.load(open('final_model.pkl', 'rb'))
@employer.route('/jobcard', methods=['GET', 'POST'])
def job_disp(): # Define job display function
    if request.method == 'GET':
      return render_template('employerhome.html')
    else:
       title = request.form.get('title')
       job = Job.query.filter_by(title=title).first()
      #  Check if the job exists
       if not job:
        flash("This job does not exist in the database")
       return redirect(url_for('main.empdash'))

@employer.route('/carddisp', methods=['GET', 'POST'])
def card_display():
  # Use the loaded pickle model to get the top predicted class, 
  # then display the job to the usertop_predicted = model_predict(model)
  top_predicted = model_predict(model)
  job_cards = get_job_cards(top_predicted)
  return render_template('employerhome.html', job_cards = job_cards[:5])

@employer.route('/jobsearch', methods=['GET', 'POST'])
def job_search():
  if request.method == 'GET':
    return render_template('candidatesearch.html')
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
    return redirect(url_for('main.empdatapage'))

@employer.route('/prediction')
def model_predict(to_predict_list):
  to_predict = np.array(to_predict_list).reshape(1, 12)
  res = model.predict(to_predict)
  return res[0]

@employer.route('/result', methods=['POST'])
def results():
  if request.method == 'POST':
    to_predict_list = request.form.to_dict()
    to_predict_list = list(to_predict_list.values())
    to_predict_list = list(map(int, to_predict_list))
    res = model_predict(to_predict_list)
    if int(res) == 1:
      prediction = res
    else:
      prediction = 'The entered job title did not produce accurate enough results to be displayed'
    return render_template('employresult.html', prediction = prediction)