import json
from datetime import datetime

FILE_NAME = "tasks.json"

import os

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    
    try:
        with open(FILE_NAME, "r") as file:
            data = file.read().strip()
            return json.loads(data) if data else []
    except json.JSONDecodeError:
        print("Ошибка: файл tasks.json поврежден. Сбрасываю задачи.")
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)
def add_task(description):
    tasks = load_tasks()
    task_id = max([task['id'] for task in tasks], default=0) + 1
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")
def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print("Task not found.")
def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task['id'] != task_id]
    if len(tasks) == len(updated_tasks):
        print("Task not found.")
    else:
        save_tasks(updated_tasks)
        print(f"Task {task_id} deleted successfully.")
def mark_task(task_id, status):
    if status not in ["in-progress", "done"]:
        print("Invalid status.")
        return
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print("Task not found.")
def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status:
        tasks = [task for task in tasks if task['status'] == filter_status]

    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print(f"ID: {task['id']} | {task['description']} | Status: {task['status']} | Created At: {task['createdAt']} | Updated At: {task['updatedAt']}")
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1].lower()

    if command == "add" and len(sys.argv) == 3:
        add_task(sys.argv[2])
    elif command == "update" and len(sys.argv) == 4:
        update_task(int(sys.argv[2]), sys.argv[3])
    elif command == "delete" and len(sys.argv) == 3:
        delete_task(int(sys.argv[2]))
    elif command == "mark-in-progress" and len(sys.argv) == 3:
        mark_task(int(sys.argv[2]), "in-progress")
    elif command == "mark-done" and len(sys.argv) == 3:
        mark_task(int(sys.argv[2]), "done")
    elif command == "list":
        list_tasks(sys.argv[2].lower() if len(sys.argv) == 3 else None)
    else:
        print("Invalid command or arguments.")

if __name__ == "__main__":
    main()
