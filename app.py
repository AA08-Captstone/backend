from flask import Flask,request, redirect, jsonify, render_template, url_for
from flask_assets import Bundle, Environment
import os

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")
js = Bundle("src/*.js", output="dist/main.js") # new

assets.register("css", css)
assets.register("js", js) # new
css.build()
js.build() # new


@app.route("/",methods=['GET','POST'])
def index():
    if request.method == "POST":
        choice = request.form['file_selection']
        return render_template(choice)
    else:
        cwd = os.getcwd()
        files = os.listdir(f"{cwd}/templates/")
        return render_template('index.html',files=files)


@app.route("/Blog")
def Blog():
    return render_template("blog.html")
