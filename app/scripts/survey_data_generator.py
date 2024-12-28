# survey_data_generator.py
import random
import pandas as pd
import os

# Define possible choices for each question
lifestyle_rating = [1, 2, 3, 4, 5]
waste_sorting = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
avoid_plastics = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
plant_meals = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
time_commitment = ['1-10', '10-20', '20-30', '30-45', '45+']
secondhand_buying = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
resource_conservation = ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily']
commute_choice = ['Car', 'Bike', 'Public Transport', 'Walk', 'Other', 'None']

campaigns = {
    'Waste-Free Week': ['Avoid disposable packaging', 'Compost all food scraps', 'Cook meals with zero food waste', 'Repair or repurpose an item instead of discarding it', 'Only use reusable bags and containers', 'Avoid single-use coffee cups and utensils', 'Donate unwanted items instead of discarding them', 'Conduct a waste audit in your home'],
    'Energy-Saver': ['Turn off all lights and electronics when not in use', 'Unplug devices when fully charged', 'Use natural light during the day', 'Reduce thermostat usage by 2 degrees', 'Wash clothes in cold water', 'Limit screen time to conserve device energy', 'Use a fan instead of air conditioning', 'Set your computer to power-saving mode'],
    'Plastic Free': ['Use a refillable water bottle exclusively', 'Replace pastic wrap with beeswax wraps', 'Avoid plastic straws', 'Choose bar soup and shampoo bars over bottled products', 'Avoid plastic bags when shopping', 'Find alternatives to plastic packaging when online shopping'],
    'Fast Fashion Detox': ['Organize a clothing swap with friends', 'Mend or alter existing clothing instead of discarding it', 'Shop secondhand for any clothing needs', 'Research the environmental impact of fast fashion', 'Build a capsule wardrobe with versatile pieces', 'Donate unused clothes to charities', 'Learn how to sew a simple garment', 'Choose natural fabrics over synthetic ones'],
    'Litter Cleanup Challenge': ['Pick up litter in your neighborhood for 20 minutes', 'Host a local cleanup event with friends', 'Remove iltter from a local park or beach', 'Collect litter during a walk or run', 'Share before and after photos of cleaned areas'],
    'Plant-Based Eating': ['Prepare one fully plant-based meal per day', 'Reduce dairy milk with plant-based alternatives', 'Try cooking with a plant-based protein', 'Swap a meat dish for a veggie alternative', 'Eat only plant-based foods today', 'Research the environmental benefits of plant-based eating', 'Buy ingredients from a local farmers\' market', 'Challenge a friend to a plant-based meal cook-off'],
    'Water-Saver': ['Limit your shower to 2 minutes', 'Turn off the tap while brushing your teeth', 'Fix a leaking faucet or pipe', 'Collect rainwater for watering plants', 'Wash clothes only when you have a full load', 'Check your home for hidden water leaks', 'Use leftover cooking water to water plants'],
    'Green Transportation': ['Walk or bike for all trips under 2 miles', 'Use public transportatino for your daily commute', 'Carpool with colleagues or friends', 'Plan your errands out to avoid unnecessary trips'],
    'Sustainable Shopping Sprint': ['Buy only local products', 'Avoid purchasing items with excessive packaging', 'Research eco-friendly brands before shopping', 'Choose products with certified sustainable labels', 'Opt for high-quality, durable items over cheap alternatives', 'Support small, local businesses', 'Create a detalied shopping list to avoid inpulse buys', 'Buy in bulk to minimize packaging waste'],
}

# Generate synthetic survey responses
def generate_survey_responses(num_responses):
    responses = []
    for _ in range(num_responses):
        #campaign = random.choice(list(campaigns.keys()))
        #challenge = random.choice(campaigns[campaign])
        response = {
            'lifestyle-rating': random.choice(lifestyle_rating),
            'waste-sorting': random.choice(waste_sorting),
            'avoid-plastics': random.choice(avoid_plastics),
            'plant-meals': random.choice(plant_meals),
            'time-commitment': random.choice(time_commitment),
            'buy-secondhand': random.choice(secondhand_buying),
            'reduce-resources': random.choice(resource_conservation),
            'commute-choice': random.choice(commute_choice),
            #'campaign_recommendation': campaign,
            #'challenge_recommendation': challenge
        }
        responses.append(response)
    return pd.DataFrame(responses)

# Generate synthetic data for 100 users
def main():
    synthetic_data = generate_survey_responses(1500)  # You can change the number of rows here
    data_path = '../data/synthetic_survey_data.csv'
    os.makedirs(os.path.dirname(data_path), exist_ok=True)  # Ensure the data folder exists
    print("Saving file to:", os.path.abspath(data_path))
    synthetic_data.to_csv(data_path, index=False)
    print("Synthetic survey data saved to 'synthetic_survey_data.csv'.")

if __name__ == "__main__":
    main()
