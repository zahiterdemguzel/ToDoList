from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QToolTip,
    QCheckBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class TaskItemWidget(QWidget):
    def __init__(
        self,
        taskText,
        dueDate,
        dueTime,
        priority,
        category,
        completed,
        description="",
        taskManager=None,
        listItem=None,
    ):
        super().__init__()

        self.taskManager = taskManager
        self.listItem = listItem  # Ensure listItem is stored

        # Set padding for the widget
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.layout.setSpacing(15)

        self.headerLayout = QHBoxLayout()

        # Checkbox to mark task as completed
        self.completedCheckbox = QCheckBox()
        self.completedCheckbox.setChecked(completed)
        self.completedCheckbox.stateChanged.connect(self.onCheckboxStateChanged)

        # Reduce checkbox size
        self.completedCheckbox.setFixedSize(20, 20)
        self.completedCheckbox.setSizePolicy(
            QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        )

        self.taskLabel = QLabel(taskText)
        taskFont = self.taskLabel.font()
        taskFont.setBold(True)
        self.taskLabel.setFont(taskFont)
        timeText = (
            " - " + dueTime.toString("HH:mm")
            if dueTime.toString("HH:mm") != "00:00"
            else ""
        )

        self.dueDateLabel = QLabel(f"Due: {dueDate}{timeText}")
        self.priorityLabel = QLabel(f"Priority: {priority}")
        self.categoryLabel = QLabel(f"Category: {category}")

        # Increase tooltip font size
        if description:
            QToolTip.setFont(QFont("SansSerif", 12))
            self.setToolTip(description)

        if completed:
            self.applyStrikeThrough()

        # Adjust spacing between checkbox and text
        self.headerLayout.addWidget(self.completedCheckbox)
        self.headerLayout.addSpacing(5)

        self.headerLayout.addWidget(self.taskLabel)
        self.headerLayout.addWidget(self.dueDateLabel)
        self.headerLayout.addWidget(self.priorityLabel)
        self.headerLayout.addWidget(self.categoryLabel)

        self.layout.addLayout(self.headerLayout)
        self.setLayout(self.layout)

    def applyStrikeThrough(self):
        def setStrikeThrough(label):
            font = label.font()
            font.setStrikeOut(True)
            label.setFont(font)

        setStrikeThrough(self.taskLabel)
        setStrikeThrough(self.dueDateLabel)
        setStrikeThrough(self.priorityLabel)
        setStrikeThrough(self.categoryLabel)

    def removeStrikeThrough(self):
        def removeStrike(label):
            font = label.font()
            font.setStrikeOut(False)
            label.setFont(font)

        removeStrike(self.taskLabel)
        removeStrike(self.dueDateLabel)
        removeStrike(self.priorityLabel)
        removeStrike(self.categoryLabel)

    def onCheckboxStateChanged(self, state):
        if state == Qt.Checked:
            self.applyStrikeThrough()
        else:
            self.removeStrikeThrough()

        # Ensure listItem reference is used correctly
        if self.listItem is not None:
            self.taskManager.updateTaskCompletion(self.listItem, state == Qt.Checked)
        else:
            print("No reference to list item found")
