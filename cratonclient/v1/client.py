"""Top-level client for version 1 of Craton's API."""
from cratonclient.v1 import regions


class Client(object):
    def __init__(self, session, url):
        self._url = url
        self._session = session

        self.regions = regions.RegionManager(self._session, self._url)
