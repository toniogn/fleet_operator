# Fleet Operator

## Introduction

Fleet operator is a demonstration project to illustrate and practice hexagonal architecture designing. The business logic purpose is to simulate usage scenarios on an EV vehicles fleet depending on a sorting criterion used to decide if a vehicle of the fleet must be used or charged at some point.

## About Hexagonal Architecture (H.A.)

![hexagonal architecture scheme](https://blog.octo.com/wp-content/uploads/2020/06/archi_hexa_06-1024x526.png)

H.A. is a designing pattern which aims to uncouple the business logic (the hexagon) from the user and the server sides. Practically its realized thanks to interface design pattern which allows to reverse server side dependency and weaken both sides coupling defining generic methods and rules to get and parse user inputs and resources data. For more information see [hexagonal architecture by octo](https://blog.octo.com/architecture-hexagonale-trois-principes-et-un-exemple-dimplementation/).

## Practicing

The root folder contains two child folders. One containing a classical M.V.C. version (without explicit view) of the source code to refactor with an H.A. and the other to explore a refactored solution. There is multiple ways to do it, the proposed refactoring may not be the best one.

## Installation

- Start a terminal and switch to your local repositories folder
- Clone the repository with `git clone https://github.com/toniogn/fleet_operator.git`.
- Create a dedicated virtual environment with `–m venv your_venv_name`.
- Activate it with `your_venv_name/Scripts/activate`.
- Install dependencies with `pip install –r requirements.txt`.

## Repository content

The repository is organized on two branches as follows :
```
-> scripts: contains useful scripts
-----> generate_fleet_json.py: generate resources data
-----> generate_scenario_json.py: generate inputs data
-----> main.py: main file
-> src: contains source codes
-----> fleet_operator
---------> data
-------------> scenario.json: inputs data generated in generate_scenario_json
-------------> fleet.json: resources data generated in generate_fleet_json
---------> etc...
-> .gitignore
-> README.md
-> requirements.txt
```

## Current functioning and problematics

The software version to refactor works as follows :
- FleetControler is instanciated.
  - A Fleet is instanciated and populated with the build_fleet method from fleet.json data.
- A simulation start with the controler's run method taking a sorting function from criterions.py as parameter and loading inputs data from input.json.

Their are two main problematics with M.V.C architecture:

- At « server-side »: dependency must be reversed. With M.V.C. pattern the business logic depends on resources, it has to load them according to the chosen infrastructure. To reverse it one has to create an interface detailing how resources must be loaded and at least one inheriting adapter dedicated to a given resources infrastructure loading.
- At « user-side »: dependency is already well oreiented. For instance, from a python console you can import, instanciate and use business logic objects. Nevertheless, H.A. gives the advantage to explicitly limit the visible method interacting with the business logic. So an interface at this side with at least one adapter should also be implemented.

## Instructions

First of all, swith to the "to_refactor" branch with `git switch to_refactor`.

The instructions could be listed as follows:
- Create a folder called domain to identify what belongs to the business logic (core.py and utils.py within it).
- Create, within the domain folder, user.py and server.py modules respectively implementing IRequestInputsData and IObtainFleetData interfaces with get_inputs_data and get_fleet_data abstract methods both returning dictionaries.
- Create, next to the domain folder, two modules also called user.py and server.py respectively implementing adapters JsonUserAdapter and JsonServerAdapter, inherited from interfaces, loading data from scenario.json and fleet.json.

For interfaces implementing, use the abc library:
```python
from abc import ABC, abstractmethod

class Interface(ABC):
  @abstractmethod
  def abstract_method(self, *args, **kwargs):
    pass
```

For data loading you can re-use the core controler's code:
```python
import json
from pkg_resources import resource_filename

with open(resource_filename("fleet_operator", "path_to_json_file_under_src")) as json_file:
  file_dict = json.load(json_file)
```

If you struggle with H.A. concepts try to refactor the code according to a main file looking like this:
```python
server_side_adapter = JsonServerAdapter()
fleet_controler = FleetControler(server_side_adapter)
inputs_adapter = JsonUserAdapter(fleet_controler, use_priority_criterion)
```

## pydantic benefits

Pydantic is a type checker library which allows to implement data models that check it's fields' type once one is trying to instanciate it. It allows also to implement fast custom validator over the model's field.

In H.A. designing it could be used to cast resources and inputs data to be sure that data are edible for the business logic. As our interfaces get methods return dictionaries, one just have to pass those dictionaries as pydantic data models parameters with a double splat operator (**).
