from flask import render_template
from flask_mail import Message
from app import app, mail
from app.models import User

from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, html_body, cc):
    msg = Message(subject, recipients=recipients, cc=cc, sender=app.config['MAIL_USERNAME'])
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
    #send_async_email(app, msg)
    '''try:
        mail.send(msg)
    except TimeoutError:
        pass'''

def email_user(subject, body, job, user):
    send_email(subject, cc=None,
               recipients=['michaelb@rods.sk.ca'],#employment@rods.sk.ca
               html_body=render_template('notification.html', body=body, user=user, job=job))


def send_registration_confirmation_email(email, name, token, two_factor_auth_code):
    send_email('Biogenix app email confirmation.',
               #sender=app.config['ADMINS'][0],
               recipients=[email], cc=None,
               html_body=render_template('email/registration_confirmation.html', name=name, token=token, two_factor_auth_code=two_factor_auth_code))


