import boto3
from fabric.api import env, sudo, run, task
from fabric.colors import green


@task
def status():
    print(green('AWS Agent status for {host}'.format(**env)))
    sudo('/opt/aws/awsagent/bin/awsagent status')


@task
def install():
    print(green('Downloading AWS Agent installation script'))
    run('curl -O https://d1wk0tztpsntt1.cloudfront.net/linux/latest/install')

    print(green('Installing AWS Agent'))
    run('sudo bash install')


@task
def validate_install():
    pass


@task
def start():
    print(green('Starting AWS Agent'))
    sudo('/etc/init.d/awsagent start')


@task
def stop():
    print(green('Stopping AWS Agent'))
    sudo('/etc/init.d/awsagent stop')


@task
def get_cluster_instances(cluster=None):
    if cluster is None:
        print('No cluster specified')
        return
    client = boto3.client('ecs')
    response = client.list_container_instances(cluster=cluster)
    print(response)
