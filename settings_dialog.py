from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFormLayout,
    QCheckBox,
    QSpinBox,
    QTabWidget,
    QWidget,
    QColorDialog,
    QFrame,
    QLabel,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from configuration_manager import ConfigurationManager


class SettingsDialog(QDialog):
    def __init__(self, configManager, parent=None):
        super().__init__(parent)
        self.configManager = configManager
        self.setWindowTitle("Settings")
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowCloseButtonHint
        )  # Hide the close button
        self.initUI()
        self.loadSettings()  # Load settings when initializing the UI

    def initUI(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.initTaskListTab()
        self.tabs.addTab(self.taskListTab, "Task List")

        layout.addWidget(self.tabs)

        buttonLayout = QHBoxLayout()
        self.okButton = QPushButton("Ok", self)
        self.cancelButton = QPushButton("Cancel", self)
        self.applyButton = QPushButton("Apply", self)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.applyButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        self.okButton.clicked.connect(self.applyAndAccept)
        self.cancelButton.clicked.connect(self.reject)
        self.applyButton.clicked.connect(self.applySettings)

    def initTaskListTab(self):
        self.taskListTab = QWidget()
        taskListLayout = QVBoxLayout()

        layout = QVBoxLayout()

        self.enableSidePanelCheck = QCheckBox("Enable side panel")
        self.enableSidePanelCheck.setChecked(
            self.configManager.get("enableSidePanel", False)
        )

        self.highlightDeadlineCheck = QCheckBox("Highlight deadline when near")
        self.highlightDeadlineCheck.stateChanged.connect(self.toggleDayRange)
        self.dayRangeSpin = QSpinBox()
        self.dayRangeSpin.setMinimum(1)
        self.dayRangeSpin.setMaximum(30)

        highlightLayout = QHBoxLayout()
        highlightLayout.addWidget(self.highlightDeadlineCheck)
        highlightLayout.addWidget(QLabel("Day range:"))
        highlightLayout.addWidget(self.dayRangeSpin)

        visibilityFrame = QFrame()
        visibilityFrame.setFrameShape(QFrame.StyledPanel)
        visibilityLayout = QVBoxLayout()

        self.dueDateCheck = QCheckBox("Due Date Visibility")
        self.dueTimeCheck = QCheckBox("Due Time Visibility")
        self.categoryCheck = QCheckBox("Category Visibility")
        self.priorityCheck = QCheckBox("Priority Visibility")

        visibilityLayout.addWidget(self.dueDateCheck)
        visibilityLayout.addWidget(self.dueTimeCheck)
        visibilityLayout.addWidget(self.categoryCheck)
        visibilityLayout.addWidget(self.priorityCheck)
        visibilityFrame.setLayout(visibilityLayout)

        colorFrame = QFrame()
        colorFrame.setFrameShape(QFrame.StyledPanel)
        colorLayout = QFormLayout()

        self.lowPriorityColorLabel = QLabel()
        self.lowColorButton = QPushButton("Low")
        self.lowColorButton.clicked.connect(lambda: self.pickColor("lowPriorityColor"))
        self.updateColorLabel(
            self.lowPriorityColorLabel,
            self.configManager.get("lowPriorityColor", "#99FF99"),
        )

        self.mediumPriorityColorLabel = QLabel()
        self.mediumColorButton = QPushButton("Medium")
        self.mediumColorButton.clicked.connect(
            lambda: self.pickColor("mediumPriorityColor")
        )
        self.updateColorLabel(
            self.mediumPriorityColorLabel,
            self.configManager.get("mediumPriorityColor", "#FFFF99"),
        )

        self.highPriorityColorLabel = QLabel()
        self.highColorButton = QPushButton("High")
        self.highColorButton.clicked.connect(
            lambda: self.pickColor("highPriorityColor")
        )
        self.updateColorLabel(
            self.highPriorityColorLabel,
            self.configManager.get("highPriorityColor", "#FF9999"),
        )

        colorLayout.addRow(self.lowColorButton, self.lowPriorityColorLabel)
        colorLayout.addRow(self.mediumColorButton, self.mediumPriorityColorLabel)
        colorLayout.addRow(self.highColorButton, self.highPriorityColorLabel)
        colorFrame.setLayout(colorLayout)

        layout.addWidget(self.enableSidePanelCheck)  # Add the new checkbox
        layout.addLayout(highlightLayout)
        layout.addWidget(visibilityFrame)
        layout.addWidget(colorFrame)

        taskListLayout.addLayout(layout)
        self.taskListTab.setLayout(taskListLayout)

    def toggleDayRange(self, state):
        self.dayRangeSpin.setEnabled(state == Qt.Checked)

    def pickColor(self, key):
        initialColor = QColor(self.configManager.get(key, "#FFFFFF"))
        color = QColorDialog.getColor(initialColor, self, "Select Color")
        if color.isValid():
            self.configManager.set(key, color.name())
            self.updateColorLabel(getattr(self, f"{key}Label"), color.name())

    def updateColorLabel(self, label, color):
        palette = label.palette()
        palette.setColor(QPalette.Window, QColor(color))
        label.setAutoFillBackground(True)
        label.setPalette(palette)
        label.setText(color)

    def applySettings(self):
        self.configManager.set("enableSidePanel", self.enableSidePanelCheck.isChecked())
        self.configManager.set(
            "highlightDeadline", self.highlightDeadlineCheck.isChecked()
        )
        self.configManager.set("dayRange", self.dayRangeSpin.value())
        self.configManager.set("dueDateVisibility", self.dueDateCheck.isChecked())
        self.configManager.set("dueTimeVisibility", self.dueTimeCheck.isChecked())
        self.configManager.set("categoryVisibility", self.categoryCheck.isChecked())
        self.configManager.set("priorityVisibility", self.priorityCheck.isChecked())
        self.configManager.saveConfig()  # Ensure settings are saved

    def loadSettings(self):
        self.enableSidePanelCheck.setChecked(
            self.configManager.get("enableSidePanel", False)
        )
        self.highlightDeadlineCheck.setChecked(
            self.configManager.get("highlightDeadline", False)
        )
        self.dayRangeSpin.setValue(self.configManager.get("dayRange", 1))
        self.dayRangeSpin.setEnabled(self.highlightDeadlineCheck.isChecked())
        self.dueDateCheck.setChecked(self.configManager.get("dueDateVisibility", True))
        self.dueTimeCheck.setChecked(self.configManager.get("dueTimeVisibility", True))
        self.categoryCheck.setChecked(
            self.configManager.get("categoryVisibility", True)
        )
        self.priorityCheck.setChecked(
            self.configManager.get("priorityVisibility", True)
        )

    def applyAndAccept(self):
        self.applySettings()
        self.accept()


# if main
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SettingsDialog(ConfigurationManager("test_config.json"))
    window.show()
    sys.exit(app.exec_())
