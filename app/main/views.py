from flask import render_template

from app.main import main


@main.route('/')
def index():
    return render_template('message.html', message='欢迎光临！')
