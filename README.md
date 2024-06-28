# AirBnB Clone | Console Project

This project is the first step towards building a full-fledged AirBnB clone application. It implements a command-line interpreter (CLI) to manage core AirBnB objects.


### Project Overview

The project focuses on:

* **Object-Oriented Programming:** Building a `BaseModel` class with functionalities for object initialization, serialization (converting to JSON), and deserialization (reconstructing from JSON).

* **Data Management:** Creating specific classes for AirBnB entities like User, State, City, and Place, inheriting from `BaseModel`. Implementing a file-based storage engine using JSON files.

* **Testing:** Writing unit tests to ensure the correctness of each class and the storage engine.

* **User Interaction:** Designing a user-friendly CLI for object creation, retrieval, and updates.


### Getting Started

**Prerequisites:**

* Python 3 (tested with version 3.x)
* `json` library (`pip install json`)
* `unittest` library (for testing) (`pip install unittest`)
* `cmd` library (for CLI) (`pip install cmd`)
* `uuid` library (for objects id's) (`pip install uuid`)
* 'datetime' library (for creation and update date and time) (`pip install datetime`)

**Project Structure:**

```
AirBnB_clone/
├── AUTHORS		# Project contributors
├── README.md		# This file
├── __init__.py		# Package initialization
├── console.py		# Main script for running the CLI
├── models		# Holds all class definitions for AirBnB entities
│   ├── __init__.py
│   ├── amenity.py
│   ├── base_model.py	# BaseModel class the parent class for all the AirBnB model 
│   ├── city.py
│   ├── engine		# Storage Engine Directory
│   │   ├── __init__.py
│   │   └── file_storage.py	# Implements functions for storing and retrieving objects using JSON files
│   ├── place.py
│   ├── review.py
│   ├── state.py
│   └── user.py
├── requirements.txt	# Required libraries for the project
└── tests		# Unit Tests for all components
    ├── __init__.py
    ├── test_console.py
    └── test_models
        ├── __init__.py
        ├── test_amenity.py
        ├── test_base_model.py
        ├── test_city.py
        ├── test_engine
        │   ├── __init__.py
        │   └── test_file_storage.py
        ├── test_place.py
        ├── test_review.py
        ├── test_state.py
        └── test_user.py

5 directories, 27 files
```

**Running the Project:**

1. Clone this repository.

2. Install required libraries:
```bash
$ pip install -r requirements.txt
```

3. Run the program:
```bash
$ python3 console.py
```
Another way:
```bash
$ ./console.py
```
in non-interactive mode:
```bash
$ echo "command" | ./console.py
```

4. Follow the on-screen instructions to interact with the CLI.



to be continued...
