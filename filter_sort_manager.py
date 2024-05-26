import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem
from task_item_widget import TaskItemWidget
from task_manager import TaskManager
from configuration_manager import ConfigurationManager


class FilterSortManager:
    def __init__(
        self,
        taskList,
        filterComboBox,
        sortComboBox,
        taskManager,
        searchBar,
        configManager,
    ):
        self.taskList = taskList
        self.filterComboBox = filterComboBox
        self.sortComboBox = sortComboBox
        self.taskManager = taskManager
        self.searchBar = searchBar
        self.configManager = configManager

        # Load configuration
        self.loadConfig()

    def filterTasks(self):
        filterText = self.filterComboBox.currentText()
        searchText = self.searchBar.text().lower()
        print(f"Filtering tasks with filter: {filterText} and searching: {searchText}")

        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            taskData = item.data(Qt.UserRole)

            title = taskData["title"].lower()
            description = taskData["description"].lower()
            tag = taskData["category"].lower()

            if searchText in title or searchText in description or searchText in tag:
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
            else:
                item.setHidden(True)

    def sortTasks(self):
        sortText = self.sortComboBox.currentText()
        tasks = []
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            tasks.append((item, item.data(Qt.UserRole)))

        if sortText == "Sort by Name":
            tasks.sort(key=lambda x: x[1]["title"])
        elif sortText == "Sort by Date":
            tasks.sort(
                key=lambda x: (x[1]["dueDate"], x[1]["dueTime"].toString("HH:mm"))
            )  # Sort by date and time
        elif sortText == "Sort by Priority":
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            tasks.sort(key=lambda x: priority_order[x[1]["priority"]])

        self.taskList.clear()
        for item, taskData in tasks:
            newItem = QListWidgetItem()
            newItem.setData(Qt.UserRole, taskData)
            widget = TaskItemWidget(
                taskData["title"],
                taskData["dueDate"],
                taskData["dueTime"],  # Include dueTime
                taskData["priority"],
                taskData["category"],  # Include category
                taskData["completed"],
                taskData["description"],
                taskManager=self.taskManager,
                listItem=newItem,
            )
            newItem.setSizeHint(widget.sizeHint())
            self.taskList.addItem(newItem)
            self.taskList.setItemWidget(newItem, widget)
            TaskManager(self.taskList).setItemColor(newItem, taskData["priority"])

        self.filterTasks()  # Ensure tasks are filtered after sorting

    def sortAndFilterTasks(self):
        self.sortTasks()
        self.filterTasks()
        self.saveConfig()  # Save configuration whenever sorting or filtering is applied

    def saveConfig(self):
        self.configManager.set("filter", self.filterComboBox.currentText())
        self.configManager.set("sort", self.sortComboBox.currentText())
        # self.configManager.set("search", self.searchBar.text())

    def loadConfig(self):
        self.filterComboBox.setCurrentText(self.configManager.get("filter", "All"))
        self.sortComboBox.setCurrentText(self.configManager.get("sort", "Sort by Name"))
        # self.searchBar.setText(self.configManager.get("search", ""))
