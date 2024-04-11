FROM python:3.11.7-alpine as test

WORKDIR /api

COPY ./docker/requirements.txt ./docker/requirements.txt

RUN pip install -r docker/requirements.txt

COPY . .

ENTRYPOINT ["pytest"]

FROM python:3.11.7-alpine 

WORKDIR /api

COPY ./docker/requirements.txt ./docker/requirements.txt

RUN pip install -r docker/requirements.txt

COPY . .

ENTRYPOINT ["python3", "main.py"]