from flask_mail import Mail, Message
from config import CONFIG

def send_email(to, subject, template, **kwargs):
    msg = Message(CONFIG['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, 
        sender = CONFIG['FLASKY_MAIL_SENDER'],
        recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)