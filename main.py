import sys
from PyQt5.QtWidgets import QApplication
from todo_list_app import ToDoListApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    toDoApp = ToDoListApp()
    toDoApp.show()
    sys.exit(app.exec_())
