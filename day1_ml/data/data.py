# ml/create_sample_data.py
import pandas as pd
import numpy as np

def create_sample_data(n_samples=1000):
    np.random.seed(42)

    df = pd.DataFrame({
        "age":              np.random.randint(18, 70, n_samples),
        "contract_type":    np.random.randint(0, 2, n_samples),   # 0=monthly, 1=yearly
        "monthly_charges":  np.round(np.random.uniform(50, 500, n_samples), 2),
        "support_calls":    np.random.randint(0, 10, n_samples),
        
        # Label — this is what makes it SUPERVISED
        "churned":          np.random.randint(0, 2, n_samples)
    })

    # Save to data folder
    import os
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/customer_churn.csv", index=False)
    print(f"✅ Created data/customer_churn.csv with {n_samples} rows")
    print(df.head())

if __name__ == "__main__":
    create_sample_data()