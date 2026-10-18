# Design Patterns Mini Project

Three common design patterns implemented in `design_patterns.py`, each with a small
working example based on a task manager. Run it with `python3 design_patterns.py`.

| Pattern | Problem it solves | When to use it | Example here |
|---|---|---|---|
| **Singleton** | Two copies of a shared resource drift out of sync | Config, logger, database connection, shared data store | `TaskStore` - every `TaskStore()` returns the same object |
| **Factory** | `if kind == ...` object creation scattered across code | The class to create depends on input, and you want one place to decide | `TaskFactory.create("priority", ...)` returns the right Task class |
| **Observer** | Many parts must react to an event without the source knowing them | Notifications, logging, UI updates, event systems | `TaskNotifier` tells `ConsoleLogger` and `CompletionCounter` about changes |

The code is commented step by step to explain how each pattern works.
