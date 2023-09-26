import os
import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, '..', '..'))
LOCAL_PATH = os.path.realpath(os.path.join(ROOT_DIR, 'environments', 'local'))


@alfred.command('local', help='Run local environment')
@alfred.option('--datalayer-only', default=False, is_flag=True, help='start only the elements of datalayer')
@alfred.option('--server-only', default=False, is_flag=True, help='start only the elements of server')
@alfred.option('--no-upgrade', default=False, is_flag=True, help="do not run upgrade")
@alfred.option('--migration-only', default=False, is_flag=True, help="run only migration")
@alfred.option('--down', default=False, is_flag=True, help='ensure docker containers are fully rebuild before starting')
def hello_world(datalayer_only, server_only, no_upgrade, migration_only, down):
    honcho = alfred.sh('honcho', 'honcho is not installed in python environment')

    os.chdir(LOCAL_PATH)

    if down:
        docker_compose = alfred.sh('docker-compose',
                                   'docker-compose is missing on your system : https://docs.docker.com/compose/install/')
        alfred.run(docker_compose, ['down'])

    # initialize database
    if not no_upgrade:
        alfred.run(honcho, ['-f', 'Procfile.initdb', 'start'], exit_on_error=False)

    if migration_only:
        alfred.run(honcho, ['-f', 'Procfile.migrate', 'start'], exit_on_error=False)

    if datalayer_only:
        alfred.run(honcho, ['-f', 'Procfile.datalayer', 'start'])
    elif server_only:
        alfred.run(honcho, ['-f', 'Procfile.serverlayer', 'start'])
    else:
        alfred.run(honcho, ['start'])
