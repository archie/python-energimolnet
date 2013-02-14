# -*- coding: utf-8 -*-

import urllib
import urllib2
import json


class Energimolnet:
    version = '1.0'
    base_url = 'https://app.energimolnet.se/api/'

    def __init__(self, username, password, company):
        self.auth = {
            'Username': username,
            'Password': password,
            'Company': company
        }

    def customer(self):
        _, content = self.get('/customer')
        return content

    def unit(self, unit_id):
        _, content = self.get('/unit/unit_id/%s' % unit_id)
        return content

    def data(self, unit_id, metrics=None, intervals=None, resolution=None):
        metrics = metrics or ['price', 'energy', 'cost']
        metrics = ",".join(metrics) if type(metrics) is list else metrics

        resolution = resolution or 'hour'  # default is hour
        intervals = intervals or self._get_unit_metric_boundary(unit_id, resolution)

        json_intervals = json.dumps([{
                "from": intervals[0],
                "to": intervals[1],
                "resolution": resolution
            }])

        _, content = self.get('/data/unit_id/%s/metrics/%s/intervals/%s' \
            % (unit_id, metrics, json_intervals))

        return content

    def nordpoolspot(self, unit_id, intervals):
        formatted_intervals = [{"from": value[0], "to": value[1]} for
            value in intervals]
        json_intervals = json.dumps(formatted_intervals)
        _, content = self.get('/nordpoolspot/unit_id/%s/intervals/%s' \
            % (unit_id, json_intervals))
        return content

    def get(self, method, headers={}):
        def makeurl(method):
            return self.base_url + self.version + method

        headers.update(self.auth)
        headers.update({
                'Accept': 'application/json',
                'Content-type': 'application/json; charset=utf-8',
                'User-agent': 'Energimolnet Python Wrapper %s' % self.version,
                'Connection': 'keep-alive'
            })

        urlencoded_method = urllib.pathname2url(method)
        opener = urllib2.build_opener()
        request = urllib2.Request(makeurl(urlencoded_method), headers=headers)
        response = opener.open(request)

        return response.headers, json.loads(response.read())

    def _get_unit_metric_boundary(self, unit_id, resolution):
        unit = self.unit(unit_id)
        min = unit['data']['boundaries'][resolution]['from']
        max = unit['data']['boundaries'][resolution]['to']
        return min, max
