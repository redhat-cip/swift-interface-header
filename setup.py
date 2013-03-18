# -*- encoding: utf-8 -*-
# Copyright 2013 eNovance.
# All Rights Reserved.
#
# Author: Mehdi Abaakouk <mehdi.abaakouk@enovance.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

name = 'swift_interface_header'
entry_point = '%s.middleware:filter_factory' % (name)
version = '0.1'

from setuptools import setup, find_packages

setup(
    name=name,
    version=version,
    description='Swift middleware to set header X-INTERFACE \
in fonction of request header.',
    license='Apache License (2.0)',
    author='OpenStack, LLC.',
    author_email='mehdi.abaakouk@enovance.com',
    url='https://github.com/enovance/%s' % (name),
    packages=find_packages(),
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Environment :: No Input/Output (Daemon)'],
    install_requires=['swift'],  # removed for better compat
    entry_points={
        'paste.filter_factory': ['interface_header=%s' % entry_point]
    }
)
