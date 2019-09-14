FROM python:3.6.1

RUN adduser zendesksol

WORKDIR /home/zendesksol

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

WORKDIR /home/zendesksol/venv

COPY project ./venv/project
COPY migrations ./venv/migrations
COPY zendesksol.py config.py ./venv/ 

RUN chown -R zendesksol:zendesksol ./
USER zendesksol

EXPOSE 5000

ENV FLASK_APP zendesksol.py

CMD cd venv/ && pwd && ls -la && ../bin/flask db upgrade && ../bin/flask run -h '0.0.0.0'

