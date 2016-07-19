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
import argparse
import pkg_resources as resources

from cratonclient.common import cliutils


def commands():
    """Define host-* commands and matching function."""
    env = resources.Environment()
    dist = env.__getitem__('python-cratonclient')[0]
    return {
        'host-list': resources.EntryPoint('list',
                                          'cratonclient.shell.v1.hosts_shell',
                                          attrs=('do_host_list',),
                                          dist=dist),
    }


def do_host_list(cc, args):
    """Print list of hosts which are registered with the Craton service."""
    parser = argparse.ArgumentParser(prog="craton host-list")
    args = parser.parse_args(args)

    params = {}
    columns = ['id', 'name']
    hosts = cc.hosts.list(**params)
    cliutils.print_list(hosts, columns)
