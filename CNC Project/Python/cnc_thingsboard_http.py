import pandas as pd
import numpy as np
import requests
import time
from sklearn.ensemble import RandomForestClassifier

ACCESS_TOKEN     = "k3n2tffuowiyhsn7hrgx"
THINGSBOARD_HOST = "https://demo.thingsboard.io"
URL              = f"{THINGSBOARD_HOST}/api/v1/{ACCESS_TOKEN}/telemetry"

# ── Load dataset ──────────────────────────────────────
data = pd.read_excel("feature_extracte_dfinal_dataset.xlsx")
features = ['rms_C', 'energy_C', 'std_C', 'mean_C']
X = data[features]
y = data['Condition']

# ── Train model ───────────────────────────────────────
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
print("✅ Model trained!")

# ── Test connection ───────────────────────────────────
print("\n🔄 Testing connection to ThingsBoard...")
try:
    r = requests.post(URL, json={"test": "ping"}, timeout=15)
    print(f"   Server response code: {r.status_code}")
    if r.status_code == 200:
        print("✅ Connected! Data is flowing to ThingsBoard!")
    elif r.status_code == 401:
        print("❌ Token rejected (401). Try regenerating token in ThingsBoard.")
        exit()
    else:
        print(f"⚠️ Unexpected: {r.status_code} — {r.text}")
        exit()
except requests.exceptions.ConnectionError as e:
    print(f"❌ Cannot reach ThingsBoard. Check internet. Error: {e}")
    exit()
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    exit()

# ── Send data loop ────────────────────────────────────
print("\n🚀 Sending data every 5 seconds... (Ctrl+C to stop)\n")

try:
    while True:
        sample = data.sample(1)
        rms    = float(sample['rms_C'].values[0])
        energy = float(sample['energy_C'].values[0])
        std    = float(sample['std_C'].values[0])
        mean   = float(sample['mean_C'].values[0])

        prediction   = model.predict(sample[features])[0]
        fault_status = "OVERLOAD FAULT" if prediction == 1 else "NORMAL"
        fault_value  = int(prediction)

        reasons = []
        if rms > 3:                    reasons.append("High RMS")
        if energy > 150:               reasons.append("High Energy")
        if std > 0.7:                  reasons.append("High Variation")
        if mean > 3:                   reasons.append("High Mean Current")
        if rms > 3 and std > 0.7:      reasons.append("Fluctuating Overload")
        if energy > 150 and mean > 3:  reasons.append("Continuous Power Stress")
        if not reasons:                reasons.append("All parameters safe")

        health_score = (rms/5 + energy/200 + std + mean/5) / 4
        life = max(0, int(100 - health_score * 100))

        recent = data.sample(15)
        alerts = []
        if recent['rms_C'].mean() > 2.8:    alerts.append("RMS Increasing")
        if recent['std_C'].mean() > 0.6:    alerts.append("Instability Rising")
        if recent['energy_C'].mean() > 140: alerts.append("Energy Increasing")
        alert_msg = " | ".join(alerts) if alerts else "NO ALERT"

        payload = {
            "fault_status": fault_status,
            "fault_value":  fault_value,
            "rms":          round(rms, 3),
            "energy":       round(energy, 3),
            "std":          round(std, 3),
            "mean_current": round(mean, 3),
            "machine_life": life,
            "reason":       " | ".join(reasons),
            "alert":        alert_msg,
            "has_alert":    1 if alerts else 0
        }

        try:
            response = requests.post(URL, json=payload, timeout=15)
            if response.status_code == 200:
                print(f"[SENT ✅] {fault_status} | Life: {life}% | Alert: {alert_msg}")
                print(f"          RMS={rms:.2f} | Energy={energy:.2f} | STD={std:.2f} | Mean={mean:.2f}\n")
            else:
                print(f"[ERROR ❌] Status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[NETWORK ERROR ❌] {e}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n🛑 Stopped. Goodbye!")
