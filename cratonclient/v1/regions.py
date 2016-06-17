"""Regions manager code."""
from cratonclient import crud


class Region(crud.Resource):
    """Representation of a Region."""

    pass


class RegionManager(crud.CRUDClient):
    """A manager for regions."""

    key = 'region'
    base_path = '/regions'
    resource_class = Region
