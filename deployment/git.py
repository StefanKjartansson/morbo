from __future__ import absolute_import

from fabric.api import env, require, run, cd


from . import apt


def install():
    if env.distro.get('DISTRIB_RELEASE') > '10.04':
        apt.install('git')
    else:
        apt.install('git-core')


def update():
    require('hosts')
    with cd(env.repo_root):
        run('git pull origin master')
