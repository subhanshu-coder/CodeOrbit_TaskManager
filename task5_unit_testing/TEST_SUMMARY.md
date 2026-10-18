# Unit Testing Summary

**Module tested:** `task_manager.py` (Personal Task Manager CLI, Task 2)
**Framework:** Python `unittest` (built-in, no installation needed)
**Test file:** `test_task_manager.py`

## Results

| Metric | Value |
|---|---|
| Total tests | 32 |
| Passed | 32 |
| Failed | 0 |
| Line coverage of function bodies | 100% (89 of 89 lines) |

Coverage was measured with Python's standard-library `trace` module.

## What is covered

| Function | Normal cases | Edge cases |
|---|---|---|
| `load_tasks` / `save_tasks` | save then load round trip | missing file, corrupted JSON, unwritable path |
| `add_task` | valid task, saved to disk | empty input, spaces only, extra whitespace trimmed |
| `view_tasks` | shows numbered list with status | empty list |
| `get_valid_task_id` | first and last valid number | 0, too high, negative, letters, empty, no tasks |
| `complete_task` / `delete_task` | correct task changed or removed | invalid or out-of-range input changes nothing |
| `search_task` | finds match | case-insensitive, no match, empty keyword |
| `print_menu` / `main` | full add-view-complete-search-delete-exit workflow, loads saved tasks | invalid menu choices |

## Technique notes

- A temporary file replaces `tasks.json` in every test, so real data is never touched.
- `unittest.mock.patch` fakes keyboard `input()` and captures `print()` output, which lets
  interactive functions be tested automatically.

## How to run

```
python3 -m unittest -v test_task_manager.py
```
