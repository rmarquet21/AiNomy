import os

import alfred

PRODUCT_PATH = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command('lint', help="validate ainomy with pylint")
def lint():
    poetry = alfred.sh('poetry', "poetry is not installed")
    os.chdir(os.path.join(PRODUCT_PATH, "server"))
    ainomy = 'server'
    path = ['run', 'pylint', '--fail-under=9', ainomy]

    if path:
        alfred.run(poetry, path)
