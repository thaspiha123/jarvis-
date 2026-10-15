import json
import os


TASK_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "memory",
    "tasks.json"
)


def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    os.makedirs(os.path.dirname(TASK_FILE), exist_ok=True)

    with open(TASK_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def add_task(title):
    tasks = load_tasks()

    tasks.insert(
        0,
        {
            "title": title,
            "done": False
        }
    )

    save_tasks(tasks)

    return f"Task added: {title}"


def list_tasks():
    tasks = load_tasks()

    if not tasks:
        return "You have no tasks."

    lines = ["Your tasks are:"]

    for index, task in enumerate(tasks):
        status = "completed" if task.get("done", False) else "pending"

        lines.append(
            f"{index + 1}. {task['title']} - {status}"
        )

    return "\n".join(lines)


def toggle_task(number):
    tasks = load_tasks()

    index = number - 1

    if index < 0 or index >= len(tasks):
        return "That task does not exist."

    tasks[index]["done"] = not tasks[index].get("done", False)

    save_tasks(tasks)

    if tasks[index]["done"]:
        return f"Task completed: {tasks[index]['title']}"

    return f"Task reopened: {tasks[index]['title']}"


def delete_task(number):
    tasks = load_tasks()

    index = number - 1

    if index < 0 or index >= len(tasks):
        return "That task does not exist."

    deleted = tasks.pop(index)

    save_tasks(tasks)

    return f"Task deleted: {deleted['title']}"