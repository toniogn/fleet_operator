from json import load, JSONDecodeError
from abc import ABC, abstractmethod
from typing import Callable
from pkg_resources import resource_filename
from fleet_operator.utils.data_models import InputsData, OutputsData
from fleet_operator.core.core import Fleet, Vehicle


class Input(ABC):
    """Inputs interface to inherit from (user-side)."""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__()
        self.data = InputsData(**self.get_inputs(*args, **kwargs))

    @abstractmethod
    def get_inputs(self, *args: list, **kwargs: dict) -> dict:
        """Returns a dictionary of the inputs.

        Parameters
        ----------
        args : list
            List of unnamed parameters.
        kwargs : dict
            Dictionary of named parameters.

        Returns
        -------
        dict
            Dictionary containing the inputs.
        """

    def run(
        self, fleet: Fleet, use_priority_criterion: Callable[[Vehicle], float]
    ) -> OutputsData:
        """Run the scenario on the given fleet.

        Parameters
        ----------
        fleet : Fleet
            The fleet instance on which to run the computation according user inputs.
        use_priority_criterion : Callable[[Vehicle], float]
            Priority criterion to choose which vehicle to use in the fleet.

        Returns
        -------
        OutputsData
            Outputs of the computing.
        """
        for index, (time_lapse, fleet_load) in enumerate(self.data.scenario):
            print(
                f"Progession: {round((index + 1) / len(self.data.scenario) * 100, 1)}%"
            )
            fleet.use(time_lapse, fleet_load, use_priority_criterion)
        return OutputsData(time=fleet.time, grades=fleet.grades)


class DirectInput(Input):
    """Inputs adapter for inputs passed as parameters."""

    def get_inputs(self, *args: list, **kwargs: dict) -> dict:
        """Returns directly named parameters."""
        super().get_inputs(*args, **kwargs)
        return kwargs


class JsonInput(Input):
    """Inputs adapater for inputs passed as JSON strings."""

    def get_inputs(self, *args: list, **kwargs: dict) -> dict:
        """Returns dictionary from concatenated json string from json filenames relative to fleet_operator folder."""
        super().get_inputs(*args, **kwargs)
        data = {"scenario": []}
        for arg in args:
            with open(resource_filename("fleet_operator", arg)) as inputs_json:
                try:
                    scenario = load(inputs_json)["scenario"]
                except (TypeError, JSONDecodeError, KeyError):
                    pass
                else:
                    data["scenario"] += scenario
        return data
