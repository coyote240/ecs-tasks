import json
from fabric.api import run, env, task
from fabric.context_managers import settings, hide


env.use_ssh_config = True


@task
def query():
    '''Query all hosts for NPM installed package versions
    '''

    containers = get_containers()
    for id, image in containers.iteritems():
        packages = get_packages(id)
        try:
            service = json.loads(packages)
        except ValueError:
            msg = 'No packages listed or npm not installed on image: {0}.'
            print(msg.format(image))
        else:
            name = service.get('name')
            version = service.get('version', 'unknown')
            deps = service.get('dependencies')

            write_file(name, version, deps)


def get_containers():
    '''Get running containers on host.
    '''

    with hide('stdout', 'running'):
        results = run('docker ps --format "{{.ID}} {{.Image}}"')

    rows = {id: image for id, image in
            [result.split(' ') for result in results.split('\r\n')]}

    return rows


@task
def list_containers():
    '''List running containers and images on host.
    '''

    containers = get_containers()
    for id, image in containers.iteritems():
        print('{0}\t{1}'.format(id, image))


def get_packages(id):
    '''Get Installed NPM Packages
    '''

    with settings(
            hide('stdout', 'running'),
            warn_only=True):
        packages = run(
                'docker exec {0} npm ls --depth=0 --json=true'.format(id))

    return packages


@task
def list_packages(id):
    '''List installed NPM packages.
    '''

    packages = get_packages(id)
    try:
        service = json.loads(packages)
    except ValueError:
        msg = 'No packages listed or npm not installed on container: {0}.'
        print(msg.format(id))
    else:
        deps = service.get('dependencies')
        for name, details in sorted(deps.iteritems(), key=lambda dep: dep[0]):
            version = details.get('version', 'unknown')
            line = '{0}@{1}'.format(name, version)
            print(line)


def write_file(name, version, deps):
    '''Write file
    For each service, write it's dependencies to file as <name>@<version>.
    '''

    file_name = '{0}-{1}.txt'.format(name, version)
    print('Writing version info to {0}'.format(file_name))

    with open(file_name, 'w') as fh:
        for name, details in sorted(deps.iteritems(), key=lambda dep: dep[0]):
            version = details.get('version', 'unknown')
            line = '{0}@{1}\n'.format(name, version)
            fh.write(line)
