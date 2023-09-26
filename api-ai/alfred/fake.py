import os
import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, '..', '..'))
LOCAL_PATH = os.path.realpath(os.path.join(ROOT_DIR, 'environments', 'fake'))


@alfred.command('fake', help='Run fake environment')
def hello_world():
    honcho = alfred.sh('honcho', 'honcho is not installed in python environment')
    os.chdir(LOCAL_PATH)

    alfred.run(honcho, ['start'])
