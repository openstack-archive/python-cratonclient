"""Top-level client for version 1 of Craton's API."""
from cratonclient.v1 import hosts
from cratonclient.v1 import regions


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

        manager_kwargs = {'session': self._session, 'url': url}

        self.hosts = hosts.HostManager(**manager_kwargs)
        self.regions = regions.RegionManager(**manager_kwargs)
