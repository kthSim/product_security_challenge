from project import app
from flask import render_template


@app.route("/")
def index():
    return "Hello World! Zendesk :D"


@app.route("/login")
def login():
    return render_template("index.html")