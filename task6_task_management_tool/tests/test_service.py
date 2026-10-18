"""Unit tests for the logic layer (service.py) - run from the project folder:
    python3 -m unittest discover -s tests -t . -v
"""

import os
import tempfile
import unittest

from service import TaskNotFoundError, TaskService
from storage import JsonStorage


class TestTaskService(unittest.TestCase):

    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)
        self.service = TaskService(JsonStorage(self.path))

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    # CREATE
    def test_create_assigns_incrementing_ids(self):
        a = self.service.create("A")
        b = self.service.create("B")
        self.assertEqual((a.id, b.id), (1, 2))

    def test_create_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.service.create("   ")

    def test_create_invalid_priority_rejected(self):
        with self.assertRaises(ValueError):
            self.service.create("A", priority="Urgent")

    # READ
    def test_get_all_and_filter_by_status(self):
        t = self.service.create("A")
        self.service.create("B")
        self.service.update(t.id, status="Completed")
        self.assertEqual(len(self.service.get_all()), 2)
        self.assertEqual(len(self.service.get_all("Completed")), 1)

    def test_get_missing_task_raises(self):
        with self.assertRaises(TaskNotFoundError):
            self.service.get(99)

    # UPDATE
    def test_update_changes_only_given_fields(self):
        t = self.service.create("Old", "desc", "Low")
        self.service.update(t.id, title="New")
        updated = self.service.get(t.id)
        self.assertEqual((updated.title, updated.description, updated.priority),
                         ("New", "desc", "Low"))

    def test_update_invalid_status_rejected(self):
        t = self.service.create("A")
        with self.assertRaises(ValueError):
            self.service.update(t.id, status="Done-ish")

    # DELETE
    def test_delete_removes_task(self):
        a = self.service.create("A")
        self.service.delete(a.id)
        with self.assertRaises(TaskNotFoundError):
            self.service.get(a.id)

    def test_new_id_is_highest_plus_one_after_middle_delete(self):
        a = self.service.create("A")
        self.service.create("B")
        self.service.delete(a.id)          # delete id 1, id 2 remains
        c = self.service.create("C")
        self.assertEqual(c.id, 3)          # not 1, so ids never collide

    # PERSISTENCE
    def test_data_survives_restart(self):
        self.service.create("Persistent")
        reloaded = TaskService(JsonStorage(self.path))
        self.assertEqual(reloaded.get_all()[0].title, "Persistent")


if __name__ == "__main__":
    unittest.main()
