from json import load, JSONDecodeError
from abc import ABC, abstractmethod
from fleet_operator.utils.data_models import ResourcesData
from pkg_resources import resource_filename


class Resources(ABC):
    """Resources interface to inherit from (resource-side)."""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__()
        self.data = ResourcesData(**self.get_resources(*args, **kwargs))

    @abstractmethod
    def get_resources(self, *args: list, **kwargs: dict) -> dict:
        """Returns a dictionary of the resources.

        Parameters
        ----------
        args : list
            List of unnamed parameters.
        kwargs : dict
            Dictionary of named parameters.

        Returns
        -------
        dict
            Dictionary containing the resources.
        """


class DirectResources(Resources):
    """Resources adapter for resources passed as parameters."""

    def get_resources(self, *args: list, **kwargs: dict) -> dict:
        """Returns directly named parameters."""
        super().get_resources(*args, **kwargs)
        return kwargs


class JsonResources(Resources):
    """Resources adapater for resources passed as JSON strings."""

    def get_resources(self, *args: list, **kwargs: dict) -> dict:
        """Returns dictionary from concatenated json string from json filenames relative to fleet_operator folder."""
        super().get_resources(*args, **kwargs)
        data = {"vehicles": [], "charging_stations": []}
        for arg in args:
            with open(resource_filename("fleet_operator", arg)) as resources_json:
                try:
                    resources = load(resources_json)
                except (TypeError, JSONDecodeError):
                    pass
                else:
                    data["vehicles"] += resources["vehicles"]
                    data["charging_stations"] += resources["charging_stations"]
        return data
