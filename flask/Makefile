test: unit lint

install:
	pip install -r requirements.txt

unit:
	APP_SETTINGS=Testing FLASK_APP=./main.py flask test

lint:
	pylint --disable=missing-docstring,protected-access,fixme --ignore=main.py,config.py ./*.py

ci: install test
