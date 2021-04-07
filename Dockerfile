FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /api
COPY ./api .

RUN useradd user
USER user
