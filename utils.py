import json
import os


def saveTasks(tasks, filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump(tasks, file, indent=4)
        print("Tasks saved.")


def loadTasks(filename="tasks.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            print("Tasks loading.")
            return json.load(file)
    print("No tasks found.")
    return []
