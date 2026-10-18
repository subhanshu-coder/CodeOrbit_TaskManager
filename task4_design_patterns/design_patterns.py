"""
Design Patterns Mini Project
CodeOrbit Tech Internship - Task 4

Three common design patterns, each demonstrated with a small working
example based on the Personal Task Manager idea:

    1. Singleton - one shared TaskStore for the whole program
    2. Factory   - TaskFactory builds different kinds of tasks
    3. Observer  - listeners get notified when a task changes

Run this file to see all three patterns in action:
    python3 design_patterns.py
"""


# =====================================================================
# PATTERN 1: SINGLETON
# ---------------------------------------------------------------------
# PROBLEM IT SOLVES:
#   Sometimes you must guarantee that only ONE object of a class exists.
#   If two parts of the program each created their own task list, they
#   would drift out of sync (one adds a task, the other never sees it).
#
# WHEN TO USE IT:
#   Shared resources such as a configuration object, a logger, a
#   database connection, or (here) the central task storage.
#
# HOW IT WORKS HERE:
#   __new__ is called before __init__ whenever an object is created.
#   We store the first instance in a class variable and return that same
#   instance on every later call.
# =====================================================================
class TaskStore:
    """Singleton: every TaskStore() call returns the SAME object."""

    _instance = None  # holds the one and only instance

    def __new__(cls):
        if cls._instance is None:
            # First time: actually create the object
            cls._instance = super().__new__(cls)
            cls._instance.tasks = []  # shared task list
        # Every other time: hand back the existing object
        return cls._instance

    def add(self, task):
        self.tasks.append(task)

    def all(self):
        return list(self.tasks)


# =====================================================================
# PATTERN 2: FACTORY
# ---------------------------------------------------------------------
# PROBLEM IT SOLVES:
#   Creating objects with "if kind == ..." scattered across the code
#   gets messy. If you add a new task type later, you would have to
#   edit code in many places.
#
# WHEN TO USE IT:
#   When the exact class to create depends on some input (a string, a
#   setting, a menu choice) and you want ONE place that decides.
#
# HOW IT WORKS HERE:
#   TaskFactory.create() receives a kind ("regular" or "priority") and
#   returns the right object. Callers never write the class names.
# =====================================================================
class Task:
    """Base task type."""

    def __init__(self, description):
        self.description = description
        self.status = "Pending"

    def label(self):
        return f"[{self.status}] {self.description}"


class RegularTask(Task):
    """A normal task."""


class PriorityTask(Task):
    """An urgent task - its label is flagged so it stands out."""

    def label(self):
        return f"[{self.status}] (!) HIGH PRIORITY: {self.description}"


class TaskFactory:
    """Factory: decides which Task class to build."""

    _kinds = {
        "regular": RegularTask,
        "priority": PriorityTask,
    }

    @staticmethod
    def create(kind, description):
        task_class = TaskFactory._kinds.get(kind.lower())
        if task_class is None:
            raise ValueError(f"Unknown task kind: {kind!r}")
        return task_class(description)


# =====================================================================
# PATTERN 3: OBSERVER
# ---------------------------------------------------------------------
# PROBLEM IT SOLVES:
#   When something happens (a task is completed), several other parts of
#   the program may care (logging, statistics, notifications). Hard-
#   coding calls to each one makes the main code messy and tightly
#   coupled.
#
# WHEN TO USE IT:
#   Event systems, notifications, UI updates - anywhere one object
#   changes and many others should react without the first object
#   knowing who they are.
#
# HOW IT WORKS HERE:
#   TaskNotifier (the "subject") keeps a list of observers. Calling
#   notify() tells each one about the event. Observers can be added or
#   removed freely without touching TaskNotifier's code.
# =====================================================================
class TaskNotifier:
    """Subject: tracks observers and tells them when events happen."""

    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify(self, event, task):
        for observer in self._observers:
            observer.update(event, task)


class ConsoleLogger:
    """Observer 1: prints every event."""

    def update(self, event, task):
        print(f"   [LOG] {event}: {task.description}")


class CompletionCounter:
    """Observer 2: counts how many tasks were completed."""

    def __init__(self):
        self.count = 0

    def update(self, event, task):
        if event == "completed":
            self.count += 1


# =====================================================================
# DEMO - run this file to see everything working together
# =====================================================================
def main():
    print("=== 1. SINGLETON ===")
    store_a = TaskStore()
    store_b = TaskStore()
    print("Same object?", store_a is store_b)  # True
    store_a.add(TaskFactory.create("regular", "Buy groceries"))
    print("store_b sees the task added via store_a:", len(store_b.all()), "task(s)")

    print("\n=== 2. FACTORY ===")
    t1 = TaskFactory.create("regular", "Read a chapter")
    t2 = TaskFactory.create("priority", "Submit internship report")
    print(t1.label())
    print(t2.label())
    try:
        TaskFactory.create("banana", "Invalid kind")
    except ValueError as err:
        print("Error handled:", err)

    print("\n=== 3. OBSERVER ===")
    notifier = TaskNotifier()
    logger = ConsoleLogger()
    counter = CompletionCounter()
    notifier.subscribe(logger)
    notifier.subscribe(counter)

    notifier.notify("added", t1)
    notifier.notify("completed", t1)
    notifier.notify("completed", t2)
    print("Tasks completed (counted by observer):", counter.count)

    notifier.unsubscribe(logger)
    print("Logger unsubscribed - this event prints no [LOG] line:")
    notifier.notify("added", t2)


if __name__ == "__main__":
    main()
