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

# Module to display the jobs to the candidate

# Global variable definitions
candidate = Blueprint('candidate', __name__) # create a Blueprint object that we name 'candidate'
model = pickle.load(open('final_model.pkl', 'rb'))
recentsearches = []

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
       return redirect(url_for('main.userdash'))

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
  
@candidate.route('/search', methods=['POST'])
def search():
    search_query = request.json['query']
    # Add the search query to the recent searches list
    recent_searches.insert(0, search_query)
    # Only keep the 5 most recent searches
    recent_searches = recent_searches[:5]
    # Return the search results
    return f'Search results for "{search_query}"'

# Define a route to get the most recent searches
@candidate.route('/recent-searches')
def recent_searches():
    return jsonify(recent_searches)

@candidate.route('/prediction')
def model_predict():
    data = request.get_json(force="TRUE") # Return set of arguments pulled from a JSON
    features = [np.array(data['Title'])] # Feature extraction
    prediction = model.predict(features) # Call the pickle model to make a prediction based on the job title given
    return str(prediction[:5])

@candidate.route('/result', methods=['POST'])
def results():
  if request.method == 'POST':
    to_predict = request.form.to_dict() #Returns a dictionary from the request form (.csv file)
    to_predict_list = list(to_predict.values()) # List all values found in the dictionary for the predicted feature
    to_predict_list = list(map(int, to_predict_list)) # Get user input from the prediction list, and perform label encoding using map
    res = model_predict(to_predict_list) # Call function to generate results
    if int(res) == 1: # If predictions are valid...
      prediction = res
    else:
      prediction = 'The entered job title did not produce accurate enough results to be displayed'
    return render_template('result.html', prediction = prediction)