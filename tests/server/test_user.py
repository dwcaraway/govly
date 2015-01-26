# -*- coding: utf-8 -*-
import datetime as dt
import pytest

from flask.ext.security.utils import verify_password

from app.models.users import User, Role
from tests.factories import UserFactory


@pytest.mark.usefixtures('apidb')
class TestUser:

    def test_get(self, user):
        retrieved = User.get(user.id)
        assert retrieved == user

    def test_reset_secret(self, user):
        old_secret = user.secret
        user.reset_secret()
        assert old_secret != user.secret
        user = User.get(user.id)
        assert old_secret != user.secret

    def test_created_at_defaults_to_datetime(self, user):
        assert user.active
        assert bool(user.confirmed_at)
        assert bool(user.last_login_at)
        assert bool(user.current_login_at)
        assert isinstance(user.confirmed_at, dt.datetime)
        assert isinstance(user.last_login_at, dt.datetime)
        assert isinstance(user.current_login_at, dt.datetime)
        assert isinstance(user.secret, basestring)

    def test_password_is_nullable(self):
        user = User(email='foo@bar.com', first_name="foo", last_name="bar")
        user.save()
        assert user.password is None

    def test_factory(self):
        user = UserFactory()
        assert bool(user.email)
        assert bool(user.confirmed_at)
        assert user.active is True
        assert verify_password('password', user.password)

    def test_check_password(self):
        pass
        #user = User.create(username="foo", email="foo@bar.com",
        #            password="foobarbaz123")
        #assert user.check_password('foobarbaz123') is True
        #assert user.check_password("barfoobaz") is False

#   def test_full_name(self):
#       user = UserFactory(first_name="Foo", last_name="Bar")
#       assert user.full_name == "Foo Bar"

    def test_roles(self):
        role = Role(name='admin')
        role.save()
        u = UserFactory()
        u.roles.append(role)
        u.save()
        assert role in u.roles
