from __future__ import absolute_import

from fabric.api import sudo
from fabric.contrib.files import exists

from . import apt


def add_repo():
    #adds rabbitmq to sources.list
    mq = '/etc/apt/sources.list.d/rabbitmq.list'
    if not exists(mq, use_sudo=True):
        sudo('echo "deb http://www.rabbitmq.com/debian/ testing main" >> %s' % mq)
        sudo('wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc')
        sudo('apt-key add rabbitmq-signing-key-public.asc')
        sudo('rm rabbitmq-signing-key-public*')


def install():
    add_repo()
    apt.clean()
    apt.install('rabbitmq-server')
