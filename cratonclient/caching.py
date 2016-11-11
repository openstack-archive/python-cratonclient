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
"""Caching utilities for use with the Craton API Client."""
import dogpile.cache
import enum

from cratonclient import session as cc_session


class Cache(enum.Enum):
    """The supported caching backends for use with cratonclient."""

    """Cache items in memory using a basic Python dictionary.

    This will not expire items and there will be no limit placed on memory.
    Items added to this cache will need to be removed manually and
    cratonclient does not implement that for you. This is purely a limitation
    of dogpile.cache. See:
    https://dogpilecache.readthedocs.io/en/latest/api.html#dogpile.cache.backends.memory.MemoryBackend
    for more details.

    Example usage:

    .. code-block:: python

        from cratonclient import caching
        from cratonclient.v1 import client

        session = caching.create_session(
            username='demo',
            token='demo',
            project_id='b9f10eca66ac4c279c139d01e65f96b4',
            cache=caching.Cache.in_memory,
        )
        craton = client.Client(
            session=session,
            url='http://127.0.0.1:8080/'
        )

    """
    in_memory = 'dogpile.cache.memory'

    """Cache items using a local file.

    This will store items in a file locally on disk. Users may configure the
    name of the file and expiration time for an item.

    Example usage:

    .. code-block:: python

        from cratonclient import caching
        from cratonclient.v1 import client

        session = caching.create_session(
            username='demo',
            token='demo',
            project_id='b9f10eca66ac4c279c139d01e65f96b4',
            cache=caching.Cache.on_disk,
            expiration_time=300,  # 5 minutes
            filename='cratonclient.cache.dbm',
        )
        craton = client.Client(
            session=session,
            url='http://127.0.0.1:8080/'
        )

    """
    on_disk = 'dogpile.cache.dbm'
    """Cache items using Memcached.

    This will store items in the memcached service that the user configures.
    Users may configure the expiration time and URL.

    Example usage:

    .. code-block:: python

        from cratonclient import caching
        from cratonclient.v1 import client

        session = caching.create_session(
            username='demo',
            token='demo',
            project_id='b9f10eca66ac4c279c139d01e65f96b4',
            cache=caching.Cache.using_memcached,
            expiration_time=300,  # 5 minutes
            url='127.0.0.1:11211',
        )
        craton = client.Client(
            session=session,
            url='http://127.0.0.1:8080/'
        )

    """
    using_memcached = 'dogpile.cache.memcached'


def configure(backend, **configuration_keyword_arguments):
    """Create a dogpile.cache region and configure it.

    :param Cache backend:
        The type of backend to use, based on what cratonclient supports.
        This must be a member of the :class:`Cache` enum.
    :param configuration_keyword_arguments:
        The allowed keyword arguments to configure a particular backend.
    :returns:
        A configured dogpile.cache region.
    :rtype:
        dogpile.cache.region.CacheRegion
    :raises ValueError:
        if the ``backend`` is not a member of :class:`Cache`.
    """
    if not isinstance(backend, Cache):
        raise ValueError('Provided cache backend is not a valid option.')

    region = dogpile.cache.make_region(name='cratonclient')

    if backend is not Cache.in_memory:
        expiration_time = configuration_keyword_arguments.pop(
            'expiration_time', None,
        )
        region.configure(
            backend.value,
            expiration_time=expiration_time,
            arguments=configuration_keyword_arguments,
        )
    else:
        region.configure(backend.value)

    return region


def create_session(session=None, username=None, token=None, project_id=None,
                   cache=None, **cache_configuration_args):
    """Create a cratonclient session with caching enabled.

    This will create an instance of :class:`~cratonclient.session.Session`
    with the provided arguments. It will then create a cache region to wrap
    the session.

    :param session:
        See documentation for :class:`~cratonclient.session.Session`.
    :param username:
        See documentation for :class:`~cratonclient.session.Session`.
    :param token:
        See documentation for :class:`~cratonclient.session.Session`.
    :param project_id:
        See documentation for :class:`~cratonclient.session.Session`.
    :param Cache cache:
        The type of cache backend to use. This must be a member of the
        :class:`Cache` enum, i.e., ``Cache.in_memory``, ``Cache.on_disk``,.
    :param cache_configuration_args:
        The arguments used to configure the cache backend.
    :returns:
        The cratonclient Session wrapped with the caching mechanism.
    :rtype:
        cratonclient.session.Session
    :raises ValueError:
        if the ``cache`` argument is not a member of :class`Cache`.
    """
    craton_session = cc_session.Session(
        session=session,
        username=username,
        token=token,
        project_id=project_id,
    )
    region = configure(backend=cache, **cache_configuration_args)
    craton_session.request = region.cache_on_arguments(craton_session.request)
    craton_session._cache_region = region
    return craton_session
