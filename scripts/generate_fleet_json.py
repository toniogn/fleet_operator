import json
from random import random
from fleet_operator.utils import Constants

number_of_vehicles = 100
number_of_charging_stations = 20

cell_nominal_capacity_range = (
    2 * Constants.SECONDS_PER_HOUR,
    3 * Constants.SECONDS_PER_HOUR,
)
battery_series_cells_number_range = (50, 150)
battery_parallel_branches_number = (5, 15)
vehicle_power_range = (10e3, 50e3)
charging_stations_power_range = (50e3, 150e3)

fleet = {"vehicles": [], "charging_stations": []}

for i in range(number_of_vehicles):
    fleet["vehicles"].append(
        tuple(
            random() * (max(value_range) - min(value_range)) + min(value_range)
            for value_range in [
                cell_nominal_capacity_range,
                battery_series_cells_number_range,
                battery_parallel_branches_number,
                vehicle_power_range,
            ]
        )
    )

for i in range(number_of_charging_stations):
    fleet["charging_stations"].append(
        random()
        * (max(charging_stations_power_range) - min(charging_stations_power_range))
        + min(charging_stations_power_range)
    )

fleet_json = json.dumps(fleet)

with open("./src/fleet_operator/data/fleet.json", "w+") as file:
    file.write(fleet_json)
