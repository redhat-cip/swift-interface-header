# Copyright (C) 2013 eNovance SAS <licensing@enovance.com>
#
# Author: Mehdi Abaakouk <mehdi.abaakouk@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from swift.common.utils import get_logger


class InterfaceHeader(object):
    """Swift middleware than set the header HTTP_X_INTERFACE to
    a value defined in rule configuration

    Configuration:
    In /etc/swift/proxy-server.conf on the main pipeline add "interface_header"

    [filter:interface_header]
    paste.filter_factory = egg:interface_header#interface_header

    # Some optionnal configuration to fill the header "HTTP_X_INTERFACE" in
    # fonction of data in the request environment
    interface_default = int
    interface_rule_1 = HTTP_HOST, 123.123.123.123:8080, ext
    interface_rule_2 = SERVER_PORT, 8081, ext
    interface_rule_3 = SERVER_NAME, 192.168.3.51, ext
    """
    def __init__(self, app, conf):
        self.app = app
        self.logger = get_logger(conf, log_route='ceilometer')

        self.interface_default = conf.get('interface_default')
        self.interface_rules = []
        for k, v in conf.iteritems():
            if k.startswith('interface_rule_'):
                try:
                    header, value, interface = v.split(',')
                except ValueError:
                    self.logger.error(_("Failed to parse rule %s = %s"), k, v)
                    continue
                self.interface_rules.append((header.upper().strip(),
                                             value.upper().strip(),
                                             interface.strip()))

    def __call__(self, env, start_response):
        """
        Main hook into the WSGI paste.deploy filter/app pipeline.

        :param env: The WSGI environment dict.
        :param start_response: The WSGI start_response hook.
        :returns: Response as per WSGI.
        """

        cur_interface = self.interface_default
        for header, value, interface in self.interface_rules:
            if header in env and env[header].upper() == value:
                cur_interface = interface
        env["HTTP_X_INTERFACE"] = cur_interface

        return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """ Returns the WSGI filter for use with paste.deploy. """
    conf = global_conf.copy()
    conf.update(local_conf)
    return lambda app: InterfaceHeader(app, conf)
