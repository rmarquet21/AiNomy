import os

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command('tests:acceptances', help="validate ainomy with acceptances testing")
@alfred.option('-v', '--verbose', is_flag=True)
def tests_acceptances(verbose: bool):
    poetry = alfred.sh('poetry')
    os.chdir(ROOT_DIR)
    directory = 'tests/acceptances'
    args = ['run', 'python', '-m', 'unittest', 'discover', directory]

    if verbose:
        args.append('-v')
    if args:
        alfred.run(poetry, args)


@alfred.command('tests:units', help="validate ainomy with unit testing")
@alfred.option('-v', '--verbose', is_flag=True)
def tests_units(verbose: bool):
    poetry = alfred.sh('poetry')
    os.chdir(ROOT_DIR)
    directory = 'tests/units'
    args = ['run', 'python', '-m', 'unittest', 'discover', directory]

    if verbose:
        args.append('-v')
    if args:
        alfred.run(poetry, args)


@alfred.command('tests:migrations', help="validate datastore migration for ainomy")
@alfred.option('-v', '--verbose', is_flag=True)
def tests_migrations(verbose: bool):
    poetry = alfred.sh('poetry')
    os.chdir(ROOT_DIR)
    directory = 'tests/migrations'
    args = ['run', 'python', '-m', 'unittest', 'discover', directory]

    if verbose:
        args.append('-v')
    if args:
        alfred.run(poetry, args)
