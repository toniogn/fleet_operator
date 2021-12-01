import matplotlib.pyplot as plt
from fleet_operator.domain.core import FleetControler
from fleet_operator.user import JsonUserAdapter
from fleet_operator.server import JsonServerAdapter


server_side_adapter = JsonServerAdapter()
fleet_controler = FleetControler(server_side_adapter)

user_side_adapter_1 = JsonUserAdapter(fleet_controler, use_priority_criterion="PERFORMANT")
user_side_adapter_2 = JsonUserAdapter(fleet_controler, use_priority_criterion="POOR")
user_side_adapter_3 = JsonUserAdapter(fleet_controler, use_priority_criterion="MEDIUM")

run_1_output = user_side_adapter_1.run()
run_2_output = user_side_adapter_2.run()
run_3_output = user_side_adapter_3.run()

plt.figure()
plt.plot(run_1_output.time, run_1_output.grades, label="Performant criterion")
plt.plot(run_2_output.time, run_2_output.grades, label="Poor criterion")
plt.plot(run_3_output.time, run_3_output.grades, label="Medium criterion")
plt.legend()
plt.show()
