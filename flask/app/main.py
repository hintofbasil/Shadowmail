#!/usr/bin/env python

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.' + os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

from models.virtual_alias import *

@app.route('/')
def hello():
    return "Hello world!"

@app.cli.command()
def initdb():
    db.create_all()

@app.cli.command()
def test():
    import pytest
    rv = pytest.main(['/home/will/Workspace/shadowmail/flask/app', '--ignore=env', '--verbose'])
    exit(rv)

if __name__=='__main__':
    app.run()
