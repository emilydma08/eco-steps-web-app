# data_preprocessing.py
import pandas as pd
from utils import sustainability_engagement, plastics_reduction_readiness, plant_based_diet_readiness, \
    waste_sorting_readiness, time_commitment_readiness, second_hand_buying_readiness, resource_conservation_readiness, \
    commute_sustainability_readiness, sustainability_knowledge, personalized_challenge_suggestion

def preprocess_data():
    # Load the generated synthetic survey data
    data = pd.read_csv('../data/synthetic_survey_data.csv')
    
    # Apply functions to generate target variables
    data['sustainability-engagement'] = data.apply(sustainability_engagement, axis=1)
    data['plastics-reduction-readiness'] = data.apply(plastics_reduction_readiness, axis=1)
    data['plant-based-diet-readiness'] = data.apply(plant_based_diet_readiness, axis=1)
    data['waste-sorting-readiness'] = data.apply(waste_sorting_readiness, axis=1)
    data['time-commitment-readiness'] = data.apply(time_commitment_readiness, axis=1)
    data['second-hand-buying-readiness'] = data.apply(second_hand_buying_readiness, axis=1)
    data['resource-conservation-readiness'] = data.apply(resource_conservation_readiness, axis=1)
    data['commute-sustainability-readiness'] = data.apply(commute_sustainability_readiness, axis=1)
    data['sustainability-knowledge'] = data.apply(sustainability_knowledge, axis=1)
    data['personalized-challenge-type'] = data.apply(personalized_challenge_suggestion, axis=1)
    
    # Save the processed data
    data.to_csv('../data/processed_survey_data.csv', index=False)
    print("Processed data saved to 'processed_survey_data.csv'.")

if __name__ == "__main__":
    preprocess_data()
