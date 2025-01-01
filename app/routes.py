from app import app
from flask import session, render_template, request, jsonify, redirect, url_for
import joblib
import pandas as pd
import numpy as np
from app.preprocessing import preprocess_data
from app.campaigns import campaigns

app.secret_key='secretkey'

model = joblib.load('app/ml_model/recommendation_model.pkl')

# Home route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        # Process the form data
        try:
            form_data = request.get_json()  # Get JSON payload from the client
            print(form_data)  # Debugging output

            # Default handling if 'waste-sorting' isn't in the form data
            if 'waste-sorting' not in form_data:
                form_data['waste-sorting'] = 'default_value'  # Set an appropriate default or handle as needed

            # Process the data (as per your existing logic)
            processed_data = preprocess_data(form_data)
            processed_data = np.array(processed_data, dtype=float)

            if np.any(np.isnan(processed_data)) or np.any(np.isinf(processed_data)):
                print("Data contains NaN or infinity values!")

            # Make predictions with the model
            predicted_campaign = model.predict(processed_data)
            predicted_campaign_value = int(predicted_campaign[0])


             # Store the predicted value in session
            session['recommended_campaign'] = predicted_campaign_value

            # Redirect to the /campaigns route
            return redirect(url_for('select_campaign'))
        
        except Exception as e:
            print(f"Error during prediction: {e}")
            return jsonify({'error': "Error predicting campaign"}), 500

    # If it's a GET request, just render the survey form
    return render_template('survey.html')

# Campaigns route
@app.route('/campaigns')
def select_campaign():
    recommended_campaign = int(session.get('recommended_campaign', None))+1
    campaign_name = campaigns[recommended_campaign]['name']
    campaign_icon = campaigns[recommended_campaign]['icon']
    campaign_description = campaigns[recommended_campaign]['description']
    campaign_length = campaigns[recommended_campaign]['length']
    return render_template(
        'campaigns.html', 
        recommended_campaign=campaign_name, 
        campaign_icon=campaign_icon,
        campaign_description=campaign_description,
        campaign_length=campaign_length)

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
