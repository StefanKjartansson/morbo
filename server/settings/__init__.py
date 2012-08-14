#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import pkgutil


for _, module_name, _ in pkgutil.walk_packages(__path__):
    module = __import__(module_name, globals(), locals(), [])

    locals().update((var, val) for (var, val)
        in inspect.getmembers(module) if var.isupper())
