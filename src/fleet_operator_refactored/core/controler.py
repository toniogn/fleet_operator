from typing import Callable
from fleet_operator_refactored.utils.data_models import ResourcesData
from .core import Cell, ChargingStation, Vehicle, Fleet, Battery
from ..resources import Resources


class FleetControler:
    """Controler object that instanciate core objects.

    Parameters
    ----------
    resources : Resources
        Resources inherited adpater.
    """

    def __init__(self, resources: Resources) -> None:
        self.fleet = self.build(resources.data)

    def build(self, resources_data: ResourcesData) -> Fleet:
        """Builds the fleet according to resources data.

        Returns
        -------
        Fleet
            The fleet built according to resources data.
        """
        fleet = Fleet()
        for (
            cell_nominal_capacity,
            battery_series_cells_number,
            battery_parallel_branches_number,
            vehicle_power,
        ) in resources_data.vehicles:
            fleet.extend_fleet(
                Vehicle(
                    vehicle_power,
                    Battery(
                        Cell(nominal_capacity=cell_nominal_capacity),
                        battery_series_cells_number,
                        battery_parallel_branches_number,
                    ),
                )
            )
        for vehicle_power in resources_data.charging_stations:
            fleet.add_charging_stations(ChargingStation(vehicle_power))
        return fleet
