#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
WSGI config for server project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import site


# This should be the repository root as well.
parent_dir = os.path.abspath(os.path.join(
    os.path.abspath(os.path.dirname(__file__)), os.pardir))

# Virtual Environment path.
VENV = os.environ.get('VIRTUAL_ENV',  os.path.join(parent_dir, 'env'))

# Directories we want to incorporate into sys.path and .pth directories (site)
DIRS = [
    VENV,
    parent_dir,
]

# Remember original sys.path.
prev_sys_path = list(sys.path)

# Add each new site-packages directory.
for directory in DIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)

sys.path[:0] = new_sys_path

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# Activate the virtual environment
activate_this = '%s/bin/activate_this.py' % VENV
execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
#Add middleware if we need it
application = get_wsgi_application()
