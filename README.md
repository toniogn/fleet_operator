# Fleet Operator

## Introduction

Fleet operator is a demonstration project to illustrate and practice hexagonal architecture designing. The business logic purpose is to simulate usage scenarios on an EV vehicles fleet depending on a sorting criterion used to decide if a vehicle of the fleet must be used or charged at some point.

## About Hexagonal Architecture (H.A.)

![hexagonal architecture scheme](https://blog.octo.com/wp-content/uploads/2020/06/archi_hexa_06-1024x526.png)

H.A. is a designing pattern which aims to uncouple the business logic (the hexagon) from the user and the server sides. Practically its realized thanks to interface design pattern which allows to reverse server side dependency and weaken both sides coupling defining generic methods and rules to get and parse user inputs and resources data. For more information see [hexagonal architecture by octo](https://blog.octo.com/architecture-hexagonale-trois-principes-et-un-exemple-dimplementation/).

## Practicing

The root folder contains two child folders. One containing a classical M.V.C. version (without explicit view) of the source code to refactor with an H.A. and the other to explore a refactored solution. There is multiple ways to do it, the proposed refactoring may not be the best one.

## Installation

Start a terminal and switch to your local repositories folder
Clone the repository with `git clone https://github.com/toniogn/fleet_operator.git`.
Create a dedicated virtual environment with `–m venv your_venv_name`.
Activate it with `your_venv_name/Scripts/activate`.
Install dependencies with `pip install –r requirements.txt`.

## Repository content

```
-> scripts: contains useful scripts
-----> generate_fleet_json.py: generate resources data
-----> generate_inputs_json.py: generate inputs data
-----> main_to_refactor.py: main file to practice refactoring on
-----> main_refactored.py: main file for the refactored solution
-> src: contains source codes
-----> fleet_operator_refactored: contains an H.A. refactored solution
---------> data
-------------> inputs.json: inputs data generated in generate_scenario_json
-------------> fleet.json: resources data generated in generate_fleet_json
---------> utils
-------------> criterions.py: contains sorting functions to decide which vehicle to send for a given task
-------------> data_models.py: contains pydantic classes defining data types at both interfaces and output
-------------> utils.py: contains custom exceptions and a class gathering physics constants
---------> core.py: contains the business logic and its controler
---------> input.py: contains user-side interface and inheriting adapters
---------> resources.py: contains server-side interface and inheriting adapters
-----> fleet_operator_to_refactor: contains the source code to practice refactoring on
---------> data
---------> core.py
---------> criterions.py
---------> utils.py
-> .gitignore
-> README.md
-> requirements.txt
```

## To refactor software functioning
