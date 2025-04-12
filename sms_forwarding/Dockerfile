FROM python:3.12

WORKDIR /code
EXPOSE 8000

ARG RUNTIME_ENV

ENV RUNTIME_ENV=${RUNTIME_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  # poetry version intentionally pinned
  POETRY_VERSION=1.7.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'
RUN pip install "poetry==$POETRY_VERSION"


COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . .
