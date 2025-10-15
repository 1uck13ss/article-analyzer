#building stage
FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN uv venv

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --compile-bytecode --no-install-project

ADD . /app

#runtime stage
FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates 

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]