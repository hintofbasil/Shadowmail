from main import app

from flask import render_template

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/request_delete')
def template_request_delete():
    return render_template(
        'click_me.html',
        submit_value='Send request'
    )
