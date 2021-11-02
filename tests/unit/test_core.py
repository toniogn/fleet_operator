import unittest
from fleet_operator.utils.utils import BatteryRangeError, Constants
from fleet_operator.core.core import Battery, Vehicle


class TestBattery(unittest.TestCase):
    LIFETIME: float = 8 * Constants.DAYS_PER_YEAR * Constants.HOURS_PER_DAY * Constants.SECONDS_PER_HOUR
    MEAN_VOLTAGE: int = 500
    NOMINAL_CAPACITY: float = 1e5

    def setUp(self) -> None:
        super().setUp()
        self.battery = Battery(self.LIFETIME, self.MEAN_VOLTAGE, self.NOMINAL_CAPACITY)
        self.power = Vehicle.DEFAULT_POWER
        self.time_to_full_discharge = self.battery.wh_to_c(self.NOMINAL_CAPACITY) * self.MEAN_VOLTAGE / self.power
        self.time_to_full_charge = self.LIFETIME * self.MEAN_VOLTAGE * self.battery.wh_to_c(self.NOMINAL_CAPACITY) / (self.power * self.LIFETIME + self.battery.wh_to_c(self.NOMINAL_CAPACITY) * self.MEAN_VOLTAGE)
        self.available_capacity_after_full_discharge = (self.LIFETIME - self.time_to_full_discharge) / self.LIFETIME * self.NOMINAL_CAPACITY
        self.available_capacity_after_full_charge = (self.LIFETIME - self.time_to_full_charge) / self.LIFETIME * self.NOMINAL_CAPACITY

    def test_use_too_long_raises_exception(self) -> None:
        with self.assertRaises(BatteryRangeError):
            self.battery.use(self.time_to_full_discharge + 1, self.power)

    def test_use_too_powerful_raises_exception(self) -> None:
        with self.assertRaises(BatteryRangeError):
            self.battery.use(self.time_to_full_discharge, self.power + 1)

    def test_use_integrity(self) -> None:
        self.battery.use(self.time_to_full_discharge, self.power)
        self.assertEqual([self.battery.soc, self.battery.current_capacity], [0, 0])
        self.assertAlmostEqual(self.battery.available_capacity, self.available_capacity_after_full_discharge)

    def test_charge_integrity(self) -> None:
        self.battery.current_capacity = 0
        self.battery.soc = 0
        self.battery.charge(self.LIFETIME, Vehicle.DEFAULT_POWER)
        self.assertAlmostEqual(self.battery.soc, 1)
        self.assertAlmostEqual(self.battery.current_capacity, self.available_capacity_after_full_charge)
        self.assertAlmostEqual(self.battery.available_capacity, self.available_capacity_after_full_charge)
