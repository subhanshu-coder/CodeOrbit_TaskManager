"""
DATA layer - the only file that knows tasks are saved in a JSON file.
To switch to a database later, only this file would need to change.
"""

import json
import os

from models import Task


class JsonStorage:
    """Loads and saves a list of Task objects to a JSON file."""

    def __init__(self, path="tasks_data.json"):
        self.path = path

    def load(self):
        """Return a list of Tasks; an empty list if the file is missing or damaged."""
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r") as f:
                raw = json.load(f)
            return [Task.from_dict(item) for item in raw]
        except (json.JSONDecodeError, OSError, TypeError):
            return []

    def save(self, tasks):
        """Write all tasks to the JSON file."""
        with open(self.path, "w") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2)
