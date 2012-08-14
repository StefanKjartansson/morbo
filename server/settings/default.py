#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import

from .paths import root_path


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Atlantic/Reykjavik'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = root_path('media')
MEDIA_URL = '/media/'

SECRET_KEY = '*2k)y)y&amp;ra)_sq%)7+9tz20jxy3jekgj)^1!bk)+imt&amp;^)=^zq'

ROOT_URLCONF = 'server.urls'
WSGI_APPLICATION = 'server.wsgi.application'
