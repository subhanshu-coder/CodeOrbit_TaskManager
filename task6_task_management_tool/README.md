# Task Management Tool

A command-line tool to manage tasks with full CRUD (Create, Read, Update, Delete),
built for the CodeOrbit Tech Software Development Internship (Task 6).

## Features

- **Create** a task with a title, optional description and priority (Low / Medium / High)
- **Read** all tasks, or view one task's full details
- **Update** any field: title, description, priority, status (Pending / In Progress / Completed)
- **Delete** a task by id
- Tasks are saved to `tasks_data.json` and reloaded on the next run
- Every input is validated; mistakes show a message instead of crashing

## Project Structure (three layers)

```
task_management_tool/
├── main.py        Entry point - connects the layers and starts the app
├── cli.py         INTERFACE layer - menus, prompts, printing
├── service.py     LOGIC layer - CRUD rules and validation
├── storage.py     DATA layer - reads/writes the JSON file
├── models.py      DATA MODEL - the Task definition
├── tests/
│   └── test_service.py   Unit tests for the logic layer
└── README.md
```

Why separate layers? Each file has one job. The logic layer never prints or reads
files, so it can be tested on its own, and storage could be swapped for a database
without touching the menu or the rules.

## Setup and Usage

Requires Python 3.8+ only. No packages to install.

```
python3 main.py
```

Choose options 1-6 from the menu. To run the tests:

```
python3 -m unittest discover -s tests -t . -v
```

## Version Control

Developed with Git using small, meaningful commits (see the repository history).
