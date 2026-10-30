import json

from churn_api.data import FEATURES, TARGET, make_dataset
from churn_api.train import main, train


def test_dataset_shape_and_ranges():
    df = make_dataset(500, seed=1)
    assert list(df.columns) == FEATURES + [TARGET]
    assert len(df) == 500
    assert df["contract_type"].isin([0, 1]).all()
    assert df[TARGET].isin([0, 1]).all()


def test_dataset_is_reproducible():
    assert make_dataset(100, seed=7).equals(make_dataset(100, seed=7))


def test_model_beats_baseline():
    _, metrics = train(n_samples=2000, seed=42)
    assert metrics["roc_auc"] > 0.7
    assert metrics["accuracy"] > metrics["baseline_accuracy"]


def test_cli_saves_model_and_metadata(tmp_path):
    assert main(["--out", str(tmp_path), "--samples", "800"]) == 0
    assert (tmp_path / "model.joblib").exists()
    meta = json.loads((tmp_path / "metadata.json").read_text())
    assert meta["features"] == FEATURES
    assert "roc_auc" in meta["metrics"]


def test_cli_refuses_weak_model(tmp_path):
    assert main(["--out", str(tmp_path), "--samples", "800", "--min-auc", "0.99"]) == 1
    assert not (tmp_path / "model.joblib").exists()
