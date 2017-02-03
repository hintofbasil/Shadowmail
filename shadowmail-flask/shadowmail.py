import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
configPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config')

app.config.from_pyfile(os.path.join(configPath, 'core.cfg'))
app.config.from_pyfile(os.path.join(configPath, os.environ['APP_SETTINGS'] + '.cfg'))

db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "Hello world!"

@app.cli.command()
def initdb():
    db.create_all()

import models

if __name__=='__main__':
    app.run()
