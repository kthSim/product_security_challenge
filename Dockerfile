FROM python:3.6.1

RUN adduser -D zendesksol

WORKDIR /home/zendesksol

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -r requirements

ENV FLASK_APP zendesksol.py

EXPOSE 5000