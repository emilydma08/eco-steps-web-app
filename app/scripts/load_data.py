import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
import joblib


# Load data
x_train = pd.read_csv('../data/x_train.csv')
x_test = pd.read_csv('../data/x_test.csv')
y_train = pd.read_csv('../data/y_campaign_train.csv')
y_test = pd.read_csv('../data/y_campaign_test.csv')

y_train = y_train.values.ravel()  # Flatten y_train
y_test = y_test.values.ravel()    # Flatten y_test


# View data summary
print("X_train shape:", x_train.shape)
print("X_test shape:", x_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)

print("Class distribution in y_train:")
print(pd.Series(y_train).value_counts())

print("Class distribution in y_test:")
print(pd.Series(y_test).value_counts())

# Initialize the scaler
scaler = StandardScaler()

# Scale the training and testing sets
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

#Apply SMOTE to balance training data
smote = SMOTE(sampling_strategy={2: 100, 3: 50, 4: 100, 5: 50, 6: 50, 8: 50}, random_state=42, k_neighbors=5)
x_train_resampled, y_train_resampled = smote.fit_resample(x_train_scaled, y_train)

print("Class distribution in y_train (after SMOTE):")
print(pd.Series(y_train_resampled).value_counts())


# Train a Random Forest model
class_weights = {0: 1, 1: 5, 2: 20, 3: 7, 4: 20, 5: 8, 6: 6, 7: 1, 8: 15}
rf_model = RandomForestClassifier(n_estimators=1400, max_depth=30, min_samples_leaf=5, random_state=42, class_weight=class_weights)
rf_model.fit(x_train_resampled, y_train_resampled)

# Make predictions
y_pred = rf_model.predict(x_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=1))

joblib.dump(rf_model, '../ml_model/recommendation_model.pkl')
print("Model saved as recommendation_model.pkl")