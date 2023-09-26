import unittest
from io import BytesIO
from unittest.mock import Mock

from server.app import injector
from server.app.web.webapp import create_app
from server.host_context import HostContext


class TestPrediction(unittest.TestCase):
    def setUp(self):
        host_context = HostContext()
        host_context.fake_data = Mock(return_value=True)
        with injector.configure_global_injector(host_context):
            self.client = create_app().test_client()

    def test_get_pneumonia_prediction(self):
        # Assign
        data = dict(img=(BytesIO(b'my image'), "img.png"))
        # Act
        response = self.client.post('/api/predict/pneumonia', content_type='multipart/form-data', data=data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'prediction': 'pneumonia'})
