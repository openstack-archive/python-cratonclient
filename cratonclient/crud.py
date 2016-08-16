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
"""Client for CRUD operations."""
import copy

from oslo_utils import strutils


class CRUDClient(object):
    """Class that handles the basic create, read, upload, delete workflow."""

    key = None
    base_path = None
    resource_class = None

    def __init__(self, session, url):
        """Initialize our Client with a session and base url."""
        self.session = session
        self.url = url.rstrip('/')

    def build_url(self, path_arguments=None):
        """Build a complete URL from the url, base_path, and arguments.

        A CRUDClient is constructed with the base URL, e.g.

        .. code-block:: python

            RegionManager(url='https://10.1.1.0:8080/v1', ...)

        The child class of the CRUDClient may set the ``base_path``, e.g.,

        .. code-block:: python

            base_path = '/regions'

        And it's ``key``, e.g.,

        .. code-block:: python

            key = 'region'

        And based on the ``path_arguments`` parameter we will construct a
        complete URL. For example, if someone calls:

        .. code-block:: python

            self.build_url(path_arguments={'region_id': 1})

        with the hypothetical values above, we would return

            https://10.1.1.0:8080/v1/regions/1

        Users can also override ``base_path`` in ``path_arguments``.
        """
        if path_arguments is None:
            path_arguments = {}

        base_path = path_arguments.pop('base_path', None) or self.base_path
        item_id = path_arguments.pop('{0}_id'.format(self.key), None)

        url = self.url + base_path

        if item_id is not None:
            url += '/{0}'.format(item_id)

        return url

    def create(self, **kwargs):
        """Create a new item based on the keyword arguments provided."""
        url = self.build_url(path_arguments=kwargs)
        response = self.session.post(url, json=kwargs)
        return self.resource_class(self, response.json())

    def get(self, **kwargs):
        """Retrieve the item based on the keyword arguments provided."""
        url = self.build_url(path_arguments=kwargs)
        response = self.session.get(url)
        return self.resource_class(self, response.json())

    def list(self, **kwargs):
        """List the items from this endpoint."""
        url = self.build_url(path_arguments=kwargs)
        response = self.session.get(url, params=kwargs)
        return [self.resource_class(self, item) for item in response.json()]

    def update(self, **kwargs):
        """Update the item based on the keyword arguments provided."""
        url = self.build_url(path_arguments=kwargs)
        response = self.session.put(url, params=kwargs)
        return self.resource_class(self, response.json())

    def delete(self, **kwargs):
        """Delete the item based on the keyword arguments provided."""
        url = self.build_url(path_arguments=kwargs)
        return self.session.delete(url, params=kwargs)


# NOTE(sigmavirus24): Credit for this Resource object goes to the
# keystoneclient developers and contributors.
class Resource(object):
    """Base class for OpenStack resources (tenant, user, etc.).

    This is pretty much just a bag for attributes.
    """

    HUMAN_ID = False
    NAME_ATTR = 'name'

    def __init__(self, manager, info, loaded=False):
        """Populate and bind to a manager.

        :param manager: BaseManager object
        :param info: dictionary representing resource attributes
        :param loaded: prevent lazy-loading if set to True
        """
        self.manager = manager
        self._info = info
        self._add_details(info)
        self._loaded = loaded

    def __repr__(self):
        """Return string representation of resource attributes."""
        reprkeys = sorted(k
                          for k in self.__dict__.keys()
                          if k[0] != '_' and k != 'manager')
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)

    @property
    def human_id(self):
        """Human-readable ID which can be used for bash completion."""
        if self.HUMAN_ID:
            name = getattr(self, self.NAME_ATTR, None)
            if name is not None:
                return strutils.to_slug(name)
        return None

    def _add_details(self, info):
        for (k, v) in info.items():
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:  # nosec(cjschaef): we already defined the
                # attribute on the class
                pass

    def __getattr__(self, k):
        """Checking attrbiute existence."""
        if k not in self.__dict__:
            # NOTE(bcwaldon): disallow lazy-loading if already loaded once
            if not self.is_loaded():
                self.get()
                return self.__getattr__(k)

            raise AttributeError(k)
        else:
            return self.__dict__[k]

    def get(self):
        """Support for lazy loading details.

        Some clients, such as novaclient have the option to lazy load the
        details, details which can be loaded with this function.
        """
        # set_loaded() first ... so if we have to bail, we know we tried.
        self.set_loaded(True)
        if not hasattr(self.manager, 'get'):
            return

        new = self.manager.get(self.id)
        if new:
            self._add_details(new._info)
            self._add_details(
                {'x_request_id': self.manager.client.last_request_id})

    def __eq__(self, other):
        """Define equality for resources."""
        if not isinstance(other, Resource):
            return NotImplemented
        # two resources of different types are not equal
        if not isinstance(other, self.__class__):
            return False
        return self._info == other._info

    def is_loaded(self):
        """Check if the resource has been loaded."""
        return self._loaded

    def set_loaded(self, val):
        """Set whether the resource has been loaded or not."""
        self._loaded = val

    def to_dict(self):
        """Return the resource as a dictionary."""
        return copy.deepcopy(self._info)

    def delete(self):
        """Delete the resource from the service."""
        return self.manager.delete(self)
