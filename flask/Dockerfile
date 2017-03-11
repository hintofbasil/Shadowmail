FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

ENV FLASK_APP /app/main.py

COPY ./app /app

RUN pip install -r /app/requirements.txt
