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
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import folium
from geopy.geocoders import Nominatim

# Module to display the jobs to the candidate

# Global variable definitions
candidate = Blueprint('candidate', __name__) # create a Blueprint object that we name 'candidate'
model = pickle.load(open('final_model.pkl', 'rb'))
df = pd.read_csv("linkedin-jobs.csv")
map = folium.Map(location=[43.6532, -79.3832],  zoom_start=8)
geolocator = Nominatim(user_agent='''Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) 
                        AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 
                        Mobile/9B179 Safari/7534.48.3")''')
recentsearches = []

# Preliminary data pre-processing
categorical_cols = ['Company', 'Location']
df[categorical_cols] = df[categorical_cols].astype('category')
df[categorical_cols] = df[categorical_cols].apply(lambda x: x.cat.codes)
df = df.drop(['index', 'Apply'], axis=1)
scaler = StandardScaler()

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

@candidate.route('/recommend-jobs', methods=['POST'])
def model_predict():
  data = request.get_json(force="TRUE") # Return set of arguments pulled from a JSON
  # Preprocess the input data
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
  return render_template("result.html", recommended_jobs=recommended_jobs)

@candidate.route('/jobmap', methods=["POST"])
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
  
@candidate.route('/jobloc', methods=["POST"])
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
  
# @candidate.route('/result', methods=['POST'])
# def results():
#   if request.method == 'POST':
#     to_predict = request.form.to_dict() #Returns a dictionary from the request form (.csv file)
#     to_predict_list = list(to_predict.values()) # List all values found in the dictionary for the predicted feature
#     to_predict_list = list(map(int, to_predict_list)) # Get user input from the prediction list, and perform label encoding using map
#     res = model_predict(to_predict_list) # Call function to generate results
#     if int(res) == 1: # If predictions are valid...
#       prediction = res
#     else:
#       prediction = 'The entered job title did not produce accurate enough results to be displayed'
#     return render_template('result.html', prediction = prediction)