import logging
from .. import framework
from ..framework.sql import db
from flask_admin import Admin, expose, AdminIndexView, helpers, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, login_user, logout_user
from flask import url_for, redirect, request
from wtforms import form, fields, validators
from ..framework.security import authenticate
from ..models.users import User

_log = logging.getLogger(__name__)


def create_app(settings_override=None):
    """Returns an Admin application instance."""

    # Create and extend a minimal application
    app = framework.create_app(__name__, __path__, settings_override, security_register_blueprint=False)

    from .invite_view import InviteView
    from .user_view import UserView

    #Init the flask-admin
    admin = Admin(app, name='FogMine Admin', url='/', index_view=MyAdminIndexView(url='/'), template_mode='bootstrap3', base_template='admin/my_master.html')
    admin.add_view(UserView(db.session))
    admin.add_view(InviteView(db.session))

    return app

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    email = fields.StringField(validators=[validators.required(), validators.email()])
    password = fields.PasswordField(validators=[validators.required()])

# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        if current_user.is_authenticated():
            return redirect(url_for('.index'))

        # handle user login
        form = LoginForm(request.form)

        if helpers.validate_form_on_submit(form):
            user = authenticate(username=form.email.data, password=form.password.data)

            if user:
                if user.has_role('admin'):
                    if login_user(user):
                        redirect(url_for('.index'))
                    else:
                        self._template_args['error'] = "User is not active or could not be logged in."
                else:
                    self._template_args['error'] = "User has insufficient privilege."
            else:
                self._template_args['error'] = "Invalid user and/or password"

        self._template_args['form'] = form
        return self.render('admin/login.html')

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.login_view'))

class MyModelView(ModelView):

    def is_accessible(self):
        """Runs before each view access, ensures that we have the correct admin role"""
        if current_user.is_authenticated() and current_user.has_role('admin'):
            return True

        return False

class MyBaseView(BaseView):

    def is_accessible(self):
        """Runs before each view access, ensures that we have the correct admin role"""
        if current_user.is_authenticated() and current_user.has_role('admin'):
            return True

        return False
