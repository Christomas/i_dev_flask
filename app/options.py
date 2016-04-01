import os
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(
        app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def dump_token(key, value, secret_key=os.environ.get('SECRET_KEY')):
    s = Serializer(secret_key, expires_in=3600)
    return s.dumps({key: value})


def load_token(token, key, secret_key=os.environ.get('SECRET_KEY')):
    s = Serializer(secret_key)
    try:
        data = s.loads(token)
    except:
        return None
    return data.get(key)
