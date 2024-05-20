import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from todo_list_app import ToDoListApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    iconDark = QIcon("icon_dark.png")
    app.setWindowIcon(iconDark)  # Set the window icon

    toDoApp = ToDoListApp()
    toDoApp.setWindowIcon(iconDark)  # Ensure the app window itself uses the same icon
    toDoApp.show()
    sys.exit(app.exec_())
