__author__ = 'dave'

from . import MyModelView
from ..models.users import Invite
from wtforms import form, fields, validators, ValidationError
from flask_admin import expose
from flask import current_app, url_for, render_template
from flask_security import current_user
from urlparse import urljoin
from ..framework.utils import generate_invitation_token
from app.framework.utils import send_message
from flask_admin.helpers import get_form_data

class InviteForm(form.Form):
    invitee_email = fields.StringField(u'Email To Invite',
                                       validators=[validators.required(), validators.email()])
    invitor_id = fields.HiddenField()
    token = fields.HiddenField()

class InviteView(MyModelView):

    def __init__(self, session):
        """
        Creates a new view.

        :param session: An SQLAlchemy session object e.g. db.session
        :return: the created instance
        """
        return super(InviteView, self).__init__(Invite, session)

    def create_form(self, obj=None):
        """Overriding the default create form to add some hidden field values"""
        form_data = get_form_data()

        i = InviteForm()

        if form_data:
            i.invitee_email.data = form_data['invitee_email']
            i.invitor_id.data = current_user.id
            i.token.data = generate_invitation_token(current_user)

        return i

    def after_model_change(self, form, model, is_created):
        """
        Override the default after_model_change to send notification email to the invitee.
        called after the model is committed to the database
        """
        if is_created:
            invite_link = urljoin(current_app.config['CLIENT_DOMAIN'], '/#/register?token='+model.token)

            #TODO this mail send should be performed asynchronously using celery, see issue #88850472
            send_message(
                subject="You've been given early access to FogMine",
                sender="do-not-reply@fogmine.com",
                recipients = [model.invitee_email],
                html_body=render_template('email/invite.html', user=current_user, confirmation_link=invite_link),
                text_body=render_template('email/invite.txt', user=current_user, confirmation_link=invite_link)
            )

        return super(InviteView, self).after_model_change(form, model, is_created)

