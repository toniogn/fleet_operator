import matplotlib.pyplot as plt
from fleet_operator_refactored.core.controler import FleetOperator
from fleet_operator_refactored.input import JsonInput
from fleet_operator_refactored.resources import JsonResources
from fleet_operator_refactored.utils.criterions import poor_criterion, performant_criterion, medium_criterion

resources_adapter = JsonResources("data/fleet.json")
business_logic = FleetOperator(resources_adapter.data)
input_adapter = JsonInput("data/inputs.json")

run_1_output = input_adapter.run(business_logic.build_fleet(), performant_criterion)
run_2_output = input_adapter.run(business_logic.build_fleet(), poor_criterion)
run_3_output = input_adapter.run(business_logic.build_fleet(), medium_criterion)

plt.figure()
plt.plot(run_1_output.time, run_1_output.grades, label="Performant criterion")
plt.plot(run_2_output.time, run_2_output.grades, label="Poor criterion")
plt.plot(run_3_output.time, run_3_output.grades, label="Medium criterion")
plt.legend()
plt.show()
