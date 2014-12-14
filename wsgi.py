# -*- coding: utf-8 -*-

__author__ = 'DavidWCaraway'
from app.settings import ProductionConfig

from app import create_app

application = create_app(ProductionConfig)