#!/usr/bin/env python

import os

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_mail import Mail
from prometheus_flask_exporter import PrometheusMetrics

app = FlaskAPI(__name__)

app.config.from_object('config.' + os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

email_limiter = Limiter(app)
ip_limiter = Limiter(app)

mail = Mail(app)

metrics = PrometheusMetrics(app)

from models.virtual_alias import *
from views.api import *
from views.templates import *

@app.cli.command()
def initdb():
    db.create_all()

@app.cli.command()
def test():
    base = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base, 'env')
    node_modules_path = os.path.join(base, 'node_modules')
    import pytest
    exit_code = pytest.main([
                             base,
                             '--ignore=' + env_path,
                             '--ignore=' + node_modules_path,
                             '--verbose'
                           ])
    exit(exit_code)

if __name__ == '__main__':
    app.run()
