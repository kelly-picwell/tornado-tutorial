import json
import uuid

from tornado.testing import AsyncHTTPTestCase
from tornado import ioloop

from tornado_tutorial import make_app


class TestHousehold(AsyncHTTPTestCase):

    def get_app(self):
        return make_app()

    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()

    def test_create_household(self):
        payload = {
            "external_id": "1234567",
            "income": 50000,
            "zip_code_3": 123,
            "client_name": "this_client",
        }
        headers = {'content-type': "application/json"}

        response = self.fetch('/household/',
                              method="POST",
                              body=json.dumps(payload),
                              headers=headers)
        response_body = json.loads(response.body)

        self.assertEqual(response.code, 200)
        uuid.UUID(response_body['data'])
