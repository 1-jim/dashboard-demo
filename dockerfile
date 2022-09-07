FROM python:3.10-slim-buster
RUN apt-get update
RUN apt-get install nano
RUN pip install --upgrade pip
RUN mkdir wd
WORKDIR /wd
COPY requirements.txt
COPY app/ ./
CMD gunicorn -b 0.0.0.0:80 app:server