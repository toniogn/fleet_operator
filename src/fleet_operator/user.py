from json import loads
from pkg_resources import resource_filename
from .domain.user import IRequestInputsData


class ConsoleUserAdapter(IRequestInputsData):
    """Inputs adapter for inputs passed as parameters."""

    def get_inputs_data(self, *args: list, **kwargs: dict) -> dict:
        """Returns directly named parameters."""
        super().get_inputs_data(*args, **kwargs)
        return kwargs


class JsonUserAdapter(IRequestInputsData):
    """Inputs adapater for inputs passed as JSON strings."""

    def get_inputs_data(self, *args: list, **kwargs: dict) -> dict:
        """Returns dictionary from concatenated json string from json filenames relative to fleet_operator folder."""
        super().get_inputs_data(*args, **kwargs)
        with open(
            resource_filename("fleet_operator", "data/scenario.json"), "r"
        ) as scenario_json:
            scenario = loads(scenario_json.read())
        kwargs["scenario"] = scenario
        return kwargs
