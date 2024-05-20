# To-Do List Application

A simple yet powerful To-Do List application built using Python and PyQt5. This application allows users to manage their tasks efficiently with features such as task addition, editing, deletion, priority setting, and filtering/sorting of tasks. The application also includes functionalities to mark tasks as completed, automatically save/load tasks, and search through tasks.

![image](https://github.com/zahiterdemguzel/ToDoList/assets/37737787/15b73446-53ba-4339-b52a-523cb6c3b892)


## Features

- **Add Tasks:** Create new tasks with a description, due date, and priority.
- **Edit Tasks:** Modify existing tasks to update their information.
- **Delete Tasks:** Remove tasks that are no longer needed.
- **Mark as Completed:** Mark tasks as completed or not completed using checkboxes.
- **Set Priorities:** Assign priorities (Low, Medium, High) to tasks.
- **Filter and Sort Tasks:** Filter tasks by completion status and priority, and sort them by name, date, or priority.
- **Search Tasks:** Search for tasks by their name or description.
- **Automatic Saving:** Automatically save tasks to a JSON file and load them on startup.
- **User-Friendly Interface:** Intuitive and responsive user interface with tooltips and visual indicators for priorities.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/zahitderdemguzel/ToDoList.git
    cd todo-list-app
    ```

2. **Install the required packages:**

    ```bash
    pip install PyQt5
    ```

3. **Run the application:**

    ```bash
    python main.py
    ```

## Files

- **main.py:** Entry point of the application.
- **tasks.json:** JSON file used to store tasks.
- **task_item_widget.py:** Defines the widget for individual task items.
- **filter_sort_manager.py:** Manages the filtering and sorting of tasks.
- **todo_list_app.py:** Main application window.
- **task_dialog.py:** Dialog window for adding and editing tasks.
- **task_manager.py:** Handles task operations such as add, edit, delete, and complete.
- **utils.py:** Utility functions for saving and loading tasks.

## Usage

1. **Adding a Task:**
    - Click on the "Add Task" button.
    - Fill in the task details in the dialog that appears.
    - Click "Add" to save the task.

2. **Editing a Task:**
    - Double-click on a task in the list or select a task and click "Edit Task".
    - Update the task details in the dialog that appears.
    - Click "Save" to update the task.

3. **Deleting a Task:**
    - Select a task and click "Delete Task".

4. **Marking a Task as Completed:**
    - Click the checkbox next to a task to mark it as completed or not completed.

5. **Filtering and Sorting Tasks:**
    - Use the "Filter" dropdown to filter tasks by completion status or priority.
    - Use the "Sort" dropdown to sort tasks by name, date, or priority.

6. **Searching for Tasks:**
    - Use the search bar at the top to search for tasks by their name or description.

## Contributions

Contributions are welcome! Please fork the repository and create a pull request with your improvements.

## License

This project is not licenced.

## Contact

For any questions or feedback, please contact [zahit14724@gmail.com](mailto:zahit14724@gmail.com)

