FROM python:3.12

WORKDIR /finni

COPY pyproject.toml ./poetry.lock ./
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install --no-root
RUN poetry show

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE}

COPY ../../../Downloads/Backend .
