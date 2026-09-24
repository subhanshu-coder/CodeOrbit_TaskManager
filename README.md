# Personal Task Manager (CLI)

A simple command-line task manager built for the CodeOrbit Tech Software
Development Internship (Task 2: Simple CLI-Based Application).

This project implements the requirements defined in the accompanying
SRS document (Task 1) for a Personal Task Manager.

## Features

- Add a task
- View all tasks with their status (Pending / Completed)
- Mark a task as completed
- Delete a task
- Search tasks by keyword
- Exit safely at any time
- Tasks are saved to `tasks.json` so they persist between runs
- Input is validated throughout — invalid input never crashes the app

## How to Run

1. Make sure Python 3 is installed:
   ```
   python3 --version
   ```
2. Run the application:
   ```
   python3 task_manager.py
   ```
3. Follow the on-screen numbered menu (1–6).

## Files

- `task_manager.py` — the main application
- `tasks.json` — auto-created on first run to store your tasks
- `README.md` — this file

## Notes

This project was built as part of the CodeOrbit Tech internship program.
See `SRS_Personal_Task_Manager.docx` (Task 1) for the full requirements
this application was designed against.
