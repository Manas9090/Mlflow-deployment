import mlflow
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from email_utils import send_email_alert  # ✅ Correct

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("drift-monitoring")

def check_and_alert(feature_name, old_data, new_data):
    stat, p_value = ks_2samp(old_data, new_data)
    drift = p_value < 0.05

    with mlflow.start_run(run_name=f"{feature_name}-drift-check"):
        mlflow.log_metric(f"{feature_name}_ks_p_value", p_value)

        plt.figure()
        sns.histplot(old_data, color='blue', label='old', kde=True, stat="density")
        sns.histplot(new_data, color='red', label='new', kde=True, stat="density")
        plt.legend()
        plt.title(f"Drift in {feature_name} | p={p_value:.4f}")
        filename = f"{feature_name}_dist_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
        plt.savefig(filename)
        mlflow.log_artifact(filename)

    if drift:
        subject = f"⚠️ Drift Detected in {feature_name}"
        body = f"Drift detected in feature '{feature_name}'\nKS p-value = {p_value:.4f}"
        send_email_alert(subject, body, to_email="your_email@gmail.com")
        print(subject)
    else:
        print(f"No drift in {feature_name} | p={p_value:.4f}")

# Simulate or load actual data
old = pd.read_csv("baseline_data.csv")
new = pd.read_csv("latest_data.csv")

for col in ["feature1", "feature2", "feature3"]:  # Replace with your actual features
    check_and_alert(col, old[col], new[col])
