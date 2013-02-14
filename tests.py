# -*- coding: utf-8 -*-

from urllib2 import HTTPError
import os
import molnet
import unittest


TEST_UNIT_ID = u'507403893145a7556a000000'


class TestEnergimolnet(unittest.TestCase):
    def setUp(self):
        [user, password, company] = os.environ.get('ENERGIMOLNET').split(',')
        self.api = molnet.Energimolnet(user, password, company)

    def test_customer(self):
        customer_unit_0_id = self.api.customer()['units'][0]['_id']
        assert customer_unit_0_id == TEST_UNIT_ID

    def test_incorrect_user(self):
        self.api = molnet.Energimolnet('monkey', 'see', 'monkey_do')
        with self.assertRaises(HTTPError) as context_manager:
            self.api.customer()

        assert context_manager.exception.code == 401

    def test_unit(self):
        customer = self.api.customer()
        unit_1 = customer['units'][0]
        queried_unit = self.api.unit(TEST_UNIT_ID)
        assert queried_unit['ean'] == unit_1['ean']

    def test_get_energy_metrics(self):
        unit_energy = self.api.data(TEST_UNIT_ID, metrics=['energy'])
        [metric] = [metric for metric in unit_energy if 'energy' in metric]
        assert len(metric['energy']) > 0


if __name__ == '__main__':
    unittest.main()
