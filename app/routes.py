from app import app
from flask import render_template

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Survey route
@app.route('/survey')
def survey():
    return render_template('survey.html')

# Campaigns route
@app.route('/campaigns')
def select_campaign():
    return render_template('campaigns.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Progress route
@app.route('/progress')
def progress():
    return render_template('progress.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')
