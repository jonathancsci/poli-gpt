FROM pytorch/pytorch:latest

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install -r /backend/requirements.txt

COPY ./app /backend/app