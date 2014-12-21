# -*- coding: utf-8 -*-
"""
    tests.factories
    ~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from datetime import datetime
from factory import Factory, Sequence, LazyAttribute, post_generation
from flask.ext.security.utils import encrypt_password

from app.models.users import User, Role
from app.models.model import Organization
from app.framework.sql import db

class BaseFactory(Factory):
    ABSTRACT_FACTORY = True

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        entity = target_class(**kwargs)
        db.session.add(entity)
        db.session.commit()
        return entity

class RoleFactory(BaseFactory):
    FACTORY_FOR = Role
    name = 'admin'
    description = 'Administrator'

class UserFactory(BaseFactory):
    FACTORY_FOR = User
    email = Sequence(lambda n: 'user{0}@foobar.com'.format(n))
    confirmed_at = datetime.utcnow()
    last_login_at = datetime.utcnow()
    current_login_at = datetime.utcnow()
    last_login_ip = '127.0.0.1'
    current_login_ip = '127.0.0.1'
    login_count = 1
    active = True

    @post_generation
    def password(self, create, extracted, **kwargs):
        self.password = encrypt_password(extracted or "password")

class OrganizationFactory(BaseFactory):
    FACTORY_FOR = Organization
    legalName = Sequence(lambda n: 'legalname{0}'.format(n))
