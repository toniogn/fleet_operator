from fleet_operator.core.core import Vehicle


def performant_criterion(vehicle: Vehicle) -> float:
    """Describe a criterion computing how long the vehicle can be used until battery's end of life.

    Parameters
    ----------
    vehicle: Vehicle
        Vehicle on which to compute the criterion.
    """
    return (
        vehicle.battery.current_capacity
        - vehicle.battery.MINIMUM_AVAILABLE_CAPACITY_RATIO
        * vehicle.battery.nominal_capacity
    ) / vehicle.power


def medium_criterion(vehicle: Vehicle) -> float:
    """Describe a criterion computing how long the vehicle can be used until battery's end of life.

    Parameters
    ----------
    vehicle: Vehicle
        Vehicle on which to compute the criterion.
    """
    return vehicle.battery.current_capacity / vehicle.power


def poor_criterion(vehicle: Vehicle) -> float:
    """Describe a criterion computing how long the vehicle can be used until battery's end of life.

    Parameters
    ----------
    vehicle: Vehicle
        Vehicle on which to compute the criterion.
    """
    return vehicle.battery.cell.soc
