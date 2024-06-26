from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QComboBox,
    QLabel,
    QDialog,
    QLineEdit,
)
from PyQt5.QtCore import QTimer, QSize
from task_manager import TaskManager
from task_dialog import TaskDialog
from filter_sort_manager import FilterSortManager
from PyQt5.QtCore import Qt
from configuration_manager import ConfigurationManager
from PyQt5.QtGui import QIcon

from settings_dialog import SettingsDialog  # Make sure to import the new dialog


# Add import for TaskDetailPanel
from task_detail_panel import TaskDetailPanel


class ToDoListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.configManager = ConfigurationManager()
        self.taskManager = TaskManager(self.taskList, self.configManager)
        self.filterSortManager = FilterSortManager(
            self.taskList,
            self.filterComboBox,
            self.sortComboBox,
            self.taskManager,
            self.searchBar,
            self.configManager,
        )
        self.taskManager.filterSortManager = self.filterSortManager

        try:
            self.taskManager.loadTasks()
            self.filterSortManager.sortAndFilterTasks()  # Sort and filter tasks initially
        except Exception as e:
            print(e)

    def initUI(self):
        self.setWindowTitle("To-Do List Application")
        self.setGeometry(300, 300, 900, 600)  # Adjust window size for the new panel

        self.layout = QHBoxLayout()  # Change main layout to horizontal
        self.mainLayout = QVBoxLayout()

        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search tasks...")
        self.mainLayout.addWidget(self.searchBar)

        self.buttonLayout = QHBoxLayout()

        self.addButton = QPushButton("Add Task", self)
        self.addButton.clicked.connect(self.showAddTaskDialog)
        self.buttonLayout.addWidget(self.addButton)

        self.editButton = QPushButton("Edit Task", self)
        self.editButton.clicked.connect(self.editTask)
        self.buttonLayout.addWidget(self.editButton)

        self.deleteButton = QPushButton("Delete Task", self)
        self.deleteButton.clicked.connect(self.deleteTask)
        self.buttonLayout.addWidget(self.deleteButton)

        self.filterComboBox = QComboBox(self)
        self.filterComboBox.addItems(
            ["All", "Completed", "Not Completed", "High Priority"]
        )
        self.buttonLayout.addWidget(QLabel("Filter:"))
        self.buttonLayout.addWidget(self.filterComboBox)

        self.sortComboBox = QComboBox(self)
        self.sortComboBox.addItems(["Sort by Name", "Sort by Date", "Sort by Priority"])
        self.buttonLayout.addWidget(QLabel("Sort:"))
        self.buttonLayout.addWidget(self.sortComboBox)

        self.settingsButton = QPushButton("", self)
        self.settingsButton.setIcon(QIcon("Resources/settings.png"))
        self.settingsButton.setFixedSize(
            35, 35
        )  # Set fixed size for the settings button
        self.buttonLayout.addWidget(self.settingsButton)
        self.settingsButton.clicked.connect(self.showSettingsDialog)

        self.mainLayout.addLayout(self.buttonLayout)

        self.taskList = QListWidget(self)
        self.taskList.itemClicked.connect(self.showTaskDetail)
        self.taskList.itemDoubleClicked.connect(self.editTask)

        self.mainLayout.addWidget(self.taskList)

        self.layout.addLayout(self.mainLayout)  # Add main layout to the left side

        self.taskDetailPanel = TaskDetailPanel(self)  # Create TaskDetailPanel
        self.taskDetailPanel.hide()  # Hide initially
        self.layout.addWidget(
            self.taskDetailPanel
        )  # Add TaskDetailPanel to the right side

        self.setLayout(self.layout)

        # Connect combo boxes to their respective functions
        self.filterComboBox.currentIndexChanged.connect(self.sortAndFilterTasks)
        self.sortComboBox.currentIndexChanged.connect(self.sortAndFilterTasks)

        # Connect the search bar to the search function
        self.searchBar.textChanged.connect(self.searchTasks)

    def showTaskDetail(self, item):
        taskData = item.data(Qt.UserRole)
        self.taskDetailPanel.loadTask(taskData)
        self.taskDetailPanel.show()  # Show panel when task is selected

    def updateSelectedTask(self, updatedTaskData):
        selectedItem = self.taskList.currentItem()
        if selectedItem:
            self.taskManager.editTask(selectedItem, updatedTaskData)
            self.filterSortManager.sortAndFilterTasks()

    def deselectCurrentTask(self):
        self.taskList.clearSelection()
        self.taskDetailPanel.hide()

    def showSettingsDialog(self):
        dialog = SettingsDialog(self.configManager, self)
        dialog.exec_()
        self.applySettings()  # Apply settings after dialog is closed
        # reload tasks
        self.filterSortManager.sortAndFilterTasks()

    def applySettings(self):
        # You can add your logic here to apply the settings to the application
        print("Settings applied")

    def sortAndFilterTasks(self):
        if hasattr(self, "filterSortManager"):
            self.filterSortManager.sortAndFilterTasks()

    def showAddTaskDialog(self):
        dialog = TaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            taskData = dialog.getTaskData()
            if taskData["title"]:
                self.taskManager.addTask(
                    taskData["title"],
                    taskData["description"],
                    taskData["dueDate"],
                    taskData["dueTime"],  # Include dueTime
                    taskData["priority"],
                    taskData["category"],  # Include category
                    taskData["completed"],
                )
                self.filterSortManager.sortAndFilterTasks()

    def editTask(self, item=None):
        selectedItem = item if item else self.taskList.currentItem()
        if selectedItem:
            taskData = selectedItem.data(Qt.UserRole)
            dialog = TaskDialog(self, taskData)
            if dialog.exec_() == QDialog.Accepted:
                updatedTaskData = dialog.getTaskData()
                self.taskManager.editTask(selectedItem, updatedTaskData)
                self.filterSortManager.sortAndFilterTasks()

    def deleteTask(self):
        selectedItem = self.taskList.currentItem()
        if selectedItem:
            self.taskManager.deleteTask(selectedItem)
            self.filterSortManager.sortAndFilterTasks()

    def searchTasks(self):
        searchText = self.searchBar.text().lower()
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            taskData = item.data(Qt.UserRole)
            title = taskData["title"].lower()
            description = taskData["description"].lower()
            if searchText in title or searchText in description:
                item.setHidden(False)
            else:
                item.setHidden(True)

        self.filterSortManager.sortAndFilterTasks()
