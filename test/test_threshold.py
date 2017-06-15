import json
import os
import uuid

from tornado import ioloop
from tornado.testing import AsyncHTTPTestCase
import psycopg2

from tornado_tutorial import make_app

HEADERS = {'content-type': "application/json"}


def get_threshold_body(**kwargs):
    threshold = {
        "external_id": "ah18-gold-hmsa",
        "family": False,
        "network": "Combined",
        'drug_moop': 3000,
        'medical_moop': 2000,
        'medical_drug_moop': None,
        'moop_embedded': True,
        'drug_deductible': 0,
        'medical_deductible': 100,
        'medical_drug_deductible': None,
        'deductible_embedded': True,
    }
    threshold.update(kwargs)
    return threshold


class TestThreshold(AsyncHTTPTestCase):

    DBNAME = 'tutorial'

    def get_app(self):
        return make_app()

    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()

    def create_new_threshold(self, body):
        return self.fetch('/threshold/',
                          method='POST',
                          body=json.dumps(body),
                          headers=HEADERS)

    def update_threshold(self, body, threshold_id):
        url = '/threshold/{threshold_id}/'.format(threshold_id=threshold_id)
        return self.fetch(url,
                          method='PUT',
                          body=json.dumps(body),
                          headers=HEADERS)

    def get_threshold(self, threshold_id):
        url = '/threshold/{threshold_id}/'.format(threshold_id=threshold_id)
        return self.fetch(url)

    def get_all_thresholds(self):
        return self.fetch('/threshold/')

    def test_create_threshold(self):
        payload = get_threshold_body()
        response = self.create_new_threshold(payload)
        response_body = json.loads(response.body)

        self.assertEqual(response.code, 200)
        uuid.UUID(response_body['data'])

    def test_get_threshold(self):
        payload = get_threshold_body()

        # create threshold
        response = self.create_new_threshold(payload)
        response_body = json.loads(response.body)
        threshold_id = response_body['data']
        payload['id'] = threshold_id

        # fetch threshold
        response = self.get_threshold(threshold_id)
        threshold = json.loads(response.body)

        self.assertDictEqual(payload, threshold)

    def test_get_all_thresholds(self):
        # delete all thresholds
        with psycopg2.connect(os.environ.get('PGSQL_TUTORIAL')) as conn:
            with conn.cursor() as curs:
                curs.execute('DELETE FROM threshold')

        # create thresholds
        num_thresholds = 5
        payload = get_threshold_body()
        for _ in range(num_thresholds):
            response = self.create_new_threshold(payload)

        # get all thresholds
        response = self.get_all_thresholds()
        thresholds = json.loads(response.body)

        self.assertEqual(num_thresholds, len(thresholds))
        for threshold in thresholds:
            threshold.pop('id')
            self.assertDictEqual(payload, threshold)

    def test_update_threshold(self):
        # create new threshold
        new_threshold = get_threshold_body()
        response = self.create_new_threshold(new_threshold)
        response_body = json.loads(response.body)

        # updated existing threshold
        new_external_id = 'new_threshold'
        new_moop = new_threshold['drug_moop'] + 1000
        updated_payload = get_threshold_body(external_id=new_external_id,
                                             drug_moop=new_moop)
        response = self.update_threshold(updated_payload,
                                         response_body['data'])
        response_body = json.loads(response.body)

        self.assertEqual(response.code, 200)
        self.assertEqual(response_body['external_id'], new_external_id)
        self.assertEqual(response_body['drug_moop'], new_moop)
