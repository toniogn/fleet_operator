from abc import ABC, abstractmethod
from .data_models import ResourcesData


class IObtainFleetData(ABC):
    """Resources interface to inherit from (resource-side)."""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__()
        self.data = ResourcesData(**self.get_fleet_data(*args, **kwargs))

    @abstractmethod
    def get_fleet_data(self, *args: list, **kwargs: dict) -> dict:
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
        pass