"""
INTERFACE layer - everything the user sees and types.
It only talks to TaskService; it never touches files or business rules.
"""

from models import VALID_PRIORITIES, VALID_STATUSES
from service import TaskNotFoundError


def print_menu():
    print("\n===== TASK MANAGEMENT TOOL =====")
    print("1. Create Task")
    print("2. List Tasks")
    print("3. View Task Details")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Exit")
    print("================================")


def ask_int(prompt):
    """Ask for a whole number; return None if the input is not one."""
    raw = input(prompt).strip()
    if not raw.isdigit():
        print("Please enter a valid number.")
        return None
    return int(raw)


def ask_choice(prompt, options, default=None):
    """Ask the user to pick one of `options`; Enter keeps/uses the default."""
    raw = input(f"{prompt} {list(options)}"
                f"{' (Enter to skip)' if default is None else f' [default {default}]'}: ").strip()
    if not raw:
        return default
    for option in options:
        if option.lower() == raw.lower():
            return option
    print(f"Invalid choice. Please use one of {list(options)}.")
    return "INVALID"


def show_task_line(task):
    print(f"#{task.id} [{task.status}] ({task.priority}) {task.title}")


def create_task(service):
    title = input("Title: ")
    description = input("Description (optional): ")
    priority = ask_choice("Priority", VALID_PRIORITIES, default="Medium")
    if priority == "INVALID":
        return
    try:
        task = service.create(title, description, priority)
        print(f"Created task #{task.id}.")
    except ValueError as err:
        print(f"Error: {err}")


def list_tasks(service):
    tasks = service.get_all()
    if not tasks:
        print("No tasks yet.")
        return
    print("\n--- All Tasks ---")
    for task in tasks:
        show_task_line(task)


def view_task(service):
    task_id = ask_int("Task id: ")
    if task_id is None:
        return
    try:
        task = service.get(task_id)
    except TaskNotFoundError as err:
        print(f"Error: {err}")
        return
    print(f"\nTask #{task.id}")
    print(f"  Title:       {task.title}")
    print(f"  Description: {task.description or '-'}")
    print(f"  Priority:    {task.priority}")
    print(f"  Status:      {task.status}")
    print(f"  Created:     {task.created_at}")


def update_task(service):
    task_id = ask_int("Task id to update: ")
    if task_id is None:
        return
    try:
        service.get(task_id)  # make sure it exists before asking questions
    except TaskNotFoundError as err:
        print(f"Error: {err}")
        return

    print("Press Enter to keep a field unchanged.")
    title = input("New title: ") or None
    description = input("New description: ") or None
    priority = ask_choice("New priority", VALID_PRIORITIES)
    status = ask_choice("New status", VALID_STATUSES)
    if "INVALID" in (priority, status):
        return
    try:
        service.update(task_id, title, description, priority, status)
        print(f"Updated task #{task_id}.")
    except ValueError as err:
        print(f"Error: {err}")


def delete_task(service):
    task_id = ask_int("Task id to delete: ")
    if task_id is None:
        return
    try:
        task = service.delete(task_id)
        print(f"Deleted task #{task.id}: {task.title}")
    except TaskNotFoundError as err:
        print(f"Error: {err}")


def run(service):
    """Main menu loop."""
    actions = {
        "1": create_task,
        "2": list_tasks,
        "3": view_task,
        "4": update_task,
        "5": delete_task,
    }
    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()
        if choice == "6":
            print("Goodbye! Your tasks have been saved.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please enter a number from 1 to 6.")
        else:
            action(service)
