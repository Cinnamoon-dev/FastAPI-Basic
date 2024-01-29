FROM python:3.11.7-alpine

WORKDIR /api

COPY ./docker/requirements.txt ./docker/requirements.txt

RUN pip install -r docker/requirements.txt

COPY . .

RUN python3 -m app.database.insertData

ENTRYPOINT ["python3", "main.py"]