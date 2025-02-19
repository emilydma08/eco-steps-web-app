from app import app
from flask import session, render_template, request, jsonify, redirect, url_for
import joblib
import pandas as pd
import numpy as np
from app.preprocessing import preprocess_data
from app.campaigns import campaigns
import random

app.secret_key='secretkey'

model = joblib.load('app/ml_model/recommendation_model.pkl')

# Home route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'GET':
        session.clear()
        return render_template('survey.html')
    
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
            session['survey_completed'] = True
            print(predicted_campaign_value)

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
    recommended_campaign = int(session.get('recommended_campaign', None))
    print(recommended_campaign)
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
    if 'survey_completed' not in session or not session['survey_completed']:
        # Render the dashboard page with a popup
        return render_template('dashboard.html', 
                               popup_message="You need to complete the initial survey before accessing your dashboard.",
                               redirect_url=url_for('survey'))
    if 'completed_campaigns' not in session:
        session['completed_campaigns'] = []

    # Ensure completed_campaigns is a list of integers
    session['completed_campaigns'] = list(map(int, session['completed_campaigns']))
    session.modified = True

    total_campaigns_completed = len(session['completed_campaigns'])

    total_challenges_completed = sum(
        len(campaigns[i]['challenges']) for i in session['completed_campaigns']
    )

    # Get the current recommended campaign
    recommended_campaign = session.get('recommended_campaign', None)

    if recommended_campaign is None:
        remaining_campaigns = [i for i in range(len(campaigns)) if i not in session['completed_campaigns']]
        if not remaining_campaigns:
            return render_template(
                'dashboard.html', 
                error_message="Congratulations! You’ve completed all available campaigns!",
                campaign_challenges=[],
                campaign_name="All Campaigns Completed",
                campaign_description="Enjoy some time off or explore the completed challenges section!",
                campaign_length=0,
                total_campaigns_completed=total_campaigns_completed,
                total_challenges_completed=total_challenges_completed,
            )
        else:
            print("Redirecting to survey due to no recommended campaign.")
            return redirect(url_for('survey'))

    try:
        recommended_campaign = int(recommended_campaign)
    except ValueError:
        print("Invalid recommended campaign, redirecting to survey.")
        return redirect(url_for('survey'))

    # Debugging output
    print("Recommended campaign:", recommended_campaign)
    print("Completed campaigns:", session['completed_campaigns'])

    # Check if the recommended campaign is already completed
    if recommended_campaign in session['completed_campaigns']:
        print("Current campaign found to be completed.")
        remaining_campaigns = [i for i in range(len(campaigns)) if i not in session['completed_campaigns']]

        if remaining_campaigns:
            recommended_campaign = random.choice(remaining_campaigns)
            session['recommended_campaign'] = recommended_campaign
            session.modified = True
            print(f"New campaign being chosen: {recommended_campaign}")
        else:
            return render_template(
                'dashboard.html', 
                error_message="Congratulations! You’ve completed all available campaigns!",
                campaign_challenges=[],
                campaign_name="All Campaigns Completed",
                campaign_description="Enjoy some time off or explore the completed challenges section!",
                campaign_length=0,
                total_campaigns_completed=total_campaigns_completed,
                total_challenges_completed=total_challenges_completed,
            )

    campaign_name = campaigns[recommended_campaign]['name']
    campaign_icon = campaigns[recommended_campaign]['icon']
    campaign_description = campaigns[recommended_campaign]['description']
    campaign_length = campaigns[recommended_campaign]['length']
    campaign_challenges = campaigns[recommended_campaign]['challenges']

    return render_template(
        'dashboard.html',
        recommended_campaign=campaign_name, 
        campaign_icon=campaign_icon,
        campaign_description=campaign_description,
        campaign_length=campaign_length,
        campaign_challenges=campaign_challenges,
        total_campaigns_completed=total_campaigns_completed,
        total_challenges_completed=total_challenges_completed,
    )



@app.route('/complete_campaign', methods=['POST'])
def complete_campaign():
    # Get the current campaign
    current_campaign = session.get('recommended_campaign', None)

    if current_campaign is not None:
        # Debugging output
        print(f"Completing campaign: {current_campaign}")
        print(f"Before completion, completed campaigns: {session.get('completed_campaigns', [])}")

        # Initialize completed campaigns if not present
        if 'completed_campaigns' not in session:
            session['completed_campaigns'] = []

        # Add the current campaign to the completed list
        session['completed_campaigns'].append(int(current_campaign))
        session.modified = True

        # Debugging output after update
        print(f"After completion, completed campaigns: {session['completed_campaigns']}")

        remaining_campaigns = [i for i in range(len(campaigns)) if i not in session['completed_campaigns']]
        if remaining_campaigns:
            new_campaign = random.choice(remaining_campaigns)
            session['recommended_campaign'] = new_campaign
            print(f"New campaign chosen: {new_campaign}")
        else:
            # If no campaigns remain, set recommended_campaign to None
            session['recommended_campaign'] = None
            print("All campaigns completed!")

    return jsonify({'message': 'Campaign completed'}), 200


# About route
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reset_session')
def reset_session():
    session.clear()
    return "Session reset. All session data cleared."
