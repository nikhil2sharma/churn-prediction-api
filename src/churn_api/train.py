"""Train the churn model and save it with its metrics."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

from . import __version__
from .data import FEATURES, TARGET, make_dataset

DEFAULT_MODEL_DIR = Path("models")


def train(n_samples: int = 2000, seed: int = 42) -> tuple[RandomForestClassifier, dict]:
    df = make_dataset(n_samples, seed)
    x_train, x_test, y_train, y_test = train_test_split(
        df[FEATURES], df[TARGET], test_size=0.2, random_state=seed, stratify=df[TARGET]
    )

    model = RandomForestClassifier(
        n_estimators=200, max_depth=6, min_samples_leaf=10, random_state=seed
    )
    model.fit(x_train, y_train)

    proba = model.predict_proba(x_test)[:, 1]
    majority = max(y_test.mean(), 1 - y_test.mean())
    metrics = {
        "accuracy": round(accuracy_score(y_test, proba >= 0.5), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
        "baseline_accuracy": round(float(majority), 4),
        "n_train": len(x_train),
        "n_test": len(x_test),
    }
    return model, metrics


def save(model: RandomForestClassifier, metrics: dict, model_dir: Path) -> Path:
    model_dir.mkdir(parents=True, exist_ok=True)
    path = model_dir / "model.joblib"
    joblib.dump(model, path)
    meta = {
        "model_version": __version__,
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "features": FEATURES,
        "metrics": metrics,
    }
    (model_dir / "metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="churn-train", description="Train the churn model.")
    parser.add_argument("--out", type=Path, default=DEFAULT_MODEL_DIR, help="model directory")
    parser.add_argument("--samples", type=int, default=2000, help="synthetic rows to generate")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--min-auc", type=float, default=0.70, help="fail if test ROC AUC is below this"
    )
    args = parser.parse_args(argv)

    model, metrics = train(args.samples, args.seed)
    print(json.dumps(metrics, indent=2))
    if metrics["roc_auc"] < args.min_auc:
        print(f"ROC AUC {metrics['roc_auc']} is below {args.min_auc}; model not saved.")
        return 1
    print(f"Saved {save(model, metrics, args.out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
