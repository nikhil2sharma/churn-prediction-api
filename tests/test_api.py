import pytest
from fastapi.testclient import TestClient

from churn_api.api import app
from churn_api.train import save, train

HIGH_RISK = {"age": 30, "contract_type": 0, "monthly_charges": 480.0, "support_calls": 10}
LOW_RISK = {"age": 55, "contract_type": 1, "monthly_charges": 60.0, "support_calls": 0}


@pytest.fixture(scope="module")
def model_dir(tmp_path_factory):
    path = tmp_path_factory.mktemp("models")
    model, metrics = train(n_samples=1500, seed=0)
    save(model, metrics, path)
    return path


@pytest.fixture
def client(model_dir, monkeypatch):
    monkeypatch.setenv("CHURN_MODEL_DIR", str(model_dir))
    with TestClient(app) as c:
        yield c


def test_health_ok(client):
    assert client.get("/health").json() == {"status": "ok", "model_version": "1.0.0"}


def test_predict_returns_probability(client):
    body = client.post("/predict", json=HIGH_RISK).json()
    assert 0 <= body["probability"] <= 1
    assert body["model_version"] == "1.0.0"


def test_high_risk_scores_above_low_risk(client):
    high = client.post("/predict", json=HIGH_RISK).json()["probability"]
    low = client.post("/predict", json=LOW_RISK).json()["probability"]
    assert high > low


@pytest.mark.parametrize(
    "patch",
    [{"age": 5}, {"contract_type": 2}, {"monthly_charges": -1}, {"support_calls": "many"}],
)
def test_invalid_input_rejected(client, patch):
    assert client.post("/predict", json={**HIGH_RISK, **patch}).status_code == 422


def test_missing_model_returns_503(tmp_path, monkeypatch):
    monkeypatch.setenv("CHURN_MODEL_DIR", str(tmp_path))
    with TestClient(app) as c:
        assert c.get("/health").json()["status"] == "model_missing"
        assert c.post("/predict", json=HIGH_RISK).status_code == 503
