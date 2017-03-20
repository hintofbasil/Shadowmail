FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

ENV FLASK_APP /app/main.py

COPY ./app /app

RUN pip install -r /app/requirements.txt

# Install NodeJS - requires additional repository
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash && apt-get update && apt-get install nodejs -y && rm -rf /var/lib/apt/lists/*

# Install npm and run gulp build
RUN cd /app && npm install && npm install -g gulp-cli && sed -i -E "s/debug: false/debug: true/g" /app/gulpfile.js && gulp build

# Must remove from /app/dist as find doesn't search simlinks properly
RUN ln -s /app/dist /app/static && find /app/dist -name *.js.map -exec rm {} \;
