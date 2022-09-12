FROM python:3.10.5

WORKDIR /code
COPY . .
RUN python3 -m pip install poetry
RUN poetry install
CMD poetry run uvicorn app.__main__:app --host 0.0.0.0 --port ${APP_PORT} --reload