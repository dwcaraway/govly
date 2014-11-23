# -*- coding: utf-8 -*-
"""
    frontend.views.legal
    ~~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""

from flask import render_template
from flask.ext.classy import FlaskView

class LegalView(FlaskView):

    def privacy(self):
        return render_template("legal/privacy.html")

    def terms_of_use(self):
        return render_template("legal/terms_of_use.html")
