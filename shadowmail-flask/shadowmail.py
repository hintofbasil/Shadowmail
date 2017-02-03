import os
from flask import Flask

app = Flask(__name__)
configPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config')

app.config.from_pyfile(os.path.join(configPath, 'core.cfg'))
app.config.from_pyfile(os.path.join(configPath, os.environ['APP_SETTINGS'] + '.cfg'))

@app.route('/')
def hello():
    return "Hello world!"

if __name__=='__main__':
    app.run()
