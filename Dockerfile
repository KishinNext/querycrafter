FROM python:3.9.16-slim-buster as base

WORKDIR /app


ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.2


RUN pip install "poetry==$POETRY_VERSION"


COPY poetry.lock pyproject.toml /app/


RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8080

CMD ["python", "-m", "app"]

FROM base as final




