#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    vitals.manage
    ~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from flask.ext.script import Command, Manager, Option, Shell, Server, prompt_bool
from flask.ext.migrate import MigrateCommand, upgrade
from werkzeug.serving import run_simple

from app import create_app
from app.framework.sql import db
from app.models.users import User
import os

application = create_app(override_settings=os.environ.get('APPLICATION_SETTINGS', 'app.settings.DevelopmentConfig'))

manager = Manager(application.mounts['/api'])
TEST_CMD = "py.test ./tests/server"

from app.framework.extensions import celery
celery.init_app(application.mounts['/api'])

class Worker(Command):

    option_list = (
        Option('-c', '--concurrency', dest='concurrency', default='1'),
        Option('-l', '--loglevel', dest='loglevel', default='debug'),
    )

    def run(self, concurrency, loglevel):
        celery.start(argv=['worker.py', 'worker',
                           '--concurrency', concurrency,
                           '--loglevel', loglevel,
                           ])

class WSGI(Server):

    def __call__(self, app, host, port, use_debugger, use_reloader,
                 threaded, processes, passthrough_errors):

        if use_debugger is None:
            use_debugger = app.debug

        if use_debugger is None:
            use_debugger = True

        if use_reloader is None:
            use_reloader = use_debugger

        run_simple(host, port, application,
                   use_debugger=use_debugger,
                   use_reloader=use_reloader,
                   threaded=threaded,
                   processes=processes,
                   passthrough_errors=passthrough_errors,
                   **self.server_options)

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {
        'app': application,
        'db': db,
        'User': User
    }

@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main(['tests', '--verbose'])
    return exit_code

#Modifications to the migrate command
@MigrateCommand.command
def drop():
    """Drops all database tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        db.engine.execute("drop table alembic_version")

@MigrateCommand.command
def create():
    """Creates database tables from sqlalchemy models"""
    upgrade()
    populate()

@MigrateCommand.command
def recreate():
    """Recreates database tables (same as issuing 'drop' and then 'create')"""
    drop()
    create()


@MigrateCommand.command
def populate():
    "Populate database with default data"
    from tests.fixtures import setup, mixer
    mixer.init_app(application.mounts['/api'])
    setup()

manager.add_command('runserver', WSGI(host='0.0.0.0'))
manager.add_command('worker', Worker())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
