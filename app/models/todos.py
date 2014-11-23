# -*- coding: utf-8 -*-
"""
    vitals.models.todos
    ~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.
"""
from ..framework.sql import (
    db,
    Model,
    ReferenceColumn,
)


class Todo(Model):

    __tablename__ = "todos"

    title = db.Column(db.String(128), nullable=False)
    completed = db.Column(db.Boolean, default=False)

