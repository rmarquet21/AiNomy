import os
import unittest

from plumbum import local, FG

from server.host_context import HostContext
from tests.fixtures import clone_fixture, wait_database_ready

SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
DATASTORE_DIR = os.path.join(SCRIPT_DIR, '..', '..')


class TestAlembicMigrations(unittest.TestCase):

    def setUp(self):
        self.host_context = HostContext()

    def test_all_migrations_can_be_rollout_from_zero_to_hero(self):
        # Assign
        with clone_fixture('empty_database', remove_docker=True):
            # Acts
            wait_database_ready(self.host_context.datastore_connection_string())

            alembic = local['alembic']
            os.chdir(DATASTORE_DIR)
            alembic['upgrade', 'head'] & FG
