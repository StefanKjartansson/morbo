from fabric.api import sudo


def get_version(package):
    """
    Returns the installed package version
    """
    for i in (i.strip() for i in sudo('apt-cache policy %s' % package).splitlines()):
        if i.startswith('Installed'):
            v = i.split(':')[1].strip()
            if v == '(none)':
                return None
            return v
    return None


def refresh():
    """
    Cleans up dirty apt cache
    """
    sudo('rm -f /var/cache/apt/*.bin')
    sudo('apt-get update && apt-get clean')


def install(*packages):
    """
    installs packages
    """
    if packages:
        sudo('apt-get -y install %s' % ' '.join(packages))


def upgrade():
    sudo('do-release-upgrade')


def clean():
    sudo('apt-get clean && apt-get update')


def add_ppa(ppa):
    sudo('add-apt-repository ppa:%s' % ppa)
    clean()
