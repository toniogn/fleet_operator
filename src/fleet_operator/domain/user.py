from abc import ABC, abstractmethod
from .core import FleetControler
from .data_models import InputsData, OutputsData


class IRequestInputsData(ABC):
    """Inputs interface to inherit from (user-side).

    Parameters
    ----------
    fleet_controler : FleetControler
        Controler of the business logic.
    """

    def __init__(
        self, fleet_controler: FleetControler, *args: list, **kwargs: dict
    ) -> None:
        super().__init__()
        self.data = InputsData(**self.get_inputs_data(*args, **kwargs))
        self.fleet_controler = fleet_controler

    @abstractmethod
    def get_inputs_data(self, *args: list, **kwargs: dict) -> dict:
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

    def run(self) -> OutputsData:
        """Run the scenario on the given fleet.

        Returns
        -------
        OutputsData
            Outputs of the computing.
        """
        self.fleet_controler.fleet.reset()
        for index, (time_lapse, fleet_load) in enumerate(self.data.scenario):
            print(
                f"Progession: {round((index + 1) / len(self.data.scenario) * 100, 1)}%"
            )
            self.fleet_controler.fleet.use(
                time_lapse, fleet_load, self.data.use_priority_criterion
            )
        return OutputsData(
            time=self.fleet_controler.fleet.time,
            grades=self.fleet_controler.fleet.grades,
        )