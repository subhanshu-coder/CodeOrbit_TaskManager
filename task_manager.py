"""
Personal Task Manager - CLI Application
CodeOrbit Tech Internship - Task 2: Simple CLI-Based Application

A simple command-line task manager that lets a user add, view,
complete, delete, and search tasks. Tasks persist between runs
using a local JSON file (tasks.json).

Requirements covered (see SRS document for full details):
FR-1: Add a new task
FR-2: View all tasks with status
FR-3: Mark a task as completed
FR-4: Delete a task
FR-5: Validate all input; never crash on bad input
FR-6: Exit safely at any time
"""

import json  
# //json module is used to read and write task data in JSON format
import os

DATA_FILE = "tasks.json" 
# //task data will be stored in this file


def load_tasks(): 
    # //load tasks from the JSON file if it exists, otherwise start empty.
    """Load tasks from the JSON file if it exists, otherwise start empty."""
    if os.path.exists(DATA_FILE):
        # //data file exists, try to read it
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: could not read saved tasks. Starting with an empty list.")
            return []
    return []


def save_tasks(tasks):
    # """Save the current task list to the JSON file.""" 
    # //save the current task list to the JSON file
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(tasks, f, indent=2)
    except IOError:
        print("Warning: could not save tasks to disk.")


def print_menu():
    # """Display the main menu options to the user."""
    # //display the main menu options to the user
    print("\n===== PERSONAL TASK MANAGER =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task Complete")
    print("4. Delete Task")
    print("5. Search Task")
    print("6. Exit")
    print("==================================")


def add_task(tasks):
    """Prompt the user for a task description and add it as 'Pending'."""
    description = input("Enter task description: ").strip()
    if not description:
        print("Task description cannot be empty. Task not added.")
        return
    tasks.append({"description": description, "status": "Pending"})
    save_tasks(tasks)
    print(f"Task added: \"{description}\"")


def view_tasks(tasks):
    """Display all tasks with their index and status."""
    if not tasks:
        print("No tasks yet. Add one from the menu!")
        return
    print("\n--- Your Tasks ---")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. [{task['status']}] {task['description']}")


def get_valid_task_id(tasks):
    """
    Ask the user for a task number and validate it.
    Returns a zero-based index, or None if the input was invalid.
    """
    if not tasks:
        print("There are no tasks to select.")
        return None

    raw = input(f"Enter task number (1-{len(tasks)}): ").strip()
    if not raw.isdigit():
        print("Please enter a valid number.")
        return None

    index = int(raw) - 1
    if index < 0 or index >= len(tasks):
        print("Task number out of range.")
        return None

    return index


def complete_task(tasks):
    """Mark a chosen task as completed."""
    view_tasks(tasks)
    index = get_valid_task_id(tasks)
    if index is None:
        return
    tasks[index]["status"] = "Completed"
    save_tasks(tasks)
    print(f"Marked as complete: \"{tasks[index]['description']}\"")


def delete_task(tasks):
    """Delete a chosen task from the list."""
    view_tasks(tasks)
    index = get_valid_task_id(tasks)
    if index is None:
        return
    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Deleted task: \"{removed['description']}\"")


def search_task(tasks):
    """Search tasks by a keyword in their description (case-insensitive)."""
    keyword = input("Enter a keyword to search: ").strip().lower()
    if not keyword:
        print("Search keyword cannot be empty.")
        return

    matches = [t for t in tasks if keyword in t["description"].lower()]
    if not matches:
        print(f"No tasks found matching \"{keyword}\".")
        return

    print(f"\n--- Tasks matching \"{keyword}\" ---")
    for i, task in enumerate(matches, start=1):
        print(f"{i}. [{task['status']}] {task['description']}")


def main():
    """Main program loop: shows the menu and routes to the right action."""
    tasks = load_tasks()

    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            search_task(tasks)
        elif choice == "6":
            print("Goodbye! Your tasks have been saved.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
