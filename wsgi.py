# -*- coding: utf-8 -*-

__author__ = 'DavidWCaraway'
from app.settings import ProductionConfig, StagingConfig
import os

from app import create_app

config = ProductionConfig if os.environ.get('STAGING_PRODUCTION', 'production') == 'production' else StagingConfig

application = create_app(config)