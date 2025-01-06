# prepare_ml_data.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Load synthetic survey data
data_path = '../data/synthetic_survey_data.csv'  # Adjust path if necessary
df = pd.read_csv(data_path)

# Define campaigns and associated logic
campaign_logic = {
    'Waste-Free Week': lambda row: row['waste-sorting'] in ['Rarely', 'Sometimes', 'Often'] and row['time-commitment'] != '1-10',
    'Energy-Saver': lambda row: row['time-commitment'] in ['1-10', '10-20', '20-30'] and row['reduce-resources'] != 'Daily',
    'Plastic Free': lambda row: row['time-commitment'] not in ['30-45', '45+'] and row['avoid-plastics'] not in ['Never', 'Rarely', 'Daily'],
    'Fast Fashion Detox': lambda row: row['time-commitment'] not in ['1-10', '10-20'] and row['buy-secondhand'] not in ['Never', 'Rarely'] and row['lifestyle-rating'] > 2,
    'Litter Cleanup Challenge': lambda row: row['time-commitment'] in ['20-30', '30-45', '45+'] and row['lifestyle-rating'] > 2,
    'Plant-Based Eating': lambda row: row['plant-meals'] != 'Never' and row['time-commitment'] not in ['1-10'] and row['lifestyle-rating'] > 3,
    'Water-Saver': lambda row: row['reduce-resources'] != 'Never' and row['time-commitment'] in ['10-20', '20-30', '30-45'],
    'Green Transportation': lambda row: row['commute-choice'] not in ['Walk', 'Bike', 'None'] and row['lifestyle-rating'] > 2,
    'Sustainable Shopping Sprint': lambda row: row['buy-secondhand'] != 'Never' and row['avoid-plastics'] != 'Never' and row['time-commitment'] not in ['1-10', '10-20'],
}

# Function to count True results for each campaign
def count_true_results(df, campaign_logic):
    true_counts = {campaign: 0 for campaign in campaign_logic}  # Initialize dictionary to store counts
    for _, row in df.iterrows():
        for campaign, logic in campaign_logic.items():
            if logic(row):
                true_counts[campaign] += 1
    return true_counts

# Count the number of True results for each campaign
true_counts = count_true_results(df, campaign_logic)

# Print the number of True results for each campaign
for campaign, count in true_counts.items():
    print(f"{campaign}: {count} True results")

def recommend_campaign(row):
    for campaign, logic in campaign_logic.items():
        if logic(row):
            return campaign
    return 'Fast Fashion Detox'  # Default if no other logic matches

df['campaign_recommendation'] = df.apply(recommend_campaign, axis=1)

# Encode categorical variables
categorical_columns = [
    'waste-sorting', 'avoid-plastics', 'plant-meals', 
    'time-commitment', 'buy-secondhand', 'reduce-resources', 
    'commute-choice'
]
encoder = OneHotEncoder()
encoded_features = encoder.fit_transform(df[categorical_columns]).toarray()

# Combine encoded features with numerical columns
numeric_columns = ['lifestyle-rating']
X = pd.concat([pd.DataFrame(encoded_features), df[numeric_columns]], axis=1)

# Check if the 'campaign_recommendation' is populated correctly
print(df['campaign_recommendation'].unique())

# If it's not populated correctly, make sure your logic is assigning campaigns as expected
df['campaign_recommendation'] = df.apply(recommend_campaign, axis=1)

# Verify a sample of the DataFrame to ensure correct recommendations
print(df[['time-commitment', 'reduce-resources', 'campaign_recommendation']].head())

# Encode target columns
label_encoder = LabelEncoder()
y_campaign = label_encoder.fit_transform(df['campaign_recommendation'])

# Verify the unique labels after encoding
print(label_encoder.classes_)

# Split into training and testing sets
X_train, X_test, y_campaign_train, y_campaign_test = train_test_split(
    X, y_campaign, test_size=0.2, random_state=42
)

# Save prepared datasets
X_train.to_csv('../data/X_train.csv', index=False)
X_test.to_csv('../data/X_test.csv', index=False)
pd.Series(y_campaign_train).to_csv('../data/y_campaign_train.csv', index=False)
pd.Series(y_campaign_test).to_csv('../data/y_campaign_test.csv', index=False)

print("Data preparation completed. Encoded data and campaign recommendations saved.")
