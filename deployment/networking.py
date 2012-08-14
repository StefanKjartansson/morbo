import os

from fabric.api import require, sudo, env, cd, run
from fabric.contrib.files import exists

from .utils import remote_stream


def free_upstream_port():
    require('hosts')
    upstream_port = 3031
    portfile = '%s.port' % env.project_name
    if exists(os.path.join(env.ports_path, portfile)):
        with cd(env.ports_path):
            env.upstream_port = int(run('cat %s' %
                portfile).splitlines()[0].strip())
    else:
        ns = sudo('netstat -atnp|grep LISTEN')
        ports = [int(i.split()[3].split(':')[-1])
            for i in ns.splitlines()]
        while upstream_port in ports:
            upstream_port += 1
        env.upstream_port = upstream_port
        with remote_stream(os.path.join(env.ports_path, portfile)) as f:
            f.write(env.upstream_port)
