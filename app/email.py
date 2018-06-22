from flask_mail import Mail, Message
from flask import current_app, render_template

def send_email(to, subject, template, **kwargs):
    mail = Mail()
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, 
        sender = app.config['FLASKY_MAIL_SENDER'],
        recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)