import os
import shutil

import io
import signal
import tempfile
import time
from asyncio import Future

import psycopg2
from decorator import contextmanager
from jsonschema import validate
from plumbum import local, BG, FG
from retrying import retry
import vcr

SCRIPT_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))


@contextmanager
def clone_fixture(fixture_name, working_dir=None, debug_fixture=False, remove_docker=False):
    working_directory, docker_compose_up_pid = clone_fixture_up(fixture_name, working_dir, debug_fixture=debug_fixture)
    try:
        yield working_directory
    finally:
        clone_fixture_down(working_directory, remove_docker)
        if docker_compose_up_pid:
            docker_compose_up_pid.wait()


def clone_fixture_up(fixture_name, tmp_directory=None, debug_fixture=False):
    docker_compose_up_pid = None
    tmp_prefix = '{0}_{1}'.format(fixture_name, '_')
    working_directory = tempfile.mktemp(prefix=tmp_prefix) if not tmp_directory else tmp_directory
    template_working_directory = os.path.join(SCRIPT_DIRECTORY_PATH, fixture_name)

    if not os.path.isdir(template_working_directory):
        fixtures_list = [d for d in os.listdir(SCRIPT_DIRECTORY_PATH) if
                         os.path.isdir(os.path.join(SCRIPT_DIRECTORY_PATH, d))]
        raise Exception('the fixture {0} does not exists in fixtures : {1}'.format(fixture_name, fixtures_list))
    shutil.copytree(template_working_directory, working_directory)

    docker_compose_path = os.path.join(working_directory, 'docker-compose.yml')
    if os.path.isfile(docker_compose_path):
        docker_compose_tool = local['docker-compose']
        if not debug_fixture:
            docker_compose_up_pid = docker_compose_tool.bound_command('--file', docker_compose_path, 'up') & BG
        else:
            docker_compose_tool.bound_command('--file', docker_compose_path, 'up') & FG

    return working_directory, docker_compose_up_pid


def clone_fixture_down(working_directory, remove_docker=False):
    docker_compose_path = os.path.join(working_directory, 'docker-compose.yml')
    if os.path.isfile(docker_compose_path):
        docker_compose_tool = local['docker-compose']
        docker_compose_tool.bound_command('--file', docker_compose_path, 'down')()  # type: Future
        if remove_docker:
            docker_compose_tool.bound_command('--file', docker_compose_path, 'rm')()

    shutil.rmtree(working_directory)


@retry(wait_fixed=6000, stop_max_attempt_number=10)
def wait_database_ready(connection_string: str) -> None:
    database = 'ainomy'

    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 AS result FROM pg_database WHERE datname='{database}'")


def validate_examples_in_json_schema(schema: dict):
    for example in schema["examples"]:
        validate(example, schema=schema)


@contextmanager
def record_cassette(api: str, cassette_path: str, port=9000):
    cornell = local['cornell']
    log = os.path.join(cassette_path, 'cassette.log')
    if os.path.isfile(log):
        os.remove(log)

    with io.open(log, 'a') as fp:
        run = (cornell['-ff', api, '--record', '-fp', '-cd', cassette_path, '-p', port] & BG(stdout=fp, stderr=fp))
        try:
            time.sleep(2)
            yield f'http://localhost:{port}'

        finally:
            run.proc.send_signal(signal.SIGINT)


@contextmanager
def use_cassette(path: str):
    with vcr.use_cassette(path, serializer='yaml', record_mode='none', decode_compressed_response=True) as cassette:
        yield cassette
