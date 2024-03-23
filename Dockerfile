FROM python:3

WORKDIR /education_schedule_docker

COPY ./requirements.txt /education_schedule_docker/

RUN pip install -r requirements.txt

COPY . .

