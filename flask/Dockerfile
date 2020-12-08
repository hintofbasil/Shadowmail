FROM python:3.9.1

ENV PORT 8000

ENV APP_SETTINGS Development
ENV DB_PASSWORD "change_me"
ENV SECRET_KEY "change_me"
ENV FLASK_DEBUG 1
ENV RELOAD ""


ENV APP_HOME /app
WORKDIR $APP_HOME

COPY ./requirements.txt $APP_HOME/requirements.txt
RUN pip install -r $APP_HOME/requirements.txt
RUN pip install gunicorn

COPY . $APP_HOME

CMD exec gunicorn --bind :$PORT --workers 1 main:app $RELOAD
