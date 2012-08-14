from __future__ import absolute_import

from fabric.api import env, sudo, require, cd
from fabric.contrib.files import exists

from .utils import remote_stream, config_file

from . import apt


def install():
    apt.install('nginx')


def configure():
    require('config_path')
    require('domain')
    require('project_name')
    require('project_root')
    require('upstream_port')

    t = 'nginx.conf'
    if env.server_type == 'gunicorn':
        t = 'nginx.gunicorn.conf'

    with remote_stream('%s.conf' % env.project_name) as f:
        f.write(open(config_file(t), 'r').read() % env)

    sudo('mv %s.conf /etc/nginx/sites-available/%s' % (env.project_name,
        env.project_name))

    with cd('/etc/nginx/sites-enabled'):
        if not exists(env.project_name, use_sudo=True):
            sudo('ln -s ../sites-available/%s .' % env.project_name)

    sudo('service nginx status || service nginx start')
    sudo('service nginx reload')
