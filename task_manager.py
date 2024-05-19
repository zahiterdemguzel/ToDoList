from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from task_item_widget import TaskItemWidget
from utils import saveTasks, loadTasks


class TaskManager:
    def __init__(self, taskList):
        self.taskList = taskList

    def addTask(self, taskText, description, dueDate, priority, completed=False):
        item = QListWidgetItem()
        widget = TaskItemWidget(taskText, dueDate, priority, completed, description)
        item.setSizeHint(widget.sizeHint())
        item.setData(
            Qt.UserRole,
            {
                "taskText": taskText,
                "dueDate": dueDate,
                "priority": priority,
                "completed": completed,
                "description": description,
            },
        )
        self.taskList.addItem(item)
        self.taskList.setItemWidget(item, widget)
        self.setItemColor(item, priority)
        self.saveTasks()

        # Connect checkbox state change to update task completion status
        widget.completedCheckbox.stateChanged.connect(
            lambda state, item=item: self.updateTaskCompletion(item, state)
        )

    def editTask(self, selectedItem, taskData):
        selectedItem.setData(Qt.UserRole, taskData)
        widget = TaskItemWidget(
            taskData["taskText"],
            taskData["dueDate"],
            taskData["priority"],
            taskData["completed"],
            taskData["description"],
        )
        selectedItem.setSizeHint(widget.sizeHint())
        self.taskList.setItemWidget(selectedItem, widget)
        self.setItemColor(selectedItem, taskData["priority"])
        self.saveTasks()

        # Connect checkbox state change to update task completion status
        widget.completedCheckbox.stateChanged.connect(
            lambda state, item=selectedItem: self.updateTaskCompletion(item, state)
        )

    def deleteTask(self, selectedItem):
        self.taskList.takeItem(self.taskList.row(selectedItem))
        self.saveTasks()

    def markAsCompleted(self, selectedItem):
        taskData = selectedItem.data(Qt.UserRole)
        taskData["completed"] = not taskData["completed"]
        selectedItem.setData(Qt.UserRole, taskData)
        widget = TaskItemWidget(
            taskData["taskText"],
            taskData["dueDate"],
            taskData["priority"],
            taskData["completed"],
            taskData["description"],
        )
        selectedItem.setSizeHint(widget.sizeHint())
        self.taskList.setItemWidget(selectedItem, widget)
        self.setItemColor(selectedItem, taskData["priority"])
        self.saveTasks()

        # Connect checkbox state change to update task completion status
        widget.completedCheckbox.stateChanged.connect(
            lambda state, item=selectedItem: self.updateTaskCompletion(item, state)
        )

    def updateTaskCompletion(self, item, state):
        taskData = item.data(Qt.UserRole)
        taskData["completed"] = state == Qt.Checked
        item.setData(Qt.UserRole, taskData)
        self.saveTasks()

    def setItemColor(self, item, priority):
        if priority == "High":
            item.setBackground(QColor(255, 153, 153))  # Pastel red
        elif priority == "Medium":
            item.setBackground(QColor(255, 255, 153))  # Pastel yellow
        elif priority == "Low":
            item.setBackground(QColor(153, 255, 153))  # Pastel green

    def saveTasks(self):
        tasks = []
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            taskData = item.data(Qt.UserRole)
            tasks.append(taskData)
        saveTasks(tasks)

    def loadTasks(self):
        tasks = loadTasks()
        for taskData in tasks:
            item = QListWidgetItem()
            widget = TaskItemWidget(
                taskData["taskText"],
                taskData["dueDate"],
                taskData["priority"],
                taskData["completed"],
                taskData["description"],
            )
            item.setSizeHint(widget.sizeHint())
            item.setData(Qt.UserRole, taskData)
            self.taskList.addItem(item)
            self.taskList.setItemWidget(item, widget)
            self.setItemColor(item, taskData["priority"])

            # Connect checkbox state change to update task completion status
            widget.completedCheckbox.stateChanged.connect(
                lambda state, item=item: self.updateTaskCompletion(item, state)
            )
