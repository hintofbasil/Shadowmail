from main import app

from flask import render_template, request

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/request_delete')
def template_request_delete():
    return render_template(
        'request_delete.html',
        url_args=request.args
    )

@app.route('/delete')
def template_delete():
    return render_template(
        'confirm_delete.html',
        url_args=request.args
    )
