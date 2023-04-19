FROM python:3.10-slim-bullseye as build-env-image

ENV DEBIAN_FRONTEND noninteractive
ENV PROJECT_ROOT "/app"

WORKDIR "${PROJECT_ROOT}"

RUN set -eu; \
    apt-get update; \
    apt-get install -y --no-install-recommends build-essential curl \
        libpq-dev; \
    curl -sSL https://install.python-poetry.org | python -;

COPY pyproject.toml poetry.lock "${PROJECT_ROOT}"/

RUN set -eu; \
    export PATH="/root/.local/bin:$PATH"; \
    poetry config virtualenvs.in-project true; \
    poetry install --no-dev;


FROM python:3.10-slim-bullseye

ENV PROJECT_ROOT "/app"
ENV PATH="${PROJECT_ROOT}/.venv/bin:${PATH}"
ENV PYTHONOPTIMIZE=1
ENV USER=mariner

WORKDIR "${PROJECT_ROOT}"

RUN set -eu; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl procps libpq5 \
      libcairo2 libglib2.0 libpango1.0 fonts-lato;

RUN rm -rf /var/lib/apt/lists/*;

# Create user and runtime dirs / files
RUN set -eu; \
    useradd --create-home --comment "Mariner User" --uid 1000 "${USER}";

COPY --from=build-env-image "${PROJECT_ROOT}/.venv" "${PROJECT_ROOT}/.venv"

COPY src "${PROJECT_ROOT}"

# Compile bytecode for faster startup
RUN python -m compileall *

CMD ["uwsgi", "--ini", "uwsgi.ini"]
