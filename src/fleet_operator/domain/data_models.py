from typing import Literal, Tuple
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import confloat, conint, conlist


class ResourcesData(BaseModel):
    vehicles: conlist(
        Tuple[confloat(gt=0), conint(gt=0), conint(gt=0), confloat(gt=0)],
        min_items=1,
    ) = Field(
        ...,
        description="Vehicle's to build as a list of tuples: vehicle's battery's cell nominal capacity (C), battery's number of cells in series, battery's number of parallel branches and power consumption of the vehicle (W).",
    )
    charging_stations: conlist(confloat(gt=0), min_items=1) = Field(
        ..., description="Charging stations as a list of delivered power (W)."
    )


class InputsData(BaseModel):
    scenario: conlist(Tuple[confloat(gt=0), confloat(ge=0, le=1)], min_items=1) = Field(
        ...,
        description="Scenario of fleet tasks to realize as a list of tuples: timelapse of task (s), task's needed fleet's load.",
    )
    use_priority_criterion: Literal["POOR", "MEDIUM", "PERFORMANT"] = Field(
        ...,
        description="Criterion to use to sort vehicles and so to choose which ones will be used for a given task.",
    )


class OutputsData(BaseModel):
    grades: conlist(float, min_items=1) = Field(
        ...,
        description="Cumulated number of fleet's succeded tasks (timelapse and load respected).",
    )
    time: conlist(float, min_items=1) = Field(
        ..., description="Time vector gathering the time step at each scenario frame."
    )
