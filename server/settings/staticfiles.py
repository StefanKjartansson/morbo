#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import

from .paths import project_path, root_path


STATIC_ROOT = root_path('static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    project_path('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
