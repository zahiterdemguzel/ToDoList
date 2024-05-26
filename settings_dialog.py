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
    DEFAULTS = {
        "enableSidePanel": True,
        "enableDoubleClick": True,
        "highlightDeadline": False,
        "dayRange": 1,
        "dueDateVisibility": True,
        "dueTimeVisibility": True,
        "categoryVisibility": True,
        "priorityVisibility": True,
        "lowPriorityColor": "#99FF99",
        "mediumPriorityColor": "#FFFF99",
        "highPriorityColor": "#FF9999",
    }

    def __init__(self, configManager, parent=None):
        super().__init__(parent)
        self.configManager = configManager
        self.setWindowTitle("Settings")
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
        self.resetButton = QPushButton("Reset", self)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.resetButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        self.okButton.clicked.connect(self.applyAndAccept)
        self.cancelButton.clicked.connect(self.reject)
        self.applyButton.clicked.connect(self.applySettings)
        self.resetButton.clicked.connect(self.resetToDefaults)

    def initTaskListTab(self):
        self.taskListTab = QWidget()
        taskListLayout = QVBoxLayout()

        layout = QVBoxLayout()

        self.enableSidePanelCheck = QCheckBox("Enable side panel")
        self.enableSidePanelCheck.setChecked(
            self.configManager.get("enableSidePanel", self.DEFAULTS["enableSidePanel"])
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

        self.enableDoubleClickCheck = QCheckBox("Enable double click")
        self.enableDoubleClickCheck.setChecked(
            self.configManager.get(
                "enableDoubleClick", self.DEFAULTS["enableDoubleClick"]
            )
        )

        visibilityFrame = QFrame()
        visibilityFrame.setFrameShape(QFrame.StyledPanel)
        visibilityLayout = QVBoxLayout()

        self.dueDateCheck = QCheckBox("Due Date Visibility")
        self.dueDateCheck.setChecked(
            self.configManager.get(
                "dueDateVisibility", self.DEFAULTS["dueDateVisibility"]
            )
        )
        self.dueTimeCheck = QCheckBox("Due Time Visibility")
        self.dueTimeCheck.setChecked(
            self.configManager.get(
                "dueTimeVisibility", self.DEFAULTS["dueTimeVisibility"]
            )
        )
        self.categoryCheck = QCheckBox("Category Visibility")
        self.categoryCheck.setChecked(
            self.configManager.get(
                "categoryVisibility", self.DEFAULTS["categoryVisibility"]
            )
        )
        self.priorityCheck = QCheckBox("Priority Visibility")
        self.priorityCheck.setChecked(
            self.configManager.get(
                "priorityVisibility", self.DEFAULTS["priorityVisibility"]
            )
        )

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
            self.configManager.get(
                "lowPriorityColor", self.DEFAULTS["lowPriorityColor"]
            ),
        )

        self.mediumPriorityColorLabel = QLabel()
        self.mediumColorButton = QPushButton("Medium")
        self.mediumColorButton.clicked.connect(
            lambda: self.pickColor("mediumPriorityColor")
        )
        self.updateColorLabel(
            self.mediumPriorityColorLabel,
            self.configManager.get(
                "mediumPriorityColor", self.DEFAULTS["mediumPriorityColor"]
            ),
        )

        self.highPriorityColorLabel = QLabel()
        self.highColorButton = QPushButton("High")
        self.highColorButton.clicked.connect(
            lambda: self.pickColor("highPriorityColor")
        )
        self.updateColorLabel(
            self.highPriorityColorLabel,
            self.configManager.get(
                "highPriorityColor", self.DEFAULTS["highPriorityColor"]
            ),
        )

        colorLayout.addRow(self.lowColorButton, self.lowPriorityColorLabel)
        colorLayout.addRow(self.mediumColorButton, self.mediumPriorityColorLabel)
        colorLayout.addRow(self.highColorButton, self.highPriorityColorLabel)
        colorFrame.setLayout(colorLayout)

        layout.addWidget(self.enableSidePanelCheck)  # Add the new checkbox
        layout.addWidget(self.enableDoubleClickCheck)  # Add the double-click checkbox
        layout.addLayout(highlightLayout)
        layout.addWidget(visibilityFrame)
        layout.addWidget(colorFrame)

        taskListLayout.addLayout(layout)
        self.taskListTab.setLayout(taskListLayout)

    def toggleDayRange(self, state):
        self.dayRangeSpin.setEnabled(state == Qt.Checked)

    def pickColor(self, key):
        initialColor = QColor(self.configManager.get(key, self.DEFAULTS[key]))
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
        self.configManager.set(
            "enableDoubleClick", self.enableDoubleClickCheck.isChecked()
        )
        self.configManager.saveConfig()  # Ensure settings are saved

    def loadSettings(self):
        self.enableSidePanelCheck.setChecked(
            self.configManager.get("enableSidePanel", self.DEFAULTS["enableSidePanel"])
        )
        self.highlightDeadlineCheck.setChecked(
            self.configManager.get(
                "highlightDeadline", self.DEFAULTS["highlightDeadline"]
            )
        )
        self.dayRangeSpin.setValue(
            self.configManager.get("dayRange", self.DEFAULTS["dayRange"])
        )
        self.dayRangeSpin.setEnabled(self.highlightDeadlineCheck.isChecked())
        self.dueDateCheck.setChecked(
            self.configManager.get(
                "dueDateVisibility", self.DEFAULTS["dueDateVisibility"]
            )
        )
        self.dueTimeCheck.setChecked(
            self.configManager.get(
                "dueTimeVisibility", self.DEFAULTS["dueTimeVisibility"]
            )
        )
        self.categoryCheck.setChecked(
            self.configManager.get(
                "categoryVisibility", self.DEFAULTS["categoryVisibility"]
            )
        )
        self.priorityCheck.setChecked(
            self.configManager.get(
                "priorityVisibility", self.DEFAULTS["priorityVisibility"]
            )
        )
        self.enableDoubleClickCheck.setChecked(
            self.configManager.get(
                "enableDoubleClick", self.DEFAULTS["enableDoubleClick"]
            )
        )

    def resetToDefaults(self):
        self.enableSidePanelCheck.setChecked(self.DEFAULTS["enableSidePanel"])
        self.highlightDeadlineCheck.setChecked(self.DEFAULTS["highlightDeadline"])
        self.dayRangeSpin.setValue(self.DEFAULTS["dayRange"])
        self.dueDateCheck.setChecked(self.DEFAULTS["dueDateVisibility"])
        self.dueTimeCheck.setChecked(self.DEFAULTS["dueTimeVisibility"])
        self.categoryCheck.setChecked(self.DEFAULTS["categoryVisibility"])
        self.priorityCheck.setChecked(self.DEFAULTS["priorityVisibility"])
        self.enableDoubleClickCheck.setChecked(self.DEFAULTS["enableDoubleClick"])
        self.updateColorLabel(
            self.lowPriorityColorLabel, self.DEFAULTS["lowPriorityColor"]
        )
        self.updateColorLabel(
            self.mediumPriorityColorLabel, self.DEFAULTS["mediumPriorityColor"]
        )
        self.updateColorLabel(
            self.highPriorityColorLabel, self.DEFAULTS["highPriorityColor"]
        )

    def applyAndAccept(self):
        self.applySettings()
        self.accept()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SettingsDialog(ConfigurationManager("test_config.json"))
    window.show()
    sys.exit(app.exec_())
