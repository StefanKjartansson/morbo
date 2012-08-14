from __future__ import absolute_import

import functools

from fabric.api import env, sudo, run, put, require

from .utils import remote_stream, config_file

from . import apt


def postgres(cmd):
    """
    Run a command as the postgres user
    """
    sudo(cmd, user='postgres')


def psql(db, cmd):
    postgres('psql -U postgres -d %s %s' % (db, cmd))


def db_exists():
    require('db_name')
    try:
        env.db_exists = env.db_name in (i.split('|')[0] for i in
            postgres('psql -l --tuples-only --no-align').splitlines())
    except:
        env.db_exists = False


def dropdb(db):
    postgres('dropdb %s' % db)


def drop():
    require('db_name')
    dropdb(env.db_name)


def install():
    db_exists()
    if env.db_exists:
        return
    dependencies = [
        'build-essential',
        'postgresql',
        'libpq-dev',
    ]
    apt.install(*dependencies)
    env.postgres_version = run('psql --version | python -c \'import sys; print ".".join((sys.stdin.read().split()[2]).split(".")[:2])\'')
    apt.install('postgresql-contrib-%s' % env.postgres_version)
    put(config_file('pg_hba.conf'), 'pg_hba.conf')
    sudo('mv pg_hba.conf /etc/postgresql/%s/main/pg_hba.conf' % env.postgres_version)
    sudo('service postgresql restart')
    env.postgres_installed = True


def postgis():
    """
    Installs postgis and all dependencies.
    """
    if not hasattr(env, 'postgres_installed'):
        install()

    dependencies = [
        'libgdal1-dev',
        'gdal-bin',
        'libproj-dev ',
        'proj-bin',
        'libgeos-dev',
        'libgeoip-dev',
        'geoip-database',
        'postgis',
    ]
    postgis_package = 'postgresql-%s-postgis' % env.postgres_version
    dependencies.append(postgis_package)
    apt.install(*dependencies)

    #Get the postgis major version
    postgis_version = '.'.join(apt.get_version(postgis_package).split('.')[:2])
    try:
        dropdb('template_postgis')
    except:
        pass
    postgres('createdb -E UTF8 -U postgres template_postgis')

    tp = functools.partial(psql, 'template_postgis')
    tp('-c"CREATE EXTENSION hstore;"')
    tp('-f /usr/share/postgresql/%s/contrib/postgis-%s/postgis.sql' % (
        env.postgres_version, postgis_version))
    tp('-f /usr/share/postgresql/%s/contrib/postgis-%s/spatial_ref_sys.sql' % (
        env.postgres_version, postgis_version))
    tp('-c"select postgis_lib_version();"')
    tp('-c "GRANT ALL ON geometry_columns TO PUBLIC;"')
    tp('-c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"')
    tp('-c "GRANT ALL ON geography_columns TO PUBLIC;"')


def configure():
    """
    """
    require('db_user')
    require('db_password')
    require('db_name')

    db_exists()
    if env.db_exists:
        return
    try:
        postgres('createuser %(db_user)s -s -d -r' % env)
    except:
        pass
    with remote_stream('/tmp/db') as f:
        f.write(open(config_file('db'), 'r').read() % env)
    postgres('psql -f /tmp/db')
    sudo('rm /tmp/db')
