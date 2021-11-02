from fleet_operator.core.core import Cell, ChargingStation, Vehicle, Fleet, Battery
from fleet_operator.utils.data_models import ResourcesData


class FleetOperator:
    """Controler object that instanciate core objects.

    Parameters
    ----------
    resources_data : ResourcesData
        Given resources to build the fleet.
    """

    def __init__(self, resources_data: ResourcesData) -> None:
        self.resources_data = resources_data

    def build_fleet(self) -> Fleet:
        """Builds the fleet according to resources data."""
        fleet = Fleet()
        for (
            cell_nominal_capacity,
            battery_series_cells_number,
            battery_parallel_branches_number,
            vehicle_power,
        ) in self.resources_data.vehicles:
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
        for vehicle_power in self.resources_data.charging_stations:
            fleet.add_charging_stations(ChargingStation(vehicle_power))
        return fleet
