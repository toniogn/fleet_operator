import json
from random import random
from fleet_operator.domain.utils import Constants

tasks_number = 500

load_range = (0.1, 1)
timelapse_range = (Constants.SECONDS_PER_HOUR / 4, Constants.SECONDS_PER_HOUR * 2)

scenario = []

for i in range(tasks_number):
    scenario.append(
        tuple(
            random() * (max(value_range) - min(value_range)) + min(value_range)
            for value_range in [
                timelapse_range,
                load_range,
            ]
        )
    )

scenario_json = json.dumps(scenario)

with open("./src/fleet_operator/data/scenario.json", "w+") as file:
    file.write(scenario_json)
