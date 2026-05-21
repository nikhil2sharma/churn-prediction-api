# ml/train.py
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train():
    # Load labeled data (supervised — every row has a target)
    df = pd.read_csv("data/customer_churn.csv")

    X = df.drop("churned", axis=1)   # features
    y = df["churned"]                # label (0 = stayed, 1 = churned)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Chef learns the recipe
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Quick quality check
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Accuracy: {acc:.4f}")

    # Save the chef to a file
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    # Return accuracy for the health inspector to verify
    return acc

if __name__ == "__main__":
    train()