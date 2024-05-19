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
    def __init__(self, taskText, dueDate, priority, completed, description=""):
        super().__init__()

        # Set padding for the widget
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(
            10, 10, 10, 10
        )  # Add padding around the entire widget
        self.layout.setSpacing(15)

        self.headerLayout = QHBoxLayout()

        # Checkbox to mark task as completed
        self.completedCheckbox = QCheckBox()
        self.completedCheckbox.setChecked(completed)
        self.completedCheckbox.stateChanged.connect(self.onCheckboxStateChanged)

        # Reduce checkbox size
        self.completedCheckbox.setFixedSize(20, 20)

        self.taskLabel = QLabel(taskText)
        taskFont = self.taskLabel.font()
        taskFont.setBold(True)
        self.taskLabel.setFont(taskFont)

        self.dueDateLabel = QLabel(f"Due: {dueDate}")
        self.priorityLabel = QLabel(f"Priority: {priority}")

        # Increase tooltip font size
        if description:
            QToolTip.setFont(QFont("SansSerif", 12))
            self.setToolTip(description)

        if completed:
            self.applyStrikeThrough()

        # Adjust spacing between checkbox and text
        self.headerLayout.addWidget(self.completedCheckbox)
        self.headerLayout.addSpacing(5)  # Add a small space between checkbox and text

        # Align the task label to the left
        self.headerLayout.addWidget(self.taskLabel)
        self.headerLayout.addWidget(self.dueDateLabel)
        self.headerLayout.addWidget(self.priorityLabel)

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

    def removeStrikeThrough(self):
        def removeStrike(label):
            font = label.font()
            font.setStrikeOut(False)
            label.setFont(font)

        removeStrike(self.taskLabel)
        removeStrike(self.dueDateLabel)
        removeStrike(self.priorityLabel)

    def onCheckboxStateChanged(self, state):
        if state == Qt.Checked:
            self.applyStrikeThrough()
        else:
            self.removeStrikeThrough()
