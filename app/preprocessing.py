import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Define the categories just like in the synthetic data generation
lifestyle_rating = [1, 2, 3, 4, 5]
waste_sorting = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
avoid_plastics = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
plant_meals = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
time_commitment = ['1-10', '10-20', '20-30', '30-45', '45+']
secondhand_buying = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
resource_conservation = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
commute_choice = ['Car', 'Bike', 'Public Transport', 'Walk', 'Other', 'None']


# Preprocess the categorical data using one-hot encoding
def preprocess_data(user_data):
    # Initialize a OneHotEncoder for the features
    encoder = OneHotEncoder(categories=[
            waste_sorting,
            avoid_plastics,
            plant_meals,
            time_commitment,
            secondhand_buying,
            resource_conservation,
            commute_choice
        ], sparse_output=False)
    
    # Create a DataFrame with categorical data only (the ones needing one-hot encoding)
    categorical_data = pd.DataFrame([[
        user_data['waste-sorting'],
        user_data['avoid-plastics'],
        user_data['plant-meals'],
        user_data['time-commitment'],
        user_data['buy-secondhand'],
        user_data['reduce-resources'],
        user_data['commute-choice']
    ]], columns=['waste-sorting', 'avoid-plastics', 'plant-meals', 'time-commitment', 'buy-secondhand', 'reduce-resources', 'commute-choice'])

    # Apply one-hot encoding
    encoded_features = encoder.fit_transform(categorical_data)
    
    # Get numerical features (like lifestyle-rating)
    numeric_features = np.array([user_data['lifestyle-rating']]).reshape(1, -1)
    
    # Combine categorical and numeric features into a single feature vector
    feature_vector = np.concatenate([encoded_features, numeric_features], axis=1)
    
    return feature_vector

