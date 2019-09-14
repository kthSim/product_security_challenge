from flask_mail import Message
from flask import render_template
from project import mail, app


def send_mail (subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_email_password_reset(user):
    token = user.get_token_reset_password()
    mail_subject = "[ZenDeskSol] Reset Your Password"
    text_body = render_template('email/reset_password.txt', user=user, token=token)
    html_body = render_template('email/reset_password.html', user=user, token=token)

    send_mail(mail_subject, app.config['ADMINS'][0], [user.email], text_body, html_body)
