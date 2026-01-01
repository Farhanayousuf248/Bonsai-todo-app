"""
Todo App Phase 1
A simple CLI-based todo application with in-memory storage.
Constitutional Constraints: CLI only, in-memory only, Python standard library only.
"""

from datetime import datetime
import sys

# Module-level variables for in-memory state management
tasks = []
next_task_id = 1


# Core Data Functions

def generate_task_id():
    """Generate unique task ID and increment counter."""
    global next_task_id
    current_id = next_task_id
    next_task_id += 1
    return current_id


def create_task(description):
    """Create a task dictionary with all required fields."""
    task_id = generate_task_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "id": task_id,
        "description": description,
        "completed": False,
        "created_at": timestamp
    }


def add_task(description):
    """Add a new task to the tasks list."""
    if not description or not description.strip():
        return False
    task = create_task(description.strip())
    tasks.append(task)
    return True


def get_task_by_id(task_id):
    """Find and return a task by its ID."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def mark_task_complete(task_id):
    """Mark a task as completed by its ID."""
    task = get_task_by_id(task_id)
    if task is None:
        return False
    task["completed"] = True
    return True


def delete_task(task_id):
    """Delete a task by its ID."""
    task = get_task_by_id(task_id)
    if task is None:
        return False
    tasks.remove(task)
    return True


# Display Functions

def display_menu():
    """Display the main menu."""
    print("\n===== TODO APP =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task Complete")
    print("4. Delete Task")
    print("5. Exit")


def display_tasks():
    """Display all tasks with formatting."""
    print("\n===== YOUR TASKS =====")

    if not tasks:
        print("No tasks found. Add your first task!")
        return

    pending_count = 0
    completed_count = 0

    for task in tasks:
        status = "[X]" if task["completed"] else "[ ]"
        print(f"{task['id']}. {status} {task['description']} (Created: {task['created_at']})")

        if task["completed"]:
            completed_count += 1
        else:
            pending_count += 1

    print(f"\nTotal: {len(tasks)} tasks ({pending_count} pending, {completed_count} completed)")


def display_success(message):
    """Display a success message."""
    print(f"[SUCCESS] {message}")


def display_error(message):
    """Display an error message."""
    print(f"[ERROR] {message}")


# Input Functions

def get_menu_choice():
    """Get and validate menu choice from user."""
    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            else:
                display_error("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            display_error("Invalid input. Please enter a number between 1 and 5.")


def get_task_description():
    """Get and validate task description from user."""
    while True:
        description = input("Enter task description: ")
        if description.strip():
            return description.strip()
        else:
            display_error("Task description cannot be empty.")


def get_task_id():
    """Get and validate task ID from user."""
    while True:
        try:
            task_id = int(input("Enter task ID: "))
            return task_id
        except ValueError:
            display_error("Invalid input. Please enter a valid task ID.")


# Menu Handler Functions

def handle_add_task():
    """Handle adding a new task."""
    description = get_task_description()
    if add_task(description):
        display_success(f"Task added successfully! (ID: {tasks[-1]['id']})")
    else:
        display_error("Failed to add task.")


def handle_view_tasks():
    """Handle viewing all tasks."""
    display_tasks()


def handle_mark_complete():
    """Handle marking a task as complete."""
    task_id = get_task_id()
    task = get_task_by_id(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    if task["completed"]:
        print("Task is already completed.")
        return

    if mark_task_complete(task_id):
        display_success("Task marked as complete!")
    else:
        display_error("Failed to mark task as complete.")


def handle_delete_task():
    """Handle deleting a task."""
    task_id = get_task_id()

    if delete_task(task_id):
        display_success("Task deleted successfully!")
    else:
        display_error(f"Task with ID {task_id} not found.")


def handle_exit():
    """Handle application exit."""
    print("\nThank you for using Todo App! Goodbye!")
    sys.exit(0)


# Main Function

def main():
    """Main application loop."""
    try:
        while True:
            display_menu()
            choice = get_menu_choice()

            if choice == 1:
                handle_add_task()
            elif choice == 2:
                handle_view_tasks()
            elif choice == 3:
                handle_mark_complete()
            elif choice == 4:
                handle_delete_task()
            elif choice == 5:
                handle_exit()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
