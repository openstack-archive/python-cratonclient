# -*- coding: utf-8 -*-

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
"""Hosts resource and resource shell wrapper."""
from cratonclient.common import cliutils


def do_host_list(cc, args):
    """Print list of hosts which are registered with the Craton service."""
    params = {}
    columns = ['id', 'name']
    hosts = cc.hosts.list(args.craton_project_id, **params)
    cliutils.print_list(hosts, columns)
