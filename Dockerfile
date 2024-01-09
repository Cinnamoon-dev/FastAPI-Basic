FROM python:3.11.7-alpine

WORKDIR /api

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

ENTRYPOINT ["python3", "main.py"]