"""
Todo App Phase 2
Enhanced CLI-based todo application with priorities, categories, edit, and search.
Constitutional Constraints: CLI only, in-memory only, Python standard library only.
"""

from datetime import datetime
import sys

# Module-level variables for in-memory state management
tasks = []
next_task_id = 1

# Phase 2: Priority and Category Constants
PRIORITY_SYMBOLS = {
    "high": "[!]",
    "medium": "[-]",
    "low": "[~]"
}

PRIORITY_SORT = {
    "high": 1,
    "medium": 2,
    "low": 3
}

CATEGORIES = {
    1: "work",
    2: "personal",
    3: "shopping",
    4: "other"
}


# Core Data Functions

def generate_task_id():
    """Generate unique task ID and increment counter."""
    global next_task_id
    current_id = next_task_id
    next_task_id += 1
    return current_id


def create_task(description, priority="medium", category="other"):
    """Create a task dictionary with all required fields."""
    task_id = generate_task_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "id": task_id,
        "description": description,
        "completed": False,
        "created_at": timestamp,
        "priority": priority,
        "category": category
    }


def add_task(description, priority="medium", category="other"):
    """Add a new task to the tasks list."""
    if not description or not description.strip():
        return False
    task = create_task(description.strip(), priority, category)
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


# Phase 2: New Core Data Functions

def edit_task(task_id, description=None, priority=None, category=None):
    """Edit task fields. Only updates provided fields."""
    task = get_task_by_id(task_id)
    if task is None:
        return False

    if description is not None and description.strip():
        task["description"] = description.strip()
    if priority is not None:
        task["priority"] = priority
    if category is not None:
        task["category"] = category

    return True


def search_tasks(keyword):
    """Search tasks by keyword in description (case-insensitive)."""
    if not keyword:
        return []
    keyword_lower = keyword.lower()
    return [task for task in tasks if keyword_lower in task["description"].lower()]


def filter_tasks_by_priority(priority):
    """Filter tasks by priority level."""
    return [task for task in tasks if task["priority"] == priority]


def filter_tasks_by_category(category):
    """Filter tasks by category."""
    return [task for task in tasks if task["category"] == category]


# Phase 2: Utility Functions

def normalize_priority(priority_input):
    """Convert priority input to standard format."""
    if not priority_input:
        return "medium"

    priority_input = priority_input.strip().lower()

    if priority_input in ["h", "high"]:
        return "high"
    elif priority_input in ["m", "medium"]:
        return "medium"
    elif priority_input in ["l", "low"]:
        return "low"
    else:
        return "medium"


def get_priority_symbol(priority):
    """Get display symbol for priority."""
    return PRIORITY_SYMBOLS.get(priority, "[-]")


def get_category_name(category_id):
    """Convert category ID to name."""
    return CATEGORIES.get(category_id, "other")


# Display Functions

def display_menu():
    """Display the main menu."""
    print("\n===== TODO APP (Phase 2) =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task Complete")
    print("4. Delete Task")
    print("5. Edit Task")
    print("6. Search Tasks")
    print("7. Filter by Priority")
    print("8. Filter by Category")
    print("9. Exit")


def display_task_enhanced(task):
    """Display a single task with priority and category."""
    status = "[X]" if task["completed"] else "[ ]"
    priority_symbol = get_priority_symbol(task["priority"])
    description = task["description"]
    category = task["category"].capitalize()
    created = task["created_at"]

    print(f"{task['id']}. {status} {priority_symbol} {description} ({category}, Created: {created})")


def display_tasks():
    """Display all tasks with enhanced formatting."""
    print("\n===== YOUR TASKS =====")

    if not tasks:
        print("No tasks found. Add your first task!")
        return

    pending_count = 0
    completed_count = 0
    priority_counts = {"high": 0, "medium": 0, "low": 0}

    for task in tasks:
        display_task_enhanced(task)

        if task["completed"]:
            completed_count += 1
        else:
            pending_count += 1

        priority_counts[task["priority"]] += 1

    print(f"\nTotal: {len(tasks)} tasks ({pending_count} pending, {completed_count} completed)")
    print(f"Priority: {priority_counts['high']} high, {priority_counts['medium']} medium, {priority_counts['low']} low")


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
            choice = int(input("\nEnter your choice (1-9): "))
            if 1 <= choice <= 9:
                return choice
            else:
                display_error("Invalid choice. Please enter a number between 1 and 9.")
        except ValueError:
            display_error("Invalid input. Please enter a number between 1 and 9.")


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


# Phase 2: New Input Functions

def get_priority_input(default="medium"):
    """Get priority input with default value."""
    print("Select priority (h=high, m=medium, l=low)")
    priority_input = input(f"Priority [{default[0]}]: ").strip()

    if not priority_input:
        return default

    return normalize_priority(priority_input)


def get_category_input(default=4):
    """Get category input with default value."""
    print("\nSelect category:")
    print("  1. Work")
    print("  2. Personal")
    print("  3. Shopping")
    print("  4. Other")

    try:
        category_input = input(f"Enter choice [4]: ").strip()
        if not category_input:
            return get_category_name(default)

        category_id = int(category_input)
        if 1 <= category_id <= 4:
            return get_category_name(category_id)
        else:
            display_error("Invalid category. Using 'other'.")
            return "other"
    except ValueError:
        display_error("Invalid input. Using 'other'.")
        return "other"


def get_search_keyword():
    """Get and validate search keyword."""
    while True:
        keyword = input("Enter search keyword: ").strip()
        if keyword:
            return keyword
        else:
            display_error("Search keyword cannot be empty.")


def get_optional_input(prompt, current_value):
    """Get optional input, return None if empty."""
    user_input = input(f"{prompt} [{current_value}]: ").strip()
    return user_input if user_input else None


# Menu Handler Functions

def handle_add_task():
    """Handle adding a new task with priority and category."""
    description = get_task_description()
    priority = get_priority_input()
    category = get_category_input()

    if add_task(description, priority, category):
        display_success(f"Task added! (ID: {tasks[-1]['id']}, Priority: {priority.capitalize()}, Category: {category.capitalize()})")
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


# Phase 2: New Menu Handlers

def handle_edit_task():
    """Handle editing a task."""
    task_id = get_task_id()
    task = get_task_by_id(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    print(f"\nCurrent: {task['description']} ({task['priority']}, {task['category']})")

    # Get new values (optional)
    new_description = get_optional_input("New description", task['description'])

    print("\nUpdate priority? (y/n)")
    if input().strip().lower() == 'y':
        new_priority = get_priority_input(task['priority'])
    else:
        new_priority = None

    print("\nUpdate category? (y/n)")
    if input().strip().lower() == 'y':
        new_category = get_category_input()
    else:
        new_category = None

    if edit_task(task_id, new_description, new_priority, new_category):
        display_success("Task updated successfully!")
    else:
        display_error("Failed to update task.")


def handle_search_tasks():
    """Handle searching tasks."""
    keyword = get_search_keyword()
    results = search_tasks(keyword)

    if not results:
        print(f"\nNo tasks found matching '{keyword}'.")
        return

    print(f"\n===== SEARCH RESULTS FOR '{keyword}' =====")
    for task in results:
        display_task_enhanced(task)
    print(f"\nFound {len(results)} matching task(s).")


def handle_filter_priority():
    """Handle filtering tasks by priority."""
    print("\nSelect priority to filter:")
    print("  1. High")
    print("  2. Medium")
    print("  3. Low")

    try:
        choice = int(input("Enter choice (1-3): "))
        priority_map = {1: "high", 2: "medium", 3: "low"}

        if choice not in priority_map:
            display_error("Invalid choice.")
            return

        priority = priority_map[choice]
        results = filter_tasks_by_priority(priority)

        if not results:
            print(f"\nNo {priority} priority tasks found.")
            return

        print(f"\n===== {priority.upper()} PRIORITY TASKS =====")
        for task in results:
            display_task_enhanced(task)
        print(f"\nTotal: {len(results)} {priority} priority task(s).")

    except ValueError:
        display_error("Invalid input. Please enter a number.")


def handle_filter_category():
    """Handle filtering tasks by category."""
    print("\nSelect category to filter:")
    print("  1. Work")
    print("  2. Personal")
    print("  3. Shopping")
    print("  4. Other")

    try:
        choice = int(input("Enter choice (1-4): "))

        if choice not in CATEGORIES:
            display_error("Invalid choice.")
            return

        category = CATEGORIES[choice]
        results = filter_tasks_by_category(category)

        if not results:
            print(f"\nNo {category} tasks found.")
            return

        print(f"\n===== {category.upper()} TASKS =====")
        for task in results:
            display_task_enhanced(task)
        print(f"\nTotal: {len(results)} {category} task(s).")

    except ValueError:
        display_error("Invalid input. Please enter a number.")


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
                handle_edit_task()
            elif choice == 6:
                handle_search_tasks()
            elif choice == 7:
                handle_filter_priority()
            elif choice == 8:
                handle_filter_category()
            elif choice == 9:
                handle_exit()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
