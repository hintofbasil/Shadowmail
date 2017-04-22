#!/usr/bin/env python

import os
from flask import Flask
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_mail import Mail

app = FlaskAPI(__name__)

app.config.from_object('config.' + os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

limiter = Limiter(app)

mail = Mail(app)

from models.virtual_alias import *
from views.api import *

if app.config['DEVELOPMENT']:
    @app.route('/')
    def hello():
        return """<html>
        <head>
            <link rel="stylesheet" type="text/css" href="static/css/homepage.css" />
        </head>
        <body>
            <div id="test"></div>
            <script src="static/js/bundle.js"></script>
        </body>
    </html>"""

@app.cli.command()
def initdb():
    db.create_all()

@app.cli.command()
def test():
    import pytest
    rv = pytest.main(['/home/will/Workspace/shadowmail/flask/app',
                      '--ignore=env', '--ignore=node_modules', '--verbose'])
    exit(rv)

if __name__=='__main__':
    app.run()
