from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QToolTip,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class TaskItemWidget(QWidget):
    def __init__(self, taskText, dueDate, priority, completed, description=""):
        super().__init__()

        # Set padding for the widget
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)  # Add more padding
        self.layout.setSpacing(10)

        self.headerLayout = QHBoxLayout()

        # Make the task label bold
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

        self.headerLayout.addWidget(self.taskLabel)
        self.headerLayout.addWidget(self.dueDateLabel)
        self.headerLayout.addWidget(self.priorityLabel)

        self.layout.addLayout(self.headerLayout)
        self.setLayout(self.layout)

        # Apply strike-through effect if the task is completed
        if completed:
            self.applyStrikeThrough()

    def applyStrikeThrough(self):
        def setStrikeThrough(label):
            font = label.font()
            font.setStrikeOut(True)
            label.setFont(font)

        setStrikeThrough(self.taskLabel)
        setStrikeThrough(self.dueDateLabel)
        setStrikeThrough(self.priorityLabel)
