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
import folium
from geopy.geocoders import Nominatim

# Module to display the jobs/candidates to the employer
employer = Blueprint('employer', __name__) # create a Blueprint object that we name 'employer'
model = pickle.load(open('final_model.pkl', 'rb'))
df = pd.read_csv("linkedin-jobs.csv")
recentsearches = []
map = folium.Map(location=[43.6532, -79.3832],  zoom_start=8)
geolocator = Nominatim(user_agent='''Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) 
                        AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 
                        Mobile/9B179 Safari/7534.48.3")''')

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
  
@employer.route('/jobmap', methods=["POST"])
def show_jobmap():
  data = request.get_json(force="TRUE")
  grouped_data = data.groupby('city')
  for i in range(0,len(data)):
   html = f"""
        <h1>{data.iloc[i]['city']}</h1>
        <p>Available Jobs:</p>
        <ul>
    """

   grouped_data = data.groupby('city')
   for city, group in grouped_data:
        if city == data.iloc[i]['city']:
            unique_jobs = group['Title'].unique()
            job_count = len(unique_jobs) # count the number of unique jobs
            html += f"<h2>{job_count} Jobs</h2>" # add job count as header to HTML
            for job in unique_jobs:
                html += f"<li>{job}</li>"
   html += """
        </ul>
        <p><a href="https://www.python-graph-gallery.com">More Info</a></p>
    """
   iframe = folium.IFrame(html=html, width=200, height=200)
   popup = folium.Popup(iframe, max_width=2650)
   location = geolocator.geocode(data.iloc[i]['city'])
   lat, lon = location.latitude, location.longitude

   folium.Marker(location=[lat, lon],popup=popup,).add_to(map)

  # Display the map
  return render_template("result.html", map=map)
  
@employer.route('/jobloc', methods=["POST"])
def get_location(cit):
  location = geolocator.geocode(cit)
  if location is not None:
    return location
  
  df["loc"] = df["city"].apply(get_location)
  df = df.dropna(subset=['loc'])
  grouped_data = df.groupby('city')
  
  for city, group in grouped_data:
      print("Jobs in " + city + ":")
      unique_jobs = group['Title'].unique()
      for job in unique_jobs:
          print("- " + job)
      
      print("")