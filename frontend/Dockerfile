#building stage
FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app/frontend

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --compile-bytecode

COPY . .

#runtime stage
FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates 

COPY --from=builder /app/frontend/.venv /app/frontend/.venv
COPY --from=builder /app/frontend /app/frontend

ENV PATH="/app/frontend/.venv/bin:$PATH"

WORKDIR /app/frontend

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
