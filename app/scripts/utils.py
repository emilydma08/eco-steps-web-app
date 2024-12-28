# utils.py

# Define the logic for each target variable
def sustainability_engagement(row):
    if row['lifestyle-rating'] >= 4:
        return 'High'
    elif row['lifestyle-rating'] == 3:
        return 'Medium'
    else:
        return 'Low'

def plastics_reduction_readiness(row):
    if row['avoid-plastics'] in ['Often', 'Daily']:
        return 'Ready'
    else:
        return 'Not Ready'

def plant_based_diet_readiness(row):
    if row['plant-meals'] in ['Often', 'Daily']:
        return 'Ready'
    else:
        return 'Not Ready'

def waste_sorting_readiness(row):
    if row['waste-sorting'] in ['Often', 'Daily']:
        return 'Ready'
    else:
        return 'Not Ready'

def time_commitment_readiness(row):
    if row['time-commitment'] in ['20-30 minutes', '30-45 minutes', '45+ minutes']:
        return 'Ready'
    else:
        return 'Not Ready'

def second_hand_buying_readiness(row):
    if row['buy-secondhand'] in ['Often', 'Daily']:
        return 'Ready'
    else:
        return 'Not Ready'

def resource_conservation_readiness(row):
    if row['reduce-resources'] in ['Often', 'Daily']:
        return 'Ready'
    else:
        return 'Not Ready'

def commute_sustainability_readiness(row):
    if row['commute-choice'] in ['Bike', 'Public Transport', 'Walk']:
        return 'Ready'
    else:
        return 'Not Ready'

def sustainability_knowledge(row):
    # Here you can define a basic logic, for now, I’ll return a dummy value
    return 'Basic' if row['lifestyle-rating'] >= 3 else 'Low'

def personalized_challenge_suggestion(row):
    # Suggest campaigns based on the readiness for sustainability actions
    if row['plastics-reduction-readiness'] == 'Ready' and row['plant-based-diet-readiness'] == 'Ready':
        return 'Plastic Reduction & Diet Challenge'
    elif row['waste-sorting-readiness'] == 'Ready':
        return 'Waste Sorting Challenge'
    else:
        return 'General Sustainability Challenge'
