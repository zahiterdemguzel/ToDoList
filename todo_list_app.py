from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QComboBox,
    QLabel,
    QDialog,
)
from PyQt5.QtCore import QTimer
from task_manager import TaskManager
from task_dialog import TaskDialog
from filter_sort_manager import FilterSortManager
from PyQt5.QtCore import Qt


class ToDoListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Initialize TaskManager and FilterSortManager after UI components
        self.taskManager = TaskManager(self.taskList)
        self.filterSortManager = FilterSortManager(
            self.taskList, self.filterComboBox, self.sortComboBox
        )

        try:
            self.taskManager.loadTasks()
        except Exception as e:
            print(e)

    def initUI(self):
        self.setWindowTitle("To-Do List Application")
        self.setGeometry(300, 300, 700, 600)

        self.layout = QVBoxLayout()

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

        self.markCompleteButton = QPushButton("Mark as Completed", self)
        self.markCompleteButton.clicked.connect(self.markAsCompleted)
        self.buttonLayout.addWidget(self.markCompleteButton)

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

        self.layout.addLayout(self.buttonLayout)

        self.taskList = QListWidget(self)
        self.taskList.itemDoubleClicked.connect(
            self.editTask
        )  # Connect double-click event to editTask method
        self.layout.addWidget(self.taskList)

        self.setLayout(self.layout)

        # Set up filter and sort manager after creating combo boxes
        self.filterSortManager = FilterSortManager(
            self.taskList, self.filterComboBox, self.sortComboBox
        )

        # Connect combo boxes to their respective functions
        self.filterComboBox.currentIndexChanged.connect(
            self.filterSortManager.filterTasks
        )
        self.sortComboBox.currentIndexChanged.connect(self.filterSortManager.sortTasks)

        # Set up timer for auto-saving tasks every 60 seconds
        # self.saveTimer = QTimer(self)
        # self.saveTimer.timeout.connect(self.taskManager.saveTasks)
        # self.saveTimer.start(60000)

    def showAddTaskDialog(self):
        dialog = TaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            taskData = dialog.getTaskData()
            if taskData["taskText"]:
                self.taskManager.addTask(
                    taskData["taskText"],
                    taskData["description"],
                    taskData["dueDate"],
                    taskData["priority"],
                    taskData["completed"],
                )
                self.filterSortManager.sortTasks()

    def editTask(self, item=None):
        selectedItem = item if item else self.taskList.currentItem()
        if selectedItem:
            taskData = selectedItem.data(Qt.UserRole)
            dialog = TaskDialog(self, taskData)
            if dialog.exec_() == QDialog.Accepted:
                updatedTaskData = dialog.getTaskData()
                self.taskManager.editTask(selectedItem, updatedTaskData)
                self.filterSortManager.sortTasks()

    def deleteTask(self):
        selectedItem = self.taskList.currentItem()
        if selectedItem:
            self.taskManager.deleteTask(selectedItem)

    def markAsCompleted(self):
        selectedItem = self.taskList.currentItem()
        if selectedItem:
            self.taskManager.markAsCompleted(selectedItem)
            self.filterSortManager.sortTasks()
