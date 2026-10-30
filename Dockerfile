FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev && churn-train --out /app/models

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "churn_api.api:app", "--host", "0.0.0.0", "--port", "8000"]
