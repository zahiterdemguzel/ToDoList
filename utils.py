import json
import os
from PyQt5.QtCore import QTime


def saveTasks(tasks, filename="tasks.json"):
    for task in tasks:
        task["dueTime"] = task["dueTime"].toString(
            "HH:mm"
        )  # Convert QTime to string before saving
    with open(filename, "w") as file:
        json.dump(tasks, file, indent=4)
        print("Tasks saved.")


def loadTasks(filename="tasks.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            tasks = json.load(file)
            for task in tasks:
                task["dueTime"] = QTime.fromString(
                    task["dueTime"], "HH:mm"
                )  # Convert string to QTime after loading
            print("Tasks loading.")
            return tasks
    print("No tasks found.")
    return []
