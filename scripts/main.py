import matplotlib.pyplot as plt
from fleet_operator.core import FleetControler
from fleet_operator.criterions import poor_criterion, performant_criterion, medium_criterion

fleet_controler = FleetControler()

run_1_time, run_1_grades = fleet_controler.run(performant_criterion)
run_2_time, run_2_grades = fleet_controler.run(poor_criterion)
run_3_time, run_3_grades = fleet_controler.run(medium_criterion)

plt.figure()
plt.plot(run_1_time, run_1_grades, label="Performant criterion")
plt.plot(run_2_time, run_2_grades, label="Poor criterion")
plt.plot(run_3_time, run_3_grades, label="Medium criterion")
plt.legend()
plt.show()
