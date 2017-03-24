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
from cratonclient.v1 import cells
from cratonclient.v1 import clouds
from cratonclient.v1 import devices
from cratonclient.v1 import hosts
from cratonclient.v1 import projects
from cratonclient.v1 import regions


class Client(object):
    """Craton v1 API Client.

    .. attribute:: cells

        The canonical way to list, get, delete, or update cell objects via a
        :class:`~cratonclient.v1.cells.CellManager` instance.

    .. attribute:: clouds

        The canonical way to list, get, delete, or update cloud objects via a
        :class:`~cratonclient.v1.clouds.CloudManager` instance.

    .. attribute:: devices

        The canonical way to list devicess via a
        :class:`~cratonclient.v1.devices.DeviceManager` instance.

    .. attribute:: hosts

        The canonical way to list, get, delete, or update host objects via a
        :class:`~cratonclient.v1.hosts.HostManager` instance.

    .. attribute:: projects

        The canonical way to list, get, delete, or update project objects via
        a :class:`~cratonclient.v1.projects.ProjectManager` instance.

    .. attribute:: regions

        The canonical way to list, get, delete, or update region objects via a
        :class:`~cratonclient.v1.regions.RegionManager` instance.

    """

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

        manager_kwargs = {'session': self._session, 'url': self._url}
        self.hosts = hosts.HostManager(**manager_kwargs)
        self.cells = cells.CellManager(**manager_kwargs)
        self.projects = projects.ProjectManager(**manager_kwargs)
        self.clouds = clouds.CloudManager(**manager_kwargs)
        self.devices = devices.DeviceManager(**manager_kwargs)
        self.regions = regions.RegionManager(**manager_kwargs)
