from flask import Flask,request, redirect, jsonify, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/Blog")
def Blog():
    return render_template("blog.html")