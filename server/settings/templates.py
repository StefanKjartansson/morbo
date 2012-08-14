#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import

from .paths import project_path
from .env import DEBUG


TEMPLATE_DEBUG = DEBUG


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


TEMPLATE_DIRS = (
    project_path('templates'),
)
