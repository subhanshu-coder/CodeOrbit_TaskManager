"""
Entry point - connects the three layers together and starts the app.

    interface (cli.py)  ->  logic (service.py)  ->  data (storage.py + models.py)

Run with:  python3 main.py
"""

from cli import run
from service import TaskService
from storage import JsonStorage


def main():
    storage = JsonStorage("tasks_data.json")  # data layer
    service = TaskService(storage)            # logic layer
    run(service)                              # interface layer


if __name__ == "__main__":
    main()
