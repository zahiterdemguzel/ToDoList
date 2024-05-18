from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem
from task_item_widget import TaskItemWidget
from task_manager import TaskManager


class FilterSortManager:
    def __init__(self, taskList, filterComboBox, sortComboBox):
        self.taskList = taskList
        self.filterComboBox = filterComboBox
        self.sortComboBox = sortComboBox

    def filterTasks(self):
        filterText = self.filterComboBox.currentText()
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            taskData = item.data(Qt.UserRole)
            if filterText == "All":
                item.setHidden(False)
            elif filterText == "Completed" and taskData["completed"]:
                item.setHidden(False)
            elif filterText == "Not Completed" and not taskData["completed"]:
                item.setHidden(False)
            elif filterText == "High Priority" and taskData["priority"] == "High":
                item.setHidden(False)
            else:
                item.setHidden(True)

    def sortTasks(self):
        sortText = self.sortComboBox.currentText()
        tasks = []
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            tasks.append((item, item.data(Qt.UserRole)))

        if sortText == "Sort by Name":
            tasks.sort(key=lambda x: x[1]["taskText"])
        elif sortText == "Sort by Date":
            tasks.sort(key=lambda x: x[1]["dueDate"])
        elif sortText == "Sort by Priority":
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            tasks.sort(key=lambda x: priority_order[x[1]["priority"]])

        self.taskList.clear()
        for item, taskData in tasks:
            newItem = QListWidgetItem()
            newItem.setData(Qt.UserRole, taskData)
            widget = TaskItemWidget(
                taskData["taskText"],
                taskData["dueDate"],
                taskData["priority"],
                taskData["completed"],
                taskData["description"],
            )
            newItem.setSizeHint(widget.sizeHint())
            self.taskList.addItem(newItem)
            self.taskList.setItemWidget(newItem, widget)
            TaskManager(self.taskList).setItemColor(newItem, taskData["priority"])
