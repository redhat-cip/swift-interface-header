# Copyright 2013 eNovance.
# All Rights Reserved.
#
# Author: Mehdi Abaakouk <mehdi.abaakouk@enovance.com>
#
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import swift_interface_header.middleware as middleware

from swift.common.swob import Response, Request


class FakeApp(object):
    def __init__(self):
        self.status_headers_body = ('204 No Content', {}, '')

    def __call__(self, env, start_response):
        status, headers, body = self.status_headers_body
        return Response(status=status, headers=headers,
                        body=body)(env, start_response)


class TestCasestInterfaceSetter(unittest.TestCase):
    def setUp(self):
        self.conf = {
            'interface_default': 'int',
            'interface_rule_1': 'HTTP_HOST, 123.123.123.123:8080, ext',
            'interface_rule_2': 'SERVER_PORT, 8081, ext',
        }
        self.test_default = middleware.filter_factory(self.conf)(FakeApp())

    def test_default(self):
        req = Request.blank("/v1/AUTH_account/cont", environ={})
        resp = req.get_response(self.test_default)
        self.assertEqual(resp.environ['HTTP_X_INTERFACE'], 'int')

    def test_match_rule1(self):
        req = Request.blank("/v1/AUTH_account/cont", environ={
            'HTTP_HOST': '123.123.123.123:8080'
        })
        resp = req.get_response(self.test_default)
        self.assertEqual(resp.environ['HTTP_X_INTERFACE'], 'ext')

    def test_match_rule2(self):
        req = Request.blank("/v1/AUTH_account/cont", environ={
            'SERVER_PORT': '8081'
        })
        resp = req.get_response(self.test_default)
        self.assertEqual(resp.environ['HTTP_X_INTERFACE'], 'ext')
