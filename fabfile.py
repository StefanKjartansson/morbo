#!/usr/bin/env python
import os

from fabric.api import *
import fabric.colors as c

from deployment import (
    apt,
    django,
    git,
    nginx,
    postgres,
    utils,
)

_, name = os.path.split(os.path.dirname(__file__))

env.forward_agent = True
env.project_name = name
env.environment = 'DJANGO_SETTINGS_MODULE="server.settings"'

env.specific_packages = (
    'libxml2-dev',
    'libxslt1-dev',
)

app = __import__('server.settings')

db = app.settings.DATABASES['default']
env.db_user = db['USER']
env.db_name = db['NAME']
env.db_password = db['PASSWORD']
env.app_settings = app.settings


def set_local_paths():
    env.home = '/home/%s' % env.user
    env.webapps_root = '%s/apps/' % env.home
    env.ports_path = os.path.join(env.home, 'ports')
    env.log_path = os.path.join(env.home, 'logs/%s' % env.project_name)
    env.project_root = os.path.join(env.webapps_root, env.project_name)
    env.venv_bin = os.path.join(env.project_root, 'env/bin')
    env.activate_script = os.path.join(env.venv_bin, 'activate')
    env.repo_root = os.path.join(env.project_root)
    env.requirements_file = os.path.join(env.repo_root, 'requirements.txt')
    env.manage_dir = env.repo_root


@task
def vagrant():
    env.user = 'vagrant'
    env.host_string = '127.0.0.1:2222'
    env.hosts = ['127.0.0.1:2222']
    env.base_dir = '/home/vagrant'
    # retrieve the IdentityFile:
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]  # parse IdentityFile
    set_local_paths()


@task
def refresh_database():
    postgres.drop()
    postgres.configure()


@task
def dropdb():
    postgres.drop()


@task
def createsuperuser():
    django.manage_py('createsuperuser')


@task
def bootstrap():
    print(c.yellow('clean & update apt'))
    print(c.yellow('creating folders'))
    run('test -d %(webapps_root)s || mkdir %(webapps_root)s' % env)
    run('test -d %(log_path)s || mkdir -p %(log_path)s' % env)
    run('test -d %(ports_path)s || mkdir -p %(ports_path)s' % env)
    print(c.yellow('bootstrap python'))
    utils.python_bootstrap()
    print(c.yellow('installing git'))
    git.install()
    print(c.yellow('installing postgres'))
    postgres.install()

    if 'djcelery' in app.settings.INSTALLED_APPS and \
            ('localhost' in getattr(app.settings, 'BROKER_URL', '')):
        apt.install('redis-server')

    print(c.yellow('installing extra packages'))
    apt.install('supervisor')
    apt.install(*env.specific_packages)

    print(c.yellow('installing nginx'))
    nginx.install()
    print(c.green('bootstrap complete'))
    postgres.configure()
    print(c.green('installing requirements'))
    django.install_requirements()

    if 'south' in app.settings.INSTALLED_APPS:
        django.migrate()

    print(c.yellow('compressing static files'))
    try:
        django.collectstatic()
    except:
        print(c.red('Collect static failed'))
    if getattr(app.settings, 'COMPRESS_OFFLINE', False):
        try:
            django.compress()
        except:
            print(c.red('Static compression failed'))
