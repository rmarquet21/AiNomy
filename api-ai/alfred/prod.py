import os
import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, '..', '..'))
LOCAL_PATH = os.path.realpath(os.path.join(ROOT_DIR, 'environments', 'prod'))


@alfred.command('prod', help='Run prod environment')
def prod():
    honcho = alfred.sh('honcho', 'honcho is not installed in python environment')

    os.chdir(LOCAL_PATH)

    alfred.run(honcho, ['-f', 'Procfile.initdb', 'start'], exit_on_error=False)

    alfred.run(honcho, ['-f', 'Procfile.initmodel', 'start'], exit_on_error=False)

    alfred.run(honcho, ['start'])
