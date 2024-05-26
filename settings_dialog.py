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
    QListWidget,
    QListWidgetItem,
    QComboBox,
    QLineEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from configuration_manager import ConfigurationManager


class SettingsDialog(QDialog):
    DEFAULTS = {
        "enableSidePanel": True,
        "highlightDeadline": False,
        "dayRange": 1,
        "dueDateVisibility": True,
        "dueTimeVisibility": True,
        "categoryVisibility": True,
        "priorityVisibility": True,
        "enableDoubleClick": True,
        "lowPriorityColor": "#99FF99",
        "mediumPriorityColor": "#FFFF99",
        "highPriorityColor": "#FF9999",
        "enableNotifications": False,
        "remindHighPriority": False,
        "remindMediumPriority": False,
        "remindLowPriority": False,
        "notificationOffsets": [],
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

        self.initNotificationsTab()
        self.tabs.addTab(self.notificationsTab, "Notifications")

        layout.addWidget(self.tabs)

        buttonLayout = QHBoxLayout()
        self.okButton = QPushButton("Ok", self)
        self.cancelButton = QPushButton("Cancel", self)
        self.resetButton = QPushButton("Reset", self)
        self.resetButton.setFixedWidth(60)  # Make the reset button smaller

        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.resetButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        self.okButton.clicked.connect(self.applyAndAccept)
        self.cancelButton.clicked.connect(self.reject)
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

    def initNotificationsTab(self):
        self.notificationsTab = QWidget()
        notificationsLayout = QVBoxLayout()

        self.enableNotificationsCheck = QCheckBox("Enable Notifications")
        self.enableNotificationsCheck.setChecked(
            self.configManager.get(
                "enableNotifications", self.DEFAULTS["enableNotifications"]
            )
        )
        self.enableNotificationsCheck.stateChanged.connect(
            self.toggleNotificationsFrame
        )

        self.notificationsFrame = QFrame()
        self.notificationsFrame.setFrameShape(QFrame.StyledPanel)
        notificationsFrameLayout = QVBoxLayout()

        remindLayout = QHBoxLayout()
        self.remindHighPriorityCheck = QCheckBox("Remind High Priority")
        self.remindHighPriorityCheck.setChecked(
            self.configManager.get(
                "remindHighPriority", self.DEFAULTS["remindHighPriority"]
            )
        )
        self.remindMediumPriorityCheck = QCheckBox("Remind Medium Priority")
        self.remindMediumPriorityCheck.setChecked(
            self.configManager.get(
                "remindMediumPriority", self.DEFAULTS["remindMediumPriority"]
            )
        )
        self.remindLowPriorityCheck = QCheckBox("Remind Low Priority")
        self.remindLowPriorityCheck.setChecked(
            self.configManager.get(
                "remindLowPriority", self.DEFAULTS["remindLowPriority"]
            )
        )

        remindLayout.addWidget(self.remindHighPriorityCheck)
        remindLayout.addWidget(self.remindMediumPriorityCheck)
        remindLayout.addWidget(self.remindLowPriorityCheck)

        notificationsFrameLayout.addLayout(remindLayout)

        self.notificationOffsetEditor = QListWidget()

        offsetButtonsLayout = QHBoxLayout()
        self.offsetTypeCombo = QComboBox()
        self.offsetTypeCombo.addItems(["minutes", "hours", "days"])
        self.offsetValueEdit = QLineEdit()
        self.offsetValueEdit.setPlaceholderText("Offset value")
        self.addOffsetButton = QPushButton("Add Offset")
        self.addOffsetButton.clicked.connect(self.addOffset)
        self.removeOffsetButton = QPushButton("Remove Offset")
        self.removeOffsetButton.clicked.connect(self.removeOffset)

        offsetButtonsLayout.addWidget(self.offsetTypeCombo)
        offsetButtonsLayout.addWidget(self.offsetValueEdit)
        offsetButtonsLayout.addWidget(self.addOffsetButton)
        offsetButtonsLayout.addWidget(self.removeOffsetButton)

        notificationsFrameLayout.addWidget(QLabel("Notification Offsets:"))
        notificationsFrameLayout.addWidget(self.notificationOffsetEditor)
        notificationsFrameLayout.addLayout(offsetButtonsLayout)

        self.notificationsFrame.setLayout(notificationsFrameLayout)
        notificationsLayout.addWidget(self.enableNotificationsCheck)
        notificationsLayout.addWidget(self.notificationsFrame)

        self.notificationsTab.setLayout(notificationsLayout)

    def toggleDayRange(self, state):
        self.dayRangeSpin.setEnabled(state == Qt.Checked)

    def toggleNotificationsFrame(self, state):
        self.notificationsFrame.setEnabled(state == Qt.Checked)

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
        self.configManager.set(
            "enableNotifications", self.enableNotificationsCheck.isChecked()
        )
        self.configManager.set(
            "remindHighPriority", self.remindHighPriorityCheck.isChecked()
        )
        self.configManager.set(
            "remindMediumPriority", self.remindMediumPriorityCheck.isChecked()
        )
        self.configManager.set(
            "remindLowPriority", self.remindLowPriorityCheck.isChecked()
        )
        self.configManager.set("notificationOffsets", self.getNotificationOffsets())
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
        self.enableNotificationsCheck.setChecked(
            self.configManager.get(
                "enableNotifications", self.DEFAULTS["enableNotifications"]
            )
        )
        self.remindHighPriorityCheck.setChecked(
            self.configManager.get(
                "remindHighPriority", self.DEFAULTS["remindHighPriority"]
            )
        )
        self.remindMediumPriorityCheck.setChecked(
            self.configManager.get(
                "remindMediumPriority", self.DEFAULTS["remindMediumPriority"]
            )
        )
        self.remindLowPriorityCheck.setChecked(
            self.configManager.get(
                "remindLowPriority", self.DEFAULTS["remindLowPriority"]
            )
        )
        self.setNotificationOffsets(
            self.configManager.get(
                "notificationOffsets", self.DEFAULTS["notificationOffsets"]
            )
        )
        self.notificationsFrame.setEnabled(self.enableNotificationsCheck.isChecked())

    def resetToDefaults(self):
        self.enableSidePanelCheck.setChecked(self.DEFAULTS["enableSidePanel"])
        self.highlightDeadlineCheck.setChecked(self.DEFAULTS["highlightDeadline"])
        self.dayRangeSpin.setValue(self.DEFAULTS["dayRange"])
        self.dueDateCheck.setChecked(self.DEFAULTS["dueDateVisibility"])
        self.dueTimeCheck.setChecked(self.DEFAULTS["dueTimeVisibility"])
        self.categoryCheck.setChecked(self.DEFAULTS["categoryVisibility"])
        self.priorityCheck.setChecked(self.DEFAULTS["priorityVisibility"])
        self.enableDoubleClickCheck.setChecked(self.DEFAULTS["enableDoubleClick"])
        self.enableNotificationsCheck.setChecked(self.DEFAULTS["enableNotifications"])
        self.remindHighPriorityCheck.setChecked(self.DEFAULTS["remindHighPriority"])
        self.remindMediumPriorityCheck.setChecked(self.DEFAULTS["remindMediumPriority"])
        self.remindLowPriorityCheck.setChecked(self.DEFAULTS["remindLowPriority"])
        self.updateColorLabel(
            self.lowPriorityColorLabel, self.DEFAULTS["lowPriorityColor"]
        )
        self.updateColorLabel(
            self.mediumPriorityColorLabel, self.DEFAULTS["mediumPriorityColor"]
        )
        self.updateColorLabel(
            self.highPriorityColorLabel, self.DEFAULTS["highPriorityColor"]
        )
        self.setNotificationOffsets(self.DEFAULTS["notificationOffsets"])
        self.notificationsFrame.setEnabled(self.enableNotificationsCheck.isChecked())

    def setNotificationOffsets(self, offsets):
        self.notificationOffsetEditor.clear()
        for offset in offsets:
            item = QListWidgetItem(f"{offset['value']} {offset['type']}")
            item.setData(Qt.UserRole, offset)
            self.notificationOffsetEditor.addItem(item)

    def getNotificationOffsets(self):
        offsets = []
        for index in range(self.notificationOffsetEditor.count()):
            item = self.notificationOffsetEditor.item(index)
            offsets.append(item.data(Qt.UserRole))
        return offsets

    def addOffset(self):
        offset_type = self.offsetTypeCombo.currentText()
        try:
            offset_value = int(self.offsetValueEdit.text())
            offset = {"type": offset_type, "value": offset_value}
            item = QListWidgetItem(f"{offset_value} {offset_type}")
            item.setData(Qt.UserRole, offset)
            self.notificationOffsetEditor.addItem(item)
        except ValueError:
            pass  # Handle invalid input

    def removeOffset(self):
        selected_items = self.notificationOffsetEditor.selectedItems()
        if selected_items:
            for item in selected_items:
                self.notificationOffsetEditor.takeItem(
                    self.notificationOffsetEditor.row(item)
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
