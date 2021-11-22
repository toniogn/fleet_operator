import matplotlib.pyplot as plt
from fleet_operator_refactored.core.controler import FleetControler
from fleet_operator_refactored.input import JsonInput
from fleet_operator_refactored.resources import JsonResources
from fleet_operator_refactored.utils.criterions import poor_criterion, performant_criterion, medium_criterion

resources_adapter = JsonResources()
fleet_controler = FleetControler(resources_adapter)
input_adapter = JsonInput(fleet_controler)

run_1_output = input_adapter.run(performant_criterion)
run_2_output = input_adapter.run(poor_criterion)
run_3_output = input_adapter.run(medium_criterion)

plt.figure()
plt.plot(run_1_output.time, run_1_output.grades, label="Performant criterion")
plt.plot(run_2_output.time, run_2_output.grades, label="Poor criterion")
plt.plot(run_3_output.time, run_3_output.grades, label="Medium criterion")
plt.legend()
plt.show()
