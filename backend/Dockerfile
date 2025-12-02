FROM python:3.13-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --compile-bytecode --link-mode=copy

COPY scripts/download_models.py .

ENV HF_HOME="/app/hf_cache"
ARG TRANSFORMER_MODEL="nlptown/bert-base-multilingual-uncased-sentiment"

RUN python download_models.py --model_name "${TRANSFORMER_MODEL}"

FROM python:3.13-slim as runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME="/home/app/.cache/huggingface" \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system app && adduser --system --group app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv ./.venv

RUN mkdir -p ${HF_HOME} && chown app:app ${HF_HOME}
COPY --from=builder --chown=app:app /app/hf_cache ${HF_HOME}

COPY --chown=app:app ./app ./app
COPY --chown=app:app entrypoint.sh .

COPY --chown=app:app ./alembic ./alembic
COPY --chown=app:app alembic.ini .

RUN chmod +x entrypoint.sh

USER app

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]