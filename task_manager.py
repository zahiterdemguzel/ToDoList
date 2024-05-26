from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from task_item_widget import TaskItemWidget
from utils import saveTasks, loadTasks


class TaskManager:
    def __init__(self, taskList):
        self.taskList = taskList
        self.filterSortManager = None  # To be set by ToDoListApp

    def addTask(
        self,
        title,
        description,
        dueDate,
        dueTime,
        priority,
        category,
        completed=False,
    ):
        item = QListWidgetItem()
        widget = TaskItemWidget(
            title,
            dueDate,
            dueTime,
            priority,
            category,
            completed,
            description,
            taskManager=self,
            listItem=item,  # Ensure listItem is passed
        )
        item.setSizeHint(widget.sizeHint())
        item.setData(
            Qt.UserRole,
            {
                "title": title,
                "dueDate": dueDate,
                "dueTime": dueTime,
                "priority": priority,
                "category": category,
                "completed": completed,
                "description": description,
            },
        )
        self.taskList.addItem(item)
        self.taskList.setItemWidget(item, widget)
        self.setItemColor(item, priority)
        self.saveTasks()

    def editTask(self, selectedItem, taskData):
        selectedItem.setData(Qt.UserRole, taskData)
        widget = TaskItemWidget(
            taskData["title"],
            taskData["dueDate"],
            taskData["dueTime"],
            taskData["priority"],
            taskData["category"],
            taskData["completed"],
            taskData["description"],
            taskManager=self,
            listItem=selectedItem,  # Ensure listItem is passed
        )
        selectedItem.setSizeHint(widget.sizeHint())
        self.taskList.setItemWidget(selectedItem, widget)
        self.setItemColor(selectedItem, taskData["priority"])
        self.saveTasks()

    # deleteTask method
    def deleteTask(self, selectedItem):
        self.taskList.takeItem(self.taskList.row(selectedItem))
        self.saveTasks()

    def updateTaskCompletion(self, item, completed):
        print(f"Updating task completion: {completed}")
        taskData = item.data(Qt.UserRole)
        taskData["completed"] = completed
        item.setData(Qt.UserRole, taskData)

        # Update the widget for the task item
        widget = TaskItemWidget(
            taskData["title"],
            taskData["dueDate"],
            taskData["dueTime"],
            taskData["priority"],
            taskData["category"],
            taskData["completed"],
            taskData["description"],
            taskManager=self,
            listItem=item,
        )
        item.setSizeHint(widget.sizeHint())
        self.taskList.setItemWidget(item, widget)
        self.setItemColor(item, taskData["priority"])

        self.saveTasks()

        if self.filterSortManager:
            self.filterSortManager.sortAndFilterTasks()

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
                taskData["title"],
                taskData["dueDate"],
                taskData["dueTime"],
                taskData["priority"],
                taskData["category"],
                taskData["completed"],
                taskData["description"],
                taskManager=self,
                listItem=item,
            )
            item.setSizeHint(widget.sizeHint())
            item.setData(Qt.UserRole, taskData)
            self.taskList.addItem(item)
            self.taskList.setItemWidget(item, widget)
            self.setItemColor(item, taskData["priority"])

        if self.filterSortManager:
            self.filterSortManager.sortAndFilterTasks()
