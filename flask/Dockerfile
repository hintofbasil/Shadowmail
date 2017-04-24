FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

ENV FLASK_APP /app/main.py

COPY ./app /app

COPY ./etc /etc

RUN rm /etc/nginx/conf.d/nginx.conf

RUN pip install -r /app/requirements.txt

# Install NodeJS - requires additional repository
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash && apt-get update && apt-get install nodejs -y && rm -rf /var/lib/apt/lists/*

# Install npm and run gulp build
RUN cd /app && npm install && npm install -g gulp-cli && gulp prod
