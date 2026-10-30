"""Synthetic customer data with a learnable churn signal."""

import numpy as np
import pandas as pd

FEATURES = ["age", "contract_type", "monthly_charges", "support_calls"]
TARGET = "churned"


def make_dataset(n_samples: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Generate customers where churn depends on contract, charges and support calls.

    Month-to-month customers with high bills and many support calls are the most
    likely to churn. Noise keeps the problem from being trivially separable.
    """
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "age": rng.integers(18, 71, n_samples),
            "contract_type": rng.integers(0, 2, n_samples),  # 0 = monthly, 1 = yearly
            "monthly_charges": np.round(rng.uniform(50, 500, n_samples), 2),
            "support_calls": rng.integers(0, 11, n_samples),
        }
    )
    logit = (
        -0.6
        - 1.8 * df["contract_type"]
        + 0.006 * (df["monthly_charges"] - 275)
        + 0.45 * (df["support_calls"] - 5)
        - 0.01 * (df["age"] - 44)
    )
    prob = 1 / (1 + np.exp(-logit))
    df[TARGET] = (rng.random(n_samples) < prob).astype(int)
    return df
