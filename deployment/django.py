import os

from fabric.api import env, require, cd, sudo, run
from fabric.contrib.files import exists

from .utils import (virtualenv, remote_stream, config_file)


def install_requirements():
    require('hosts')
    virtualenv('pip install -r %(requirements_file)s' % env)


def manage_py(command, use_sudo=False):
    require('hosts')
    with cd(env.manage_dir):
        virtualenv('python manage.py %s' % command, use_sudo)


def syncdb(app=None):
    require('hosts')
    manage_py('syncdb --noinput')


def migrate():
    require('hosts')
    manage_py('migrate --all --fake')


def compress():
    require('hosts')
    manage_py('compress')


def collectstatic():
    require('hosts')
    manage_py('collectstatic -l --noinput')


def supervisor_service(name):
    require('hosts')

    dname = '%s.%s.conf' % (env.project_name, name)

    with remote_stream(dname) as f:
        f.write(open(config_file(name), 'r').read() % env)

    sudo('mv %s /etc/supervisor/conf.d/' % dname)
    status = sudo('supervisorctl status').strip()
    if status:
        sudo('supervisorctl restart %s_%s' % (
            env.project_name, name))
    else:
        sudo('supervisorctl reload')


def configure_celery():
    supervisor_service('celery')


def configure_uwsgi():
    require('hosts')
    require('upstream_port')
    if not exists(os.path.join(env.venv_bin, 'uwsgi')):
        virtualenv('pip install uwsgi')
    supervisor_service('uwsgi')


def configure_gunicorn():
    require('hosts')
    require('upstream_port')

    env.worker_class = 'sync'
    with cd(env.repo_root):
        r = run('cat %(requirements_file)s' % env)
        for i in ['eventlet', 'gevent', 'tornado']:
            if i in r:
                env.worker_class = i
    supervisor_service('gunicorn')


def configure_server():

    env.num_cpus = int(sudo('cat /proc/cpuinfo | grep processor | wc -l')[-1].strip())
    env.num_workers = (env.num_cpus * 4)

    if 'gunicorn' in env.app_settings.INSTALLED_APPS:
        env.server_type = 'gunicorn'
        configure_gunicorn()
    else:
        env.server_type = 'uwsgi'
        configure_uwsgi()
