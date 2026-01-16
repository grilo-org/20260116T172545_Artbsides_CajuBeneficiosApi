FROM python:3.12.3-alpine AS development

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    pip install --user poetry-plugin-export

RUN poetry export --output requirements.txt --with-credentials --no-interaction
RUN poetry export --output requirements.dev.txt --with-credentials --no-interaction --with dev

RUN pip install -r requirements.dev.txt --require-hashes --no-cache-dir && \
    pip uninstall poetry --yes

ENV PYTHONPATH=/app

FROM python:3.12.3-alpine

WORKDIR /app

COPY --chown=appuser --from=development app/requirements.txt .
COPY --chown=appuser --from=development app/api ./api

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --require-hashes --no-cache-dir

RUN rm requirements.txt

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

USER appuser

ENV APP_HOST=${APP_HOST:-0.0.0.0} \
    APP_HOST_PORT=${APP_HOST_PORT:-8000}

ENV PYTHONPATH=/app

CMD ["sh", "-c", "gunicorn api.main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker --bind=${APP_HOST}:${APP_HOST_PORT}"]
