# -*- coding: utf-8 -*-
"""
    vitals.framework
    ~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from .factory import create_app
from .utils import flash_errors, generate_salt
