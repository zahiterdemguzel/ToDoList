from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QDateEdit,
    QTimeEdit,
    QComboBox,
    QPushButton,
    QFrame,
)
from PyQt5.QtCore import QDate, Qt


class TaskDetailPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.hide()  # Initially hidden

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.headerLayout = QHBoxLayout()
        self.deselectButton = QPushButton(">")
        self.deselectButton.setFixedSize(35, 35)
        self.deselectButton.clicked.connect(self.deselectTask)

        deselectButtonLayout = QHBoxLayout()
        deselectButtonLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        deselectButtonLayout.addWidget(self.deselectButton)

        self.headerLayout.addLayout(deselectButtonLayout)
        self.layout.addLayout(self.headerLayout)

        self.formLayout = QVBoxLayout()

        self.taskInput = QLineEdit()
        self.formLayout.addWidget(self.createFormItem("Title:", self.taskInput))

        self.descriptionInput = QTextEdit()
        self.formLayout.addWidget(
            self.createFormItem("Description:", self.descriptionInput, vertical=True)
        )

        self.dueDateEdit = QDateEdit(QDate.currentDate())
        self.dueDateEdit.setCalendarPopup(True)
        self.formLayout.addWidget(self.createFormItem("Due Date:", self.dueDateEdit))

        self.dueTimeEdit = QTimeEdit()
        self.formLayout.addWidget(self.createFormItem("Due Time:", self.dueTimeEdit))

        self.priorityComboBox = QComboBox()
        self.priorityComboBox.addItems(["Low", "Medium", "High"])
        self.formLayout.addWidget(
            self.createFormItem("Priority:", self.priorityComboBox)
        )

        self.categoryInput = QLineEdit()
        self.formLayout.addWidget(self.createFormItem("Category:", self.categoryInput))

        self.completedComboBox = QComboBox()
        self.completedComboBox.addItems(["Not Completed", "Completed"])
        self.formLayout.addWidget(
            self.createFormItem("Status:", self.completedComboBox)
        )

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveTask)
        self.formLayout.addWidget(self.saveButton)

        self.layout.addLayout(self.formLayout)

        # Add a frame to visually separate the form from other elements
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.separator)

        self.setLayout(self.layout)

    def createFormItem(self, label, widget, vertical=False):
        if not vertical:
            layout = QHBoxLayout()
        else:
            layout = QVBoxLayout()
        layout.addWidget(QLabel(label))
        layout.addWidget(widget)
        formItem = QWidget()
        formItem.setLayout(layout)
        return formItem

    def loadTask(self, taskData):
        self.taskInput.setText(taskData["title"])
        self.descriptionInput.setText(taskData["description"])
        self.dueDateEdit.setDate(QDate.fromString(taskData["dueDate"], "yyyy-MM-dd"))
        self.dueTimeEdit.setTime(taskData["dueTime"])
        self.priorityComboBox.setCurrentText(taskData["priority"])
        self.categoryInput.setText(taskData["category"])
        self.completedComboBox.setCurrentText(
            "Completed" if taskData["completed"] else "Not Completed"
        )
        self.show()  # Show panel when task is loaded

    def saveTask(self):
        taskData = {
            "title": self.taskInput.text(),
            "description": self.descriptionInput.toPlainText(),
            "dueDate": self.dueDateEdit.date().toString("yyyy-MM-dd"),
            "dueTime": self.dueTimeEdit.time(),
            "priority": self.priorityComboBox.currentText(),
            "category": self.categoryInput.text(),
            "completed": self.completedComboBox.currentText() == "Completed",
        }
        self.parent().updateSelectedTask(taskData)

    def deselectTask(self):
        self.hide()
        self.parent().deselectCurrentTask()
