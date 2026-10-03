import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- 1. LOAD FINAL DATASET ---
# Make sure the filename matches exactly what you uploaded
data = pd.read_excel("feature_extracted_final_dataset.xlsx")

# --- 2. FEATURES + LABEL ---
# Use underscores for column names
features = ['rms_C', 'energy_C', 'std_C', 'mean_C']
X = data[features]
y = data['Condition']

# --- 3. TRAIN / TEST SPLIT (Avoid Data Leakage) ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 4. TRAIN MODEL ---
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy on Test Set: {accuracy * 100:.2f}%\n")

# --- 5. DEMO PREDICTION (Random Test Sample) ---
# Sample from the test set to simulate a new incoming machine reading
test_sample = X_test.sample(1)

rms = float(test_sample['rms_C'].values[0])
energy = float(test_sample['energy_C'].values[0])
std = float(test_sample['std_C'].values[0])
mean = float(test_sample['mean_C'].values[0])

prediction = model.predict(test_sample)[0]

# --- 6. FAULT RESULT ---
fault = "OVERLOAD FAULT" if prediction == 1 else "NORMAL CONDITION"

# --- 7. WHY FAULT (MULTI LOGIC) ---
reason = []
if rms > 3:
    reason.append("High RMS -> strong signal/stress")
if energy > 150:
    reason.append("High energy -> power surge")
if std > 0.7:
    reason.append("High variation -> unstable behavior")
if mean > 3:
    reason.append("High average current -> sustained load")

# Combined reasoning
if rms > 3 and std > 0.7:
    reason.append("Fluctuating overload condition")
if energy > 150 and mean > 3:
    reason.append("Continuous power stress")
if len(reason) == 0:
    reason.append("All parameters within safe range")

# --- 8. LIFE ESTIMATION ---
# Fixed math to ensure all values are normalized before averaging
health_score = (rms/5 + energy/200 + std/2 + mean/5) / 4
life = max(0, int(100 - health_score * 100))

# --- 9. EARLY WARNING (TREND) ---
recent = data.sample(15)  # Random trend check
alert_list = []

if recent['rms_C'].mean() > 2.8:
    alert_list.append("RMS increasing")
if recent['std_C'].mean() > 0.6:
    alert_list.append("Instability rising")
if recent['energy_C'].mean() > 140:
    alert_list.append("Energy increasing")

if len(alert_list) > 0:
    alert = "EARLY WARNING: " + ", ".join(alert_list)
else:
    alert = "NO ALERT"

# --- 10. OUTPUT ---
print("====================")
print("MACHINE HEALTH REPORT")
print("====================")
print("Fault Status:", fault)
print("\nReason:")
for r in reason:
    print(" -", r)
print(f"\nEstimated Life: {life}%")
print("\nAlert:", alert)
print("\nValues:")
print(f"RMS: {rms:.2f}")
print(f"Energy: {energy:.2f}")
print(f"STD: {std:.2f}")
print(f"Mean Current: {mean:.2f}")