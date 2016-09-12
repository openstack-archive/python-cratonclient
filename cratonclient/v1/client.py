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
"""Top-level client for version 1 of Craton's API."""
from cratonclient.v1 import inventory


class Client(object):
    """Craton v1 API Client."""

    def __init__(self, session, url):
        """Initialize our client object with our session and url.

        :param session:
            Initialized Session object.
        :type session:
            cratonclient.session.Session
        :param str url:
            The URL that points us to the craton instance. For example,
            'https://10.1.1.0:8080/'.
        """
        self._url = url
        self._session = session

        if not self._url.endswith('/v1'):
            self._url += '/v1'

        self._manager_kwargs = {'session': self._session, 'url': self._url}

    def inventory(self, region_id):
        """Retrieve inventory for a given region."""
        self._manager_kwargs['region_id'] = region_id
        return inventory.Inventory(**self._manager_kwargs)
