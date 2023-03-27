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
import pandas as pd
import pickle
from utils import new_job_card, get_job_cards
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Module to display the jobs/candidates to the employer
employer = Blueprint('employer', __name__) # create a Blueprint object that we name 'employer'
model = pickle.load(open('final_model.pkl', 'rb'))
df = pd.read_csv("linkedin-jobs.csv")
recentsearches = []

# Preliminary data pre-processing
categorical_cols = ['Company', 'Location']
df[categorical_cols] = df[categorical_cols].astype('category')
df[categorical_cols] = df[categorical_cols].apply(lambda x: x.cat.codes)
df = df.drop(['index', 'Apply'], axis=1)
scaler = StandardScaler()
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
  
@employer.route('/search', methods=['POST'])
def search():
    search_query = request.json['query']
    # Add the search query to the recent searches list
    recent_searches.insert(0, search_query)
    # Only keep the 10 most recent searches
    recent_searches = recent_searches[:5]
    # Return the search results
    return f'Search results for "{search_query}"'

# Define a route to get the most recent searches
@employer.route('/recent-searches')
def recent_searches():
    return jsonify(recent_searches)
@employer.route('/prediction')
def model_predict():
    data = request.get_json(force="TRUE") # Return set of arguments pulled from a JSON
    features = [np.array(data['Title'])] # Feature extraction
    prediction = model.predict(features) # Call the pickle model to make a prediction based on the job title given
    return str(prediction[:5])

@employer.route('/recommend-jobs', methods=['POST'])
def model_predict():
    data = request.get_json(force="TRUE") # Return set of arguments pulled from a JSON
    # Preprocess the input data
    title = request.form['Title']
    input_data = pd.DataFrame(data, index=[0])
    input_data[categorical_cols] = input_data[categorical_cols].astype('category')
    input_data[categorical_cols] = input_data[categorical_cols].apply(lambda x: x.cat.codes)
    input_data = input_data.drop(['index', 'Apply'], axis=1)
    
    # Scale the input data
    input_data = scaler.transform(input_data)
    
    # Use the trained model to make predictions on the preprocessed input data
    similarities = cosine_similarity(input_data, scaler.transform(df.drop('Title', axis=1)))
    top_similarities = np.argsort(similarities)[0][::-1][1:6]
    recommended_jobs = df.iloc[top_similarities]['Title'].tolist()
    
    # Return the predicted job titles to the user
    return render_template("empresult.html", title=title, recommended_jobs=recommended_jobs)