#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import

from django.conf.urls.defaults import url, patterns

from .views import TestView


urlpatterns = patterns('',
    url(r'^$', TestView.as_view(), name='index'),
)
