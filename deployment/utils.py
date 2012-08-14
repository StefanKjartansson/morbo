from __future__ import absolute_import

import os

import StringIO
from contextlib import contextmanager

from fabric.api import put, sudo, env, require, run, cd
from fabric.contrib.files import exists

from . import apt


def inspect_distro():
    d = dict((k.lower(), v) for (k, v) in ((i.strip().split('=') for i in
        run('cat /etc/lsb-release').splitlines())))
    env.version_tuple = tuple(map(int, d['distrib_release'].split('.')))
    env.distro = d


def inspect_and_upgrade():
    inspect_distro()
    if env.version_tuple < (12, 04):
        apt.upgrade()


@contextmanager
def remote_stream(name):
    f = StringIO.StringIO()
    yield f
    f.seek(0)
    put(f, name)
    f.close()


def config_file(name):
    require('config_path')
    return os.path.join(env.config_path, name)


def virtualenv(command, use_sudo=False):
    if not exists(os.path.join(env.project_root, 'env')):
        with cd(env.project_root):
            run('virtualenv --no-site-packages env')
    (sudo if use_sudo else run)('source "%s" && %s' % (env.activate_script, command))


def easy_install(*packages):
    sudo('easy_install %s' % ' '.join(packages))


def python_bootstrap():
    apt.install('python-setuptools python-dev build-essential')
    easy_install('virtualenv', 'pip', 'elementtree')
