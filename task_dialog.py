from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QDateEdit,
    QTimeEdit,  # Import QTimeEdit
    QComboBox,
    QHBoxLayout,
    QPushButton,
)
from PyQt5.QtCore import QDate


class TaskDialog(QDialog):
    def __init__(self, parent=None, taskData=None):
        super().__init__(parent)
        self.setWindowTitle("Add Task" if taskData is None else "Edit Task")
        self.initUI(taskData)

    def initUI(self, taskData):
        formLayout = QFormLayout()
        self.taskInput = QLineEdit(self)
        self.descriptionInput = QTextEdit(self)
        self.dueDateEdit = QDateEdit(QDate.currentDate(), self)
        self.dueDateEdit.setCalendarPopup(True)
        self.dueTimeEdit = QTimeEdit(self)  # Add time input
        self.priorityComboBox = QComboBox(self)
        self.priorityComboBox.addItems(["Low", "Medium", "High"])
        self.categoryInput = QLineEdit(self)  # Add category input

        if taskData:
            self.taskInput.setText(taskData["taskText"])
            self.descriptionInput.setText(taskData["description"])
            self.dueDateEdit.setDate(
                QDate.fromString(taskData["dueDate"], "yyyy-MM-dd")
            )
            self.dueTimeEdit.setTime(taskData["dueTime"])  # Set time if available
            self.priorityComboBox.setCurrentText(taskData["priority"])
            self.categoryInput.setText(
                taskData["category"]
            )  # Set category if available
            self.completedCheckbox = QComboBox(self)
            self.completedCheckbox.addItems(["Not Completed", "Completed"])
            self.completedCheckbox.setCurrentText(
                "Completed" if taskData["completed"] else "Not Completed"
            )
            formLayout.addRow("Status:", self.completedCheckbox)

        formLayout.addRow("Task:", self.taskInput)
        formLayout.addRow("Description:", self.descriptionInput)
        formLayout.addRow("Due Date:", self.dueDateEdit)
        formLayout.addRow("Due Time:", self.dueTimeEdit)  # Add to form layout
        formLayout.addRow("Priority:", self.priorityComboBox)
        formLayout.addRow("Category:", self.categoryInput)  # Add to form layout

        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add" if taskData is None else "Save", self)
        self.cancelButton = QPushButton("Cancel", self)
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.cancelButton)
        formLayout.addRow(buttonLayout)

        self.setLayout(formLayout)

        self.addButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def getTaskData(self):
        taskData = {
            "taskText": self.taskInput.text(),
            "description": self.descriptionInput.toPlainText(),
            "dueDate": self.dueDateEdit.date().toString("yyyy-MM-dd"),
            "dueTime": self.dueTimeEdit.time(),  # Include time
            "priority": self.priorityComboBox.currentText(),
            "category": self.categoryInput.text(),  # Include category
        }
        if hasattr(self, "completedCheckbox"):
            taskData["completed"] = self.completedCheckbox.currentText() == "Completed"
        else:
            taskData["completed"] = False
        return taskData
