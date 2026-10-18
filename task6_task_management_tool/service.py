"""
LOGIC layer - the rules of the application (create, read, update, delete).
It never prints or asks for input, and it does not know HOW data is stored.
That separation is what makes it easy to test and to reuse.
"""

from models import Task, VALID_PRIORITIES, VALID_STATUSES


class TaskNotFoundError(Exception):
    """Raised when no task has the requested id."""


class TaskService:
    """Implements CRUD operations on top of any storage object."""

    def __init__(self, storage):
        self._storage = storage
        self._tasks = storage.load()

    # ---------- helpers ----------
    def _next_id(self):
        """New id = highest existing id + 1 (ids of deleted tasks in the middle are not reused)."""
        return max((t.id for t in self._tasks), default=0) + 1

    def _save(self):
        self._storage.save(self._tasks)

    @staticmethod
    def _check_priority(priority):
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {VALID_PRIORITIES}.")

    @staticmethod
    def _check_status(status):
        if status not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}.")

    # ---------- CREATE ----------
    def create(self, title, description="", priority="Medium"):
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        self._check_priority(priority)
        task = Task(id=self._next_id(), title=title,
                    description=description.strip(), priority=priority)
        self._tasks.append(task)
        self._save()
        return task

    # ---------- READ ----------
    def get_all(self, status=None):
        """Return all tasks, or only those with the given status."""
        if status is None:
            return list(self._tasks)
        self._check_status(status)
        return [t for t in self._tasks if t.status == status]

    def get(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"No task with id {task_id}.")

    # ---------- UPDATE ----------
    def update(self, task_id, title=None, description=None,
               priority=None, status=None):
        """Change any of the given fields; fields left as None are kept."""
        task = self.get(task_id)
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Title cannot be empty.")
            task.title = title
        if description is not None:
            task.description = description.strip()
        if priority is not None:
            self._check_priority(priority)
            task.priority = priority
        if status is not None:
            self._check_status(status)
            task.status = status
        self._save()
        return task

    # ---------- DELETE ----------
    def delete(self, task_id):
        task = self.get(task_id)
        self._tasks.remove(task)
        self._save()
        return task
