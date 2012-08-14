#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import

import os


SETTINGS_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT, _ = os.path.split(SETTINGS_ROOT)
PROJECT_BASE, _ = os.path.split(PROJECT_ROOT)


project_path = lambda *x: os.path.join(PROJECT_ROOT, *x)
root_path = lambda *x: os.path.join(PROJECT_BASE, *x)
