FROM node:8 as static

ENV STATIC_HOME /static
WORKDIR $STATIC_HOME
COPY static $STATIC_HOME


RUN npm install \
    && npm install -g gulp-cli \
    && gulp prod \
    && cp -r /$STATIC_HOME/images /$STATIC_HOME/out

FROM python:3.7

ENV PORT 8000

ENV APP_SETTINGS Development
ENV DB_PASSWORD "change_me"
ENV SECRET_KEY "change_me"
ENV FLASK_DEBUG=1

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY app $APP_HOME

RUN pip install -r $APP_HOME/requirements.txt
RUN pip install gunicorn

COPY --from=static /static/out /app/static

CMD exec gunicorn --bind :$PORT --workers 1 main:app
