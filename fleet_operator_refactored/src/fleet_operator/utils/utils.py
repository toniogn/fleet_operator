class Constants:
    SECONDS_PER_MINUTE: int = 60
    MINUTES_PER_HOUR: int = 60
    SECONDS_PER_HOUR: int = SECONDS_PER_MINUTE * MINUTES_PER_HOUR
    HOURS_PER_DAY: int = 24
    DAYS_PER_YEAR: float = 365.25


class BatteryLifetimeError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__("The battery has to be renewed.", *args)


class EmptyCellError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__("The cell doesn't have enough capacity to be discharged anymore.", *args)


class FullCellError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__("The cell reached it's available capacity.", *args)


class TooPowerfullDischargeError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__("The cell can't handle this much power.", *args)