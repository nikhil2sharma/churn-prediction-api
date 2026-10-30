# churn-api

[![CI](https://github.com/nikhil2sharma/ML-Supervised_Learning-Test_Linear_Reg/actions/workflows/ci.yml/badge.svg)](https://github.com/nikhil2sharma/ML-Supervised_Learning-Test_Linear_Reg/actions/workflows/ci.yml)

An end-to-end churn prediction service: a scikit-learn training pipeline with a
quality gate, and a FastAPI app that serves the model. Runs locally with `uv` or
as a Docker container.

> The dataset is synthetic. It's generated so that churn depends on contract
> type, monthly charges and support calls, which gives the model a real signal
> to learn.

## Quick start

```bash
uv sync
uv run churn-train                     # trains, prints metrics, saves models/
uv run uvicorn churn_api.api:app --reload
```

Open http://localhost:8000/docs for the Swagger UI, or:

```bash
curl -X POST localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "contract_type": 0, "monthly_charges": 480, "support_calls": 10}'
```

```json
{"churn": true, "probability": 0.9397, "model_version": "1.0.0"}
```

### Docker

```bash
docker build -t churn-api .            # trains the model during the build
docker run --rm -p 8000:8000 churn-api
```

## How it works

```
make_dataset() ──► train/test split ──► RandomForest ──► quality gate ──► models/
                                                         (ROC AUC ≥ 0.70)    │
                                                                             ▼
                          client ──► POST /predict ──► FastAPI (model loaded at startup)
```

- **Training** (`churn-train`) reports accuracy, ROC AUC and the majority-class
  baseline, and refuses to save a model whose AUC is below `--min-auc`.
- **Artifacts**: `models/model.joblib` plus `metadata.json` (version, timestamp,
  features, metrics). Models are not committed to git.
- **Serving**: the model is loaded once in the FastAPI lifespan hook. If it's
  missing, `/health` reports `model_missing` and `/predict` returns `503`
  instead of crashing.
- **Validation**: Pydantic rejects out-of-range input (e.g. `age < 18`,
  `contract_type` not 0/1) with `422`.

## API

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | `{"status": "ok", "model_version": "1.0.0"}` |
| `POST` | `/predict` | churn flag, probability and model version |
| `GET` | `/docs` | interactive API docs |

Request fields: `age` (18–100), `contract_type` (0 = monthly, 1 = yearly),
`monthly_charges` (≥ 0), `support_calls` (≥ 0).

Set `CHURN_MODEL_DIR` to load the model from a different directory.

## Development

```bash
uv run pytest        # trains small models in temp dirs; no setup needed
uv run ruff check .
```

CI runs lint, tests, a training run and a Docker build on every push.

## Project layout

```
src/churn_api/
    data.py      synthetic dataset
    train.py     training, metrics, quality gate, churn-train CLI
    schemas.py   request/response models
    api.py       FastAPI app
tests/
Dockerfile
```

## Roadmap

- [ ] Track experiments with MLflow
- [ ] Batch prediction endpoint
- [ ] Drift check on incoming requests

## License

MIT
