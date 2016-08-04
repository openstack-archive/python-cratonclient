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

from cratonclient.v1 import hosts


class Inventory(object):
    """Representation of the viewable inventory."""

    def __init__(self, session, url, region_id):
        """Initialize our client object with our session and url.
        :param session:
            Initialized Session object.
        :type session:
            cratonclient.session.Session
        :param str url:
            The URL that points us to the craton instance. For example,
            'https://10.1.1.0:8080/'.
        """

        # TODO(cmspence): self.region = self.regions.get(region=region_id)
        self.hosts = hosts.HostManager(session, url)
        # TODO(cmspence): self.users, self.projects, self.workflows