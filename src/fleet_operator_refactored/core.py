from typing import Callable, List, Union, Tuple
from copy import deepcopy
from scipy import interpolate
from itertools import count, chain
from .resources import Resources
from .utils.data_models import ResourcesData
from .utils.utils import (
    EmptyCellError,
    FullCellError,
    BatteryLifetimeError,
    TooPowerfullDischargeError,
    Constants,
)


class Cell:
    """Battery object.

    Parameters
    ----------
    ocv : Callable
        Function of the state of charge returning open circuit voltage (V).
    resistance : float
        Internal resistance of the cell (Ohms).
    nominal_capacity : float
        Nominal capacity of the battery at birth (C).
    alpha : float
        Cell's capacity ageing coefficient (1/(W.s)).
    beta : float
        Cell's internal resistance ageing coefficient (1/(W.s)).
    """

    DEFAULT_OCV = interpolate.interp1d([0, 1], [3, 4.2], bounds_error=True)
    DEFAULT_RESISTANCE = 70 * 1e-3
    DEFAULT_NOMINAL_CAPACITY = 2600 * 1e-3 * Constants.SECONDS_PER_HOUR
    TIME_INCREMENT = 120

    def __init__(
        self,
        ocv: Callable = DEFAULT_OCV,
        resistance: Callable = DEFAULT_RESISTANCE,
        nominal_capacity: float = DEFAULT_NOMINAL_CAPACITY,
        alpha: float = 0,
        beta: float = 0,
    ) -> None:
        self.soc = 1
        self.ocv = ocv
        self.resistance = resistance
        self.alpha = alpha
        self.beta = beta
        self.tension = self.ocv(self.soc)
        self.nominal_capacity = self.c_to_wh(nominal_capacity, self.tension)
        self.available_capacity = self.nominal_capacity
        self.current_capacity = self.available_capacity

    def __age(self, power: float) -> Tuple[float, float]:
        """Ages the cell according to power of use.

        Parameters
        ----------
        power : float
            Power of use (W).

        Returns
        -------
        Tuple[float, float]
            Aged maximum available capacity (Wh) and aged resistance (Ohms).
        """
        available_capacity = self.available_capacity * (
            1 - self.alpha * self.TIME_INCREMENT * abs(power)
        )
        resistance = self.resistance * (
            1 + self.beta * self.TIME_INCREMENT * abs(power)
        )
        return available_capacity, resistance

    def compute_tension(self, power: float) -> float:
        """Computes the tension of the cell.

        Computes the voltage of the cell under a certain power of use.

        Parameters
        ----------
        power : float
            Power of use (W).

        Returns
        -------
        float
            Cell's voltage (V).
        """
        delta = self.ocv(self.soc) ** 2 + 4 * self.resistance * power
        if delta < 0:
            raise TooPowerfullDischargeError
        elif delta == 0:
            return self.ocv(self.soc) / 2
        else:
            return (self.ocv(self.soc) + delta ** 0.5) / 2

    def __use_on_time_increment(self, power: float) -> None:
        """Uses the cell for a time increment.

        Uses and ages accordingly the cell for a time increment with a given power.

        Parameters
        ----------
        power : float
            Power of use (W).
        """
        tension = self.compute_tension(power)
        capacity_delta = self.c_to_wh(power / tension * self.TIME_INCREMENT, tension)
        available_capacity, resistance = self.__age(power)
        if self.current_capacity + capacity_delta < 0:
            raise EmptyCellError
        elif self.current_capacity + capacity_delta > available_capacity:
            raise FullCellError
        else:
            self.available_capacity = available_capacity
            self.resistance = resistance
            self.tension = tension
            self.current_capacity += capacity_delta
            self.soc = self.current_capacity / self.available_capacity

    def use(self, timelapse: float, power: float) -> None:
        """Uses the cell for a given timelapse with a given power.

        Parameters
        ----------
        timelapse : float
            Timelapse of use (s).
        power : float
            Power of use (W).
        """
        elapsed_time = 0
        while elapsed_time < timelapse:
            elapsed_time += self.TIME_INCREMENT
            self.__use_on_time_increment(power)

    def __repr__(self) -> str:
        return "Cell({}, {}, {}, {}, {})".format(
            self.ocv, self.resistance, self.nominal_capacity, self.alpha, self.beta
        )

    def c_to_wh(self, c_capacity: float, tension: float) -> float:
        """Converts a capacity in C to a Wh.

        Paramaters
        ----------
        c_capacity : float
            Capacity to convert (C).
        tension : float
            Tension used for conversion (V).

        Returns
        -------
        float
            Converted capacity (Wh).
        """
        return c_capacity * tension / Constants.SECONDS_PER_HOUR


class Battery:
    """Battery object.

    Parameters
    ----------
    cell : Cell
        Cells used to build the battery.
    series_cells_number : int
        Number of series cells per branch.
    parallel_branches_number : int
        Number of parallel branches.
    """

    MINIMUM_AVAILABLE_CAPACITY_RATIO: float = 0.3

    def __init__(
        self,
        cell: Cell = Cell(),
        series_cells_number: int = 100,
        parallel_branches_number: int = 10,
    ) -> None:
        self.cell = cell
        self.series_cells_number = series_cells_number
        self.parallel_branches_number = parallel_branches_number
        self.nominal_capacity = self.cell.nominal_capacity * parallel_branches_number
        self.available_capacity = (
            self.cell.available_capacity * self.parallel_branches_number
        )
        self.current_capacity = (
            self.cell.current_capacity * self.parallel_branches_number
        )
        self.tension = self.cell.tension * self.series_cells_number

    def use(self, timelapse: float, power: float) -> None:
        """Method to use the battery.

        Use the battery depending on the wanted power.

        Parameters
        ----------
        timelapse : float
            Time lapse of using (s).
        power : float
            Power of using (positive for charge and negative for discharge) (W).
        """
        self.cell.use(
            timelapse,
            power / (self.series_cells_number * self.parallel_branches_number),
        )
        self.tension = self.cell.tension * self.series_cells_number
        self.available_capacity = (
            self.cell.available_capacity * self.parallel_branches_number
        )
        self.current_capacity = (
            self.cell.current_capacity * self.parallel_branches_number
        )
        if (
            self.available_capacity / self.nominal_capacity
            <= self.MINIMUM_AVAILABLE_CAPACITY_RATIO
        ):
            raise BatteryLifetimeError

    def __repr__(self) -> str:
        return "Battery({}, {}, {})".format(
            repr(self.cell), self.series_cells_number, self.parallel_branches_number
        )


class Vehicle:
    """Vehicle object.

    Parameters
    ----------
    power : float
        The electrical power consumption of the vehicle (W).

    Attributes
    ----------
    battery : Battery
        Battery of the vehicle.
    id : str
        Unique identification code of the vehicle.
    """

    DEFAULT_POWER: float = 20e3
    __ids = count(0)

    def __init__(self, power: float = 20e3, battery: Battery = Battery()) -> None:
        self.power = power
        self.battery = battery
        self.id = "V#{}".format(next(self.__ids))
        self.__needed_battery = deepcopy(battery)

    def use(self, timelapse: float) -> None:
        """Uses the vehicle for a given time lapse.

        Parameters
        ----------
        time_lapse : float
            Time lapse of vehicle's using (s).
        """
        try:
            self.battery.use(timelapse, -self.power)
        except BatteryLifetimeError:
            self.change_battery()
            self.use(timelapse)
        except TooPowerfullDischargeError:
            self.upgrade_battery()
            self.use(timelapse)

    def charge(self, timelapse: float, power: float):
        """Charges the vehicle for a given time lapse.

        Parameters
        ----------
        time_lapse : float
            Time lapse of vehicle's charging (s).
        power : float
            Power of charging (W).
        """
        try:
            self.battery.use(timelapse, power)
        except BatteryLifetimeError:
            self.change_battery()

    def change_battery(
        self,
    ) -> None:
        """Renew the battery of a vehicle."""
        self.battery = deepcopy(self.__needed_battery)

    def upgrade_battery(
        self, series_multiplier: int = 1, parallel_multiplier: int = 2
    ) -> None:
        """Upgrades the battery according to multipliers.

        Parameters
        ----------
        series_multiplier : int
            Multiplier of the number of series cells in each branches.
        parallel_multiplier : int
            Multiplier of the number of branches.
        """
        self.battery = Battery(
            deepcopy(self.__needed_battery.cell),
            self.__needed_battery.series_cells_number * series_multiplier,
            self.__needed_battery.parallel_branches_number * parallel_multiplier,
        )
        self.__needed_battery = deepcopy(self.battery)

    def __repr__(self) -> str:
        return "Vehicle({}, {})".format(self.power, repr(self.battery))


class ChargingStation:
    """Charging station object.

    Parameters
    ----------
    power : float
        Electrical power delivered by the charging station (W).
    """

    def __init__(self, power: float = 100e3) -> None:
        self.power = power
        self.plugged_vehicle = None

    def charge(self, time_lapse: float):
        """Charges the plugged vehicle for a given time lapse.

        Parameters
        ----------
        time_lapse : float
            Time lapse of plugged vehicle's charging (s).
        """
        if self.plugged_vehicle is None:
            raise ValueError("A vehicle must be plugged to be charged.")
        self.plugged_vehicle.charge(time_lapse, self.power)
        self.plugged_vehicle = None

    def plug_vehicle(self, vehicle: Vehicle) -> None:
        """Plugs a vehicle.

        Parameters
        ----------
        vehicle : 'Vehicle'
            Vehicle to plug.
        """
        self.plugged_vehicle = vehicle

    def __repr__(self) -> str:
        return "ChargingStation({})".format(self.power)


class Fleet:
    """Fleet object.

    A fleet contains several 'Vehicle' instances and has several 'ChargingStation' instances available to charge them.
    """

    def __init__(self, *args: List[Union[Vehicle, ChargingStation]]) -> None:
        self.__vehicles: List[Vehicle] = []
        self.__charging_stations: List[ChargingStation] = []
        for arg in args:
            if isinstance(arg, Vehicle):
                self.__vehicles.append(arg)
            elif isinstance(arg, ChargingStation):
                self.__charging_stations.append(arg)
        self.time = [0]
        self.grades = [0]

    def use(
        self,
        timelapse: float,
        load: float,
        use_priority_criterion: Callable[[Vehicle], float],
    ) -> None:
        """Method to use the fleet.

        Uses the fleet for a given time lapse at a given load (between 0 and 1 to tell how much the fleet is used).
        The part of the fleet which isn't used is charged in the charging stations' availability limit.

        Parameters
        ----------
        timelapse : float
            Time lapse of fleet use (s).
        load : float
            Load of use of the fleet.
        use_priority_criterion : Callable[[Vehicle], float]
            A function that takes a 'Vehicle' instance as input and that returns a numerical sorting criterion (vehicle's battery's age for instance). Higher the criterion is, higher the priority will be to use the vehicle.
        """
        number_of_vehicles_to_use = round(load * len(self.__vehicles))
        sorted_vehicles = sorted(
            self.__vehicles, key=use_priority_criterion, reverse=True
        )
        vehicles_to_use = {
            vehicle.id: vehicle
            for vehicle in sorted_vehicles[:number_of_vehicles_to_use]
        }
        vehicles_to_charge = {
            vehicle.id: vehicle
            for vehicle in sorted_vehicles[number_of_vehicles_to_use:]
        }
        failed_vehicles = {}

        grade = 0
        for vehicle in vehicles_to_use.values():  # Loop on vehicles to use
            try:
                vehicle.use(timelapse)
            except EmptyCellError:  # A vehicle to use experiences a too low battery error, we add it at the first place of the list of vehicles to charge
                failed_vehicles[vehicle.id] = vehicle
            else:
                grade += 1

        if len(vehicles_to_use) > 0:
            grade /= len(vehicles_to_use)

        vehicles_to_use = {
            vehicle.id: vehicle
            for vehicle in vehicles_to_use.values()
            if vehicle.id not in failed_vehicles.keys()
        }

        for vehicle, charging_station in zip(
            chain(vehicles_to_charge.values(), failed_vehicles.values()),
            self.__charging_stations,
        ):  # Loop on vehicles to charge
            charging_station.plug_vehicle(vehicle)
            try:
                charging_station.charge(timelapse)
            except FullCellError:
                pass

        self.__vehicles = [
            vehicle
            for vehicle in chain(
                vehicles_to_use.values(),
                vehicles_to_charge.values(),
                failed_vehicles.values(),
            )
        ]
        self.time.append(timelapse + self.time[-1])
        self.grades.append(grade + self.grades[-1])

    def extend_fleet(self, *args: List[Vehicle]) -> None:
        """Extends the fleet with new vehicles."""
        for arg in args:
            if isinstance(arg, Vehicle):
                self.__vehicles.append(arg)

    def add_charging_stations(self, *args: List[ChargingStation]) -> None:
        """Adds new charging stations to the fleet."""
        for arg in args:
            if isinstance(arg, ChargingStation):
                self.__charging_stations.append(arg)

    def __repr__(self) -> str:
        return "Fleet(*{})".format(
            [repr(vehicle) for vehicle in self.__vehicles]
            + [repr(charging_station) for charging_station in self.__charging_stations]
        )


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