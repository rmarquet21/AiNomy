import os

from urllib.parse import urlparse
from plumbum import ProcessExecutionError
from retrying import retry

import click
import psycopg2
import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))
DATASTORE_ALEMBIC_PATH = os.path.realpath(os.path.join(ROOT_DIR))
DATASTORE_LOCAL_PATH = os.path.realpath(os.path.join(ROOT_DIR, "environments", "local"))
DATASTORE_URL = os.getenv('AINOMY_DATABASE_URL', 'postgresql://ainomy:ainomy@ai-postgres:5432/ainomy')


@alfred.command('datastore:init', help="create the initial database", hidden=True)
def init():
    query_string = _get_query_string(DATASTORE_URL)
    database = _get_database(DATASTORE_URL)
    try:
        _ensure_database_exists(database, query_string)

        click.echo(f"{database} database is ready")
    except Exception as exception:
        click.echo(exception)


@alfred.command('datastore:reset', help="wipe the content of local data (all tables and data)", hidden=True)
def reset():
    query_string = _get_query_string(DATASTORE_URL)
    database = _get_database(DATASTORE_URL)
    try:
        _ensure_database_removed(database, query_string)
        _ensure_database_exists(database, query_string)

        click.echo(f"{database} database has been reseted (all data have been wiped in local)")
    except Exception as exception:
        click.echo(exception)


@alfred.command('datastore:revision:autogenerate', help="create a new revision for the datastore with model change")
@alfred.option('--message', '-m', help='message string to use with revision')
def revision_autogenerate(message):
    honcho = alfred.sh('honcho', "honcho is not installed in python environment")

    os.chdir(DATASTORE_LOCAL_PATH)
    alfred.run(honcho, ['-f', 'Procfile.initdb', 'start'], exit_on_error=False)
    try:
        with honcho.bgrun(['-f', 'Procfile.datalayer', 'start']) as bg1:
            query_string = _get_query_string(DATASTORE_URL)
            database = _get_database(DATASTORE_URL)
            try:
                _ensure_database_exists(database, query_string)
                alembic = alfred.sh('alembic')
                os.chdir(DATASTORE_ALEMBIC_PATH)

                args = ['revision', '--autogenerate']
                if message is not None:
                    args.append("-m")
                    args.append(message)

                alfred.run(alembic, args)
                bg1.terminate()
            except Exception as exception:
                click.echo(exception)
    except ProcessExecutionError:
        # normal flow due to bg1.terminate
        pass


@alfred.command('datastore:revision', help="create a new revision for the datastore")
@alfred.option('--message', '-m', help='message string to use with revision')
def revision(message):
    args = ['revision']

    if message is not None:
        args.append("-m")
        args.append(message)

    alembic = alfred.sh('alembic')
    os.chdir(DATASTORE_ALEMBIC_PATH)
    alfred.run(alembic, args)


@alfred.command('datastore:revision:history', help="list the history of the datastore")
def history():
    args = ['history']

    alembic = alfred.sh('alembic')
    os.chdir(DATASTORE_ALEMBIC_PATH)
    alfred.run(alembic, args)


@alfred.command('datastore:upgrade',
                help="upgrade operations, proceeding from the current database revision to the given target revision")
@alfred.option('--revision', default="head")
def upgrade(revision: str = "head"):
    alembic = alfred.sh('alembic')
    args = ['upgrade', revision]
    os.chdir(DATASTORE_ALEMBIC_PATH)
    alfred.run(alembic, args)


@retry(wait_fixed=5000, stop_max_attempt_number=10)
def _ensure_database_exists(database, query_string):
    conn = psycopg2.connect(query_string)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 AS result FROM pg_database WHERE datname='{database}'")
    if cursor.rowcount == 0:
        cursor.execute(f"CREATE DATABASE {database}")


@retry(wait_fixed=5000, stop_max_attempt_number=10)
def _ensure_database_removed(database, query_string):
    conn = psycopg2.connect(query_string)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 AS result FROM pg_database WHERE datname='{database}'")
    if cursor.rowcount == 1:
        cursor.execute(f"DROP DATABASE {database}")


def _get_query_string(datastore_url: str):
    o = urlparse(datastore_url)
    user = o.username
    password = o.password
    hostname = o.hostname
    port = o.port
    query_string = f"dbname='postgres' user='{user}' host='{hostname}' port='{port}' password='{password}'"
    return query_string


def _get_database(datastore_url: str):
    o = urlparse(datastore_url)
    database = o.path[1:]
    return database
