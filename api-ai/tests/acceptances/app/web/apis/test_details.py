import unittest
from unittest.mock import Mock

from server.app import injector
from server.app.web.webapp import create_app
from server.host_context import HostContext


class TestDetails(unittest.TestCase):
    def setUp(self):
        host_context = HostContext()
        host_context.fake_data = Mock(return_value=True)
        with injector.configure_global_injector(host_context):
            self.client = create_app().test_client()

    def test_get_details(self):
        # Assign

        # Act
        response = self.client.get('/api/details/Viral%20pneumonia')

        # Assert
        disease = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(disease['name'], 'Viral pneumonia')

    def test_get_details_not_found(self):
        # Assign

        # Act
        response = self.client.get('/api/details/Not%20found')

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Disease not found'})
