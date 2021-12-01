import matplotlib.pyplot as plt
from fleet_operator.core import FleetControler

fleet_controler = FleetControler()

run_1_time, run_1_grades = fleet_controler.run("PERFORMANT")
run_2_time, run_2_grades = fleet_controler.run("POOR")
run_3_time, run_3_grades = fleet_controler.run("MEDIUM")

plt.figure()
plt.plot(run_1_time, run_1_grades, label="Performant criterion")
plt.plot(run_2_time, run_2_grades, label="Poor criterion")
plt.plot(run_3_time, run_3_grades, label="Medium criterion")
plt.legend()
plt.show()
