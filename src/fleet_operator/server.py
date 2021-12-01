from json import loads
from pkg_resources import resource_filename
from .domain.server import IObtainFleetData


class ConsoleServerAdapter(IObtainFleetData):
    """Resources adapter for resources passed as parameters."""

    def get_fleet_data(self, *args: list, **kwargs: dict) -> dict:
        """Returns directly named parameters."""
        super().get_fleet_data(*args, **kwargs)
        return kwargs


class JsonServerAdapter(IObtainFleetData):
    """Resources adapater for resources passed as JSON strings."""

    def get_fleet_data(self, *args: list, **kwargs: dict) -> dict:
        """Returns dictionary from concatenated json string from json filenames relative to fleet_operator folder."""
        super().get_fleet_data(*args, **kwargs)
        with open(
            resource_filename("fleet_operator", "data/fleet.json"), "r"
        ) as resources_json:
            resources = loads(resources_json.read())
        return resources
