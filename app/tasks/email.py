# -*- coding: utf-8 -*-
"""
    tasks.email
    ~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.
"""
from flask.ext.mail import Message

from ..framework.extensions import mail, celery

@celery.task()
def send_email(message):
    mail.send(message)

@celery.task()
def send_message(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_email.delay(msg)
