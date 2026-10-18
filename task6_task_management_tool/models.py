"""
DATA MODEL layer - describes what a Task looks like.
Contains no logic about storage or user interface.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime

VALID_PRIORITIES = ("Low", "Medium", "High")
VALID_STATUSES = ("Pending", "In Progress", "Completed")


@dataclass
class Task:
    """A single task with an id, title, optional description, priority and status."""
    id: int
    title: str
    description: str = ""
    priority: str = "Medium"
    status: str = "Pending"
    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    def to_dict(self):
        """Convert to a plain dictionary (used when saving to JSON)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Task from a dictionary (used when loading from JSON)."""
        return cls(**data)
