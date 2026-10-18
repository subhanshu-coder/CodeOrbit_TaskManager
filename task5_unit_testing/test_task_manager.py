"""
Unit Testing Practice
CodeOrbit Tech Internship - Task 5

Tests for task_manager.py (the CLI app from Task 2), using Python's
built-in unittest framework.

Techniques used:
  - A temporary file replaces tasks.json so real data is never touched.
  - unittest.mock.patch fakes keyboard input() and captures print()
    output, so functions that talk to the user can be tested automatically.

Run all tests:
    python3 -m unittest -v test_task_manager.py
"""

import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

import task_manager


class TaskManagerTestCase(unittest.TestCase):
    """Base class: points DATA_FILE at a throwaway temp file for each test."""

    def setUp(self):
        fd, self.temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.temp_path)  # start with "file does not exist"
        self.original_path = task_manager.DATA_FILE
        task_manager.DATA_FILE = self.temp_path

    def tearDown(self):
        task_manager.DATA_FILE = self.original_path
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    @staticmethod
    def run_with_input(func, tasks, *typed_inputs):
        """Call func(tasks) with fake typed input; return everything printed."""
        with patch("builtins.input", side_effect=list(typed_inputs)):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                func(tasks)
        return fake_out.getvalue()


# ---------------------------------------------------------------------
# load_tasks / save_tasks
# ---------------------------------------------------------------------
class TestSaveAndLoad(TaskManagerTestCase):

    def test_load_returns_empty_list_when_no_file(self):  # edge case
        self.assertEqual(task_manager.load_tasks(), [])

    def test_save_then_load_round_trip(self):  # normal case
        tasks = [{"description": "Study", "status": "Pending"}]
        task_manager.save_tasks(tasks)
        self.assertEqual(task_manager.load_tasks(), tasks)

    def test_load_handles_corrupted_file(self):  # edge case
        with open(self.temp_path, "w") as f:
            f.write("{ this is not valid json")
        with patch("sys.stdout", new=StringIO()):
            self.assertEqual(task_manager.load_tasks(), [])


# ---------------------------------------------------------------------
# add_task
# ---------------------------------------------------------------------
class TestAddTask(TaskManagerTestCase):

    def test_add_valid_task(self):  # normal case
        tasks = []
        self.run_with_input(task_manager.add_task, tasks, "Buy milk")
        self.assertEqual(tasks, [{"description": "Buy milk", "status": "Pending"}])

    def test_add_task_strips_whitespace(self):  # edge case
        tasks = []
        self.run_with_input(task_manager.add_task, tasks, "   Clean room   ")
        self.assertEqual(tasks[0]["description"], "Clean room")

    def test_add_empty_task_is_rejected(self):  # edge case
        tasks = []
        output = self.run_with_input(task_manager.add_task, tasks, "")
        self.assertEqual(tasks, [])
        self.assertIn("cannot be empty", output)

    def test_add_spaces_only_is_rejected(self):  # edge case
        tasks = []
        self.run_with_input(task_manager.add_task, tasks, "     ")
        self.assertEqual(tasks, [])

    def test_add_task_is_saved_to_disk(self):  # normal case
        tasks = []
        self.run_with_input(task_manager.add_task, tasks, "Persist me")
        self.assertEqual(task_manager.load_tasks()[0]["description"], "Persist me")


# ---------------------------------------------------------------------
# view_tasks
# ---------------------------------------------------------------------
class TestViewTasks(TaskManagerTestCase):

    def test_view_empty_list(self):  # edge case
        output = self.run_with_input(task_manager.view_tasks, [])
        self.assertIn("No tasks yet", output)

    def test_view_shows_status_and_description(self):  # normal case
        tasks = [
            {"description": "Task A", "status": "Pending"},
            {"description": "Task B", "status": "Completed"},
        ]
        output = self.run_with_input(task_manager.view_tasks, tasks)
        self.assertIn("1. [Pending] Task A", output)
        self.assertIn("2. [Completed] Task B", output)


# ---------------------------------------------------------------------
# get_valid_task_id (input validation)
# ---------------------------------------------------------------------
class TestGetValidTaskId(TaskManagerTestCase):

    def setUp(self):
        super().setUp()
        self.tasks = [
            {"description": "One", "status": "Pending"},
            {"description": "Two", "status": "Pending"},
        ]

    def pick(self, typed):
        with patch("builtins.input", return_value=typed):
            with patch("sys.stdout", new=StringIO()):
                return task_manager.get_valid_task_id(self.tasks)

    def test_valid_first_number(self):  # normal case
        self.assertEqual(self.pick("1"), 0)

    def test_valid_last_number(self):  # boundary
        self.assertEqual(self.pick("2"), 1)

    def test_zero_is_rejected(self):  # boundary
        self.assertIsNone(self.pick("0"))

    def test_number_too_high_is_rejected(self):  # boundary
        self.assertIsNone(self.pick("3"))

    def test_negative_number_is_rejected(self):  # edge case
        self.assertIsNone(self.pick("-1"))

    def test_letters_are_rejected(self):  # edge case
        self.assertIsNone(self.pick("abc"))

    def test_empty_input_is_rejected(self):  # edge case
        self.assertIsNone(self.pick(""))

    def test_no_tasks_available(self):  # edge case
        with patch("sys.stdout", new=StringIO()):
            self.assertIsNone(task_manager.get_valid_task_id([]))


# ---------------------------------------------------------------------
# complete_task / delete_task
# ---------------------------------------------------------------------
class TestCompleteAndDelete(TaskManagerTestCase):

    def make_tasks(self):
        return [
            {"description": "First", "status": "Pending"},
            {"description": "Second", "status": "Pending"},
        ]

    def test_complete_task_changes_status(self):  # normal case
        tasks = self.make_tasks()
        self.run_with_input(task_manager.complete_task, tasks, "1")
        self.assertEqual(tasks[0]["status"], "Completed")
        self.assertEqual(tasks[1]["status"], "Pending")  # untouched

    def test_complete_with_invalid_input_changes_nothing(self):  # edge case
        tasks = self.make_tasks()
        self.run_with_input(task_manager.complete_task, tasks, "xyz")
        self.assertEqual(tasks, self.make_tasks())

    def test_delete_task_removes_correct_one(self):  # normal case
        tasks = self.make_tasks()
        self.run_with_input(task_manager.delete_task, tasks, "1")
        self.assertEqual([t["description"] for t in tasks], ["Second"])

    def test_delete_out_of_range_changes_nothing(self):  # edge case
        tasks = self.make_tasks()
        self.run_with_input(task_manager.delete_task, tasks, "99")
        self.assertEqual(len(tasks), 2)


# ---------------------------------------------------------------------
# search_task
# ---------------------------------------------------------------------
class TestSearchTask(TaskManagerTestCase):

    def setUp(self):
        super().setUp()
        self.tasks = [
            {"description": "Buy Groceries", "status": "Pending"},
            {"description": "Write report", "status": "Completed"},
        ]

    def test_search_finds_match(self):  # normal case
        output = self.run_with_input(task_manager.search_task, self.tasks, "report")
        self.assertIn("Write report", output)
        self.assertNotIn("Buy Groceries", output)

    def test_search_is_case_insensitive(self):  # edge case
        output = self.run_with_input(task_manager.search_task, self.tasks, "GROCERIES")
        self.assertIn("Buy Groceries", output)

    def test_search_no_match(self):  # edge case
        output = self.run_with_input(task_manager.search_task, self.tasks, "zzz")
        self.assertIn("No tasks found", output)

    def test_search_empty_keyword_rejected(self):  # edge case
        output = self.run_with_input(task_manager.search_task, self.tasks, "")
        self.assertIn("cannot be empty", output)


# ---------------------------------------------------------------------
# print_menu, save error handling, and the main() loop
# ---------------------------------------------------------------------
class TestMenuAndMainLoop(TaskManagerTestCase):

    def run_main(self, *typed_inputs):
        """Run main() with fake typed input and return everything printed."""
        with patch("builtins.input", side_effect=list(typed_inputs)):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                task_manager.main()
        return fake_out.getvalue()

    def test_print_menu_shows_all_six_options(self):  # normal case
        with patch("sys.stdout", new=StringIO()) as fake_out:
            task_manager.print_menu()
        for text in ["Add Task", "View Tasks", "Mark Task Complete",
                     "Delete Task", "Search Task", "Exit"]:
            self.assertIn(text, fake_out.getvalue())

    def test_save_tasks_handles_unwritable_path(self):  # edge case
        # A directory cannot be opened as a file, so saving must fail safely.
        task_manager.DATA_FILE = tempfile.gettempdir()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            task_manager.save_tasks([{"description": "x", "status": "Pending"}])
        self.assertIn("could not save", fake_out.getvalue())

    def test_main_exit_immediately(self):  # normal case
        self.assertIn("Goodbye", self.run_main("6"))

    def test_main_invalid_choice_then_exit(self):  # edge case
        output = self.run_main("9", "abc", "6")
        self.assertEqual(output.count("Invalid choice"), 2)
        self.assertIn("Goodbye", output)

    def test_main_full_workflow(self):  # normal case: add, view, complete, search, delete
        output = self.run_main(
            "1", "Write tests",   # add
            "2",                  # view
            "3", "1",             # complete task 1
            "5", "write",         # search
            "4", "1",             # delete task 1
            "6",                  # exit
        )
        self.assertIn("Task added", output)
        self.assertIn("Marked as complete", output)
        self.assertIn("Deleted task", output)
        self.assertIn("Goodbye", output)

    def test_main_loads_previously_saved_tasks(self):  # normal case
        task_manager.save_tasks([{"description": "From last time", "status": "Pending"}])
        self.assertIn("From last time", self.run_main("2", "6"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
