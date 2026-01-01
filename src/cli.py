"""
CLI interface and user interaction handlers.
"""

import sys
from typing import Optional
from src import storage, todo


def display_menu():
    """Display the main menu (Phase 3)."""
    print("\n===== TODO APP (Phase 3) =====")
    print("\nBASIC OPERATIONS:")
    print("1.  Add Task")
    print("2.  View Tasks")
    print("3.  Mark Task Complete")
    print("4.  Delete Task")
    print("5.  Edit Task")
    print("\nSEARCH & FILTER:")
    print("6.  Search Tasks")
    print("7.  Filter by Priority")
    print("8.  Filter by Category")
    print("9.  View Overdue Tasks")
    print("10. View Today's Tasks")
    print("11. View Tomorrow's Tasks")
    print("\nORGANIZATION:")
    print("12. Sort Tasks")
    print("13. Set Due Date")
    print("14. Add/Edit Task Notes")
    print("15. View Task Details")
    print("16. Add Subtask")
    print("17. Set Dependencies")
    print("18. Set Recurring")
    print("\nTEMPLATES:")
    print("19. Save as Template")
    print("20. List Templates")
    print("21. Create from Template")
    print("\nBULK OPERATIONS:")
    print("22. Bulk Mark Complete")
    print("23. Bulk Delete")
    print("24. Archive Completed")
    print("25. View Archived")
    print("\nADVANCED:")
    print("26. Task Statistics")
    print("27. Undo Last Action")
    print("28. Exit")


def display_task_enhanced(task: dict, indent: int = 0):
    """
    Display a single task with priority, category, due date, and relationships (Phase 3).

    Args:
        task: Task dictionary
        indent: Indentation level for subtasks
    """
    status = "[X]" if task["completed"] else "[ ]"
    priority_symbol = todo.get_priority_symbol(task["priority"])
    description = task["description"]
    category = task["category"].capitalize()
    created = task["created_at"]

    # Phase 3: Due date and overdue status
    due_info = ""
    if task.get("due_date"):
        due_info = f", Due: {task['due_date']}"
        overdue, days = todo.is_overdue(task)
        if overdue:
            due_info += f", OVERDUE by {days} days"
    else:
        due_info = ", No due date"

    # Phase 3.3: Subtask completion ratio
    subtask_info = ""
    if task.get("parent_id") is None:  # Only show for root tasks
        completed, total = storage.get_subtask_completion_ratio(task['id'])
        if total > 0:
            subtask_info = f", {completed}/{total} subtasks complete"

    # Phase 3.3: Dependencies
    dep_info = ""
    depends_on = task.get("depends_on", [])
    if depends_on:
        all_complete, incomplete = storage.check_dependencies_complete(task['id'])
        dep_info = f", Depends on: {len(depends_on)} tasks"
        if not all_complete:
            dep_info += f" ({len(incomplete)} incomplete)"

    # Phase 3.4: Recurring indicator
    recurring_info = ""
    if task.get("recurring"):
        recurring = task["recurring"]
        recurring_info = f", [RECURRING: {recurring['type'].capitalize()}"
        if recurring['interval'] > 1:
            recurring_info += f" every {recurring['interval']} {recurring['type']}s"
        recurring_info += "]"

    # Indentation for subtasks
    prefix = "   " * indent
    if indent > 0:
        prefix += "|-- "

    print(f"{prefix}{task['id']}. {status} {priority_symbol} {description} ({category}{due_info}{subtask_info}{dep_info}{recurring_info}, Created: {created})")


def display_tasks():
    """Display all tasks with hierarchical structure (Phase 3.3)."""
    print("\n===== YOUR TASKS =====")

    tasks = storage.get_all_tasks()

    if not tasks:
        print("No tasks found. Add your first task!")
        return

    stats = todo.get_task_statistics()

    # Phase 3.3: Display root tasks with their subtasks
    root_tasks = storage.get_root_tasks()

    for task in root_tasks:
        display_task_enhanced(task, indent=0)

        # Display subtasks with indentation
        subtasks = storage.get_subtasks(task['id'])
        for subtask in subtasks:
            display_task_enhanced(subtask, indent=1)

    print(f"\nTotal: {stats['total']} tasks ({stats['pending']} pending, {stats['completed']} completed)")
    print(f"Priority: {stats['by_priority']['high']} high, {stats['by_priority']['medium']} medium, {stats['by_priority']['low']} low")


def display_success(message: str):
    """Display a success message."""
    print(f"[SUCCESS] {message}")


def display_error(message: str):
    """Display an error message."""
    print(f"[ERROR] {message}")


def get_menu_choice() -> int:
    """Get and validate menu choice from user (Phase 3: 1-28)."""
    while True:
        try:
            choice = int(input("\nEnter your choice (1-28): "))
            if 1 <= choice <= 28:
                return choice
            else:
                display_error("Invalid choice. Please enter a number between 1 and 28.")
        except ValueError:
            display_error("Invalid input. Please enter a number between 1 and 28.")


def get_task_description() -> str:
    """Get and validate task description from user."""
    while True:
        description = input("Enter task description: ")
        if description.strip():
            return description.strip()
        else:
            display_error("Task description cannot be empty.")


def get_task_id() -> int:
    """Get and validate task ID from user."""
    while True:
        try:
            task_id = int(input("Enter task ID: "))
            return task_id
        except ValueError:
            display_error("Invalid input. Please enter a valid task ID.")


def get_priority_input(default: str = "medium") -> str:
    """Get priority input with default value."""
    print("Select priority (h=high, m=medium, l=low)")
    priority_input = input(f"Priority [{default[0]}]: ").strip()

    if not priority_input:
        return default

    return todo.normalize_priority(priority_input)


def get_category_input(default: int = 4) -> str:
    """Get category input with default value."""
    print("\nSelect category:")
    print("  1. Work")
    print("  2. Personal")
    print("  3. Shopping")
    print("  4. Other")

    try:
        category_input = input(f"Enter choice [4]: ").strip()
        if not category_input:
            return todo.get_category_name(default)

        category_id = int(category_input)
        if 1 <= category_id <= 4:
            return todo.get_category_name(category_id)
        else:
            display_error("Invalid category. Using 'other'.")
            return "other"
    except ValueError:
        display_error("Invalid input. Using 'other'.")
        return "other"


def get_search_keyword() -> str:
    """Get and validate search keyword."""
    while True:
        keyword = input("Enter search keyword: ").strip()
        if keyword:
            return keyword
        else:
            display_error("Search keyword cannot be empty.")


def get_optional_input(prompt: str, current_value: str) -> Optional[str]:
    """Get optional input, return None if empty."""
    user_input = input(f"{prompt} [{current_value}]: ").strip()
    return user_input if user_input else None


def handle_add_task():
    """Handle adding a new task with priority, category, and optional due date (Phase 3)."""
    description = get_task_description()
    priority = get_priority_input()
    category = get_category_input()

    if storage.add_task(description, priority, category):
        tasks = storage.get_all_tasks()
        new_task_id = tasks[-1]['id']

        # Phase 3: Optional due date
        add_due = input("\nAdd due date? (y/n): ").strip().lower()
        if add_due == 'y':
            while True:
                due_date = input("Enter due date (YYYY-MM-DD): ").strip()
                if not due_date:
                    break
                if todo.validate_date_format(due_date):
                    storage.set_due_date(new_task_id, due_date)
                    display_success(f"Task added with due date {due_date}! (ID: {new_task_id}, Priority: {priority.capitalize()}, Category: {category.capitalize()})")
                    return
                else:
                    display_error("Invalid date format. Use YYYY-MM-DD (e.g., 2025-01-15)")

        display_success(f"Task added! (ID: {new_task_id}, Priority: {priority.capitalize()}, Category: {category.capitalize()})")
    else:
        display_error("Failed to add task.")


def handle_view_tasks():
    """Handle viewing all tasks."""
    display_tasks()


def handle_mark_complete():
    """Handle marking a task as complete (Phase 3.3: checks dependencies)."""
    task_id = get_task_id()
    task = storage.get_task_by_id(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    if task["completed"]:
        print("Task is already completed.")
        return

    # Phase 3.3: Check dependencies before marking complete
    all_complete, incomplete = storage.check_dependencies_complete(task_id)
    if not all_complete:
        display_error(f"Cannot complete task {task_id}. Incomplete dependencies:")
        for dep_task in incomplete:
            print(f"  - Task {dep_task['id']}: {dep_task['description']} (Pending)")
        print("\nComplete dependencies first, or remove them to proceed.")
        return

    if storage.mark_task_complete(task_id, force=False):
        display_success("Task marked as complete!")
    else:
        display_error("Failed to mark task as complete.")


def handle_delete_task():
    """Handle deleting a task."""
    task_id = get_task_id()

    if storage.delete_task(task_id):
        display_success("Task deleted successfully!")
    else:
        display_error(f"Task with ID {task_id} not found.")


def handle_edit_task():
    """Handle editing a task."""
    task_id = get_task_id()
    task = storage.get_task_by_id(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    print(f"\nCurrent: {task['description']} ({task['priority']}, {task['category']})")

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

    if storage.edit_task(task_id, new_description, new_priority, new_category):
        display_success("Task updated successfully!")
    else:
        display_error("Failed to update task.")


def handle_search_tasks():
    """Handle searching tasks."""
    keyword = get_search_keyword()
    results = storage.search_tasks(keyword)

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
        results = storage.filter_tasks_by_priority(priority)

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

        if choice not in storage.CATEGORIES:
            display_error("Invalid choice.")
            return

        category = storage.CATEGORIES[choice]
        results = storage.filter_tasks_by_category(category)

        if not results:
            print(f"\nNo {category} tasks found.")
            return

        print(f"\n===== {category.upper()} TASKS =====")
        for task in results:
            display_task_enhanced(task)
        print(f"\nTotal: {len(results)} {category} task(s).")

    except ValueError:
        display_error("Invalid input. Please enter a number.")


def handle_sort_tasks():
    """Handle sorting tasks."""
    print("\nSort by:")
    print("  1. ID (default)")
    print("  2. Priority (High to Low)")
    print("  3. Creation Date (Newest first)")
    print("  4. Creation Date (Oldest first)")

    try:
        choice = int(input("Enter choice (1-4): "))
        sort_map = {
            1: "id",
            2: "priority",
            3: "date_new",
            4: "date_old"
        }

        if choice not in sort_map:
            display_error("Invalid choice.")
            return

        sort_by = sort_map[choice]
        sorted_tasks = storage.sort_tasks(sort_by)

        if not sorted_tasks:
            print("\nNo tasks to sort.")
            return

        sort_labels = {
            "id": "ID",
            "priority": "Priority",
            "date_new": "Date (Newest First)",
            "date_old": "Date (Oldest First)"
        }

        print(f"\n===== TASKS (Sorted by {sort_labels[sort_by]}) =====")

        if sort_by == "priority":
            # Group by priority for better display
            high = [t for t in sorted_tasks if t["priority"] == "high"]
            medium = [t for t in sorted_tasks if t["priority"] == "medium"]
            low = [t for t in sorted_tasks if t["priority"] == "low"]

            if high:
                print("\n[HIGH PRIORITY]")
                for task in high:
                    display_task_enhanced(task)

            if medium:
                print("\n[MEDIUM PRIORITY]")
                for task in medium:
                    display_task_enhanced(task)

            if low:
                print("\n[LOW PRIORITY]")
                for task in low:
                    display_task_enhanced(task)
        else:
            for task in sorted_tasks:
                display_task_enhanced(task)

        print(f"\nTotal: {len(sorted_tasks)} task(s).")

    except ValueError:
        display_error("Invalid input. Please enter a number.")


def handle_statistics():
    """Handle displaying enhanced task statistics (Phase 3.6)."""
    stats = todo.get_enhanced_statistics()
    trends = todo.get_completion_trends()
    relationships = todo.get_relationship_stats()

    print("\n" + "="*70)
    print("ENHANCED TASK STATISTICS (Phase 3)")
    print("="*70)

    if stats["total"] == 0:
        print("\nNo tasks found. Add your first task!")
        return

    # Basic Overview
    print(f"\n{'OVERVIEW':-^70}")
    print(f"Total Tasks:      {stats['total']}")
    print(f"Active Tasks:     {stats['active']}")
    print(f"Archived Tasks:   {stats['archived']}")
    print(f"Completed:        {stats['completed']} ({stats['completion_rate']}%)")
    print(f"Pending:          {stats['pending']}")

    # Priority Breakdown
    print(f"\n{'BY PRIORITY':-^70}")
    for priority in ["high", "medium", "low"]:
        count = stats['by_priority'][priority]
        percentage = (count * 100 // stats['active']) if stats['active'] > 0 else 0
        completion = trends['by_priority'][priority]
        print(f"  {priority.capitalize():8} {count:3} ({percentage:2}%) | Completion: {completion:2}%")

    # Category Breakdown
    print(f"\n{'BY CATEGORY':-^70}")
    for category in ["work", "personal", "shopping", "other"]:
        count = stats['by_category'][category]
        percentage = (count * 100 // stats['active']) if stats['active'] > 0 else 0
        completion = trends['by_category'][category]
        print(f"  {category.capitalize():10} {count:3} ({percentage:2}%) | Completion: {completion:2}%")

    # Time-Based Stats (Phase 3)
    print(f"\n{'TIME-BASED BREAKDOWN':-^70}")
    time_stats = stats['time_based']
    print(f"Overdue:          {time_stats['overdue']} task(s)")
    print(f"Due Today:        {time_stats['today']} task(s)")
    print(f"Due Tomorrow:     {time_stats['tomorrow']} task(s)")
    print(f"Due This Week:    {time_stats['this_week']} task(s)")
    print(f"No Due Date:      {time_stats['no_due_date']} task(s)")

    # Relationship Stats (Phase 3)
    print(f"\n{'RELATIONSHIPS & STRUCTURE':-^70}")
    rel_stats = stats['relationships']
    print(f"Root Tasks:       {rel_stats['root_tasks']}")
    print(f"Subtasks:         {rel_stats['subtasks']}")
    print(f"With Dependencies: {rel_stats['with_dependencies']}")
    print(f"Recurring Tasks:  {rel_stats['recurring']}")

    # Detailed Relationship Insights
    if relationships['subtasks'] > 0 or relationships['tasks_with_dependencies'] > 0:
        print(f"\n{'RELATIONSHIP INSIGHTS':-^70}")
        if relationships['parent_tasks'] > 0:
            print(f"Parent Tasks:     {relationships['parent_tasks']}")
            print(f"Avg Subtasks/Parent: {relationships['avg_subtasks_per_parent']:.1f}")
        if relationships['tasks_with_dependencies'] > 0:
            print(f"Tasks with Deps:  {relationships['tasks_with_dependencies']}")
            print(f"Max Dep Chain:    {relationships['max_dependency_chain']}")
        if relationships['recurring_tasks'] > 0:
            print(f"Recurring Tasks:  {relationships['recurring_tasks']}")

    # Overall Completion Trend
    print(f"\n{'COMPLETION TRENDS':-^70}")
    print(f"Overall Active Completion Rate: {trends['overall']}%")

    print("\n" + "="*70)


def handle_exit():
    """Handle application exit."""
    print("\nThank you for using Todo App! Goodbye!")
    sys.exit(0)


# ============================================================================
# PHASE 3 HANDLERS
# ============================================================================

# ----------------------------------------------------------------------------
# Due Date Handlers
# ----------------------------------------------------------------------------

def handle_set_due_date():
    """Handle setting/updating due date for a task."""
    task_id = get_task_id()
    task = storage.get_task_by_id(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    print(f"\nCurrent task: {task['description']}")
    if task.get('due_date'):
        print(f"Current due date: {task['due_date']}")
    else:
        print("Current due date: None")

    due_date = input("\nEnter new due date (YYYY-MM-DD) or press Enter to remove: ").strip()

    if not due_date:
        # Remove due date
        storage.set_due_date(task_id, None)
        display_success("Due date removed!")
        return

    if todo.validate_date_format(due_date):
        storage.set_due_date(task_id, due_date)
        display_success(f"Due date set to {due_date}!")
    else:
        display_error("Invalid date format. Use YYYY-MM-DD (e.g., 2025-01-15)")


def handle_view_overdue():
    """Handle viewing overdue tasks."""
    overdue_tasks = storage.get_overdue_tasks()

    if not overdue_tasks:
        print("\n===== OVERDUE TASKS =====")
        print("No overdue tasks. Great job!")
        return

    print("\n===== OVERDUE TASKS =====")
    for task in overdue_tasks:
        display_task_enhanced(task)

    print(f"\nTotal: {len(overdue_tasks)} overdue task(s)")


def handle_view_today_tasks():
    """Handle viewing tasks due today."""
    today_tasks = storage.get_tasks_by_due_date("today")

    if not today_tasks:
        print("\n===== TODAY'S TASKS =====")
        print("No tasks due today.")
        return

    from datetime import date
    print(f"\n===== TODAY'S TASKS ({date.today().strftime('%Y-%m-%d')}) =====")
    for task in today_tasks:
        display_task_enhanced(task)

    completed = sum(1 for t in today_tasks if t["completed"])
    print(f"\nTotal: {len(today_tasks)} task(s) due today ({completed} completed)")


def handle_view_tomorrow_tasks():
    """Handle viewing tasks due tomorrow."""
    tomorrow_tasks = storage.get_tasks_by_due_date("tomorrow")

    if not tomorrow_tasks:
        print("\n===== TOMORROW'S TASKS =====")
        print("No tasks due tomorrow.")
        return

    from datetime import date, timedelta
    tomorrow = date.today() + timedelta(days=1)
    print(f"\n===== TOMORROW'S TASKS ({tomorrow.strftime('%Y-%m-%d')}) =====")
    for task in tomorrow_tasks:
        display_task_enhanced(task)

    print(f"\nTotal: {len(tomorrow_tasks)} task(s) due tomorrow")


# ----------------------------------------------------------------------------
# Task Notes Handlers
# ----------------------------------------------------------------------------

def handle_add_edit_notes():
    """Handle adding or editing notes for a task."""
    task_id = get_task_id()
    task = storage.get_task_by_id(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    print(f"\nCurrent task: {task['description']} ({task['priority'].capitalize()}, {task['category'].capitalize()})")

    if task.get('notes'):
        print(f"\nCurrent notes:")
        print(task['notes'])
    else:
        print("\nCurrent notes: [None]")

    print("\nEnter notes (type END on a new line to finish):")

    notes_lines = []
    while True:
        line = input("> ")
        if line.strip().upper() == "END":
            break
        notes_lines.append(line)

    notes = "\n".join(notes_lines)

    if storage.set_task_notes(task_id, notes):
        display_success(f"Notes {'updated' if task.get('notes') else 'added'} for task {task_id}!")
    else:
        display_error("Failed to update notes.")


def handle_view_task_details():
    """Handle viewing complete task details including notes."""
    task_id = get_task_id()
    task = storage.get_task_details(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    print("\n===== TASK DETAILS =====")
    print(f"ID: {task['id']}")
    print(f"Description: {task['description']}")
    print(f"Status: {'Completed' if task['completed'] else 'Pending'}")
    print(f"Priority: {task['priority'].capitalize()}")
    print(f"Category: {task['category'].capitalize()}")

    if task.get('due_date'):
        print(f"Due Date: {task['due_date']}")
        overdue, days = todo.is_overdue(task)
        if overdue:
            print(f"  [OVERDUE by {days} days]")
    else:
        print("Due Date: None")

    print(f"Created: {task['created_at']}")

    if task['completed']:
        print(f"Completed: {task.get('completed_at', 'N/A')}")

    if task.get('notes'):
        print(f"\nNotes:")
        print(task['notes'])
    else:
        print("\nNotes: [None]")


# ----------------------------------------------------------------------------
# Subtask & Dependency Handlers
# ----------------------------------------------------------------------------

def handle_add_subtask():
    """Handle adding a subtask to a parent task."""
    print("\n===== ADD SUBTASK =====")

    parent_id = get_task_id()
    parent = storage.get_task_by_id(parent_id)

    if parent is None:
        display_error(f"Task with ID {parent_id} not found.")
        return

    # Check if parent is already a subtask
    if parent.get("parent_id") is not None:
        display_error("Cannot add subtask. Maximum depth is 2 levels (parent -> subtask only).")
        print("This task is already a subtask.")
        return

    print(f"\nParent: {parent['description']} ({parent['priority'].capitalize()}, {parent['category'].capitalize()})")

    description = get_task_description()
    priority = get_priority_input(parent['priority'])

    # Default to parent's category
    print(f"\nInherit category from parent ({parent['category']})? (y/n): ", end="")
    inherit = input().strip().lower()

    if inherit == 'y':
        category = parent['category']
    else:
        category = get_category_input()

    if storage.add_subtask(parent_id, description, priority, category):
        tasks = storage.get_all_tasks()
        display_success(f"Subtask added! (ID: {tasks[-1]['id']}, Parent: {parent_id})")
    else:
        display_error("Failed to add subtask.")


def handle_set_dependencies():
    """Handle setting dependencies for a task."""
    print("\n===== SET TASK DEPENDENCIES =====")

    task_id = get_task_id()
    task = storage.get_task_by_id(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    print(f"\nCurrent task: {task['description']} ({task['priority'].capitalize()}, {task['category'].capitalize()})")

    current_deps = task.get("depends_on", [])
    if current_deps:
        print(f"Current dependencies: {', '.join(map(str, current_deps))}")
    else:
        print("Current dependencies: None")

    print("\nEnter task IDs this task depends on (comma-separated), or press Enter to clear:")
    dep_input = input("> ").strip()

    if not dep_input:
        # Clear dependencies
        if storage.set_dependencies(task_id, []):
            display_success("Dependencies cleared!")
        else:
            display_error("Failed to clear dependencies.")
        return

    # Parse dependency IDs
    try:
        dep_ids = [int(x.strip()) for x in dep_input.split(',')]
    except ValueError:
        display_error("Invalid input. Please enter comma-separated task IDs.")
        return

    # Show what tasks these are
    print(f"\nProposed dependencies ({len(dep_ids)} tasks):")
    for dep_id in dep_ids:
        dep_task = storage.get_task_by_id(dep_id)
        if dep_task:
            status = "[X]" if dep_task["completed"] else "[ ]"
            print(f"  {status} Task {dep_id}: {dep_task['description']}")
        else:
            print(f"  [NOT FOUND] Task {dep_id}: Invalid ID")
            display_error(f"Task ID {dep_id} does not exist.")
            return

    # Attempt to set dependencies
    if storage.set_dependencies(task_id, dep_ids):
        display_success(f"Dependencies set! Task {task_id} depends on {len(dep_ids)} task(s).")
    else:
        display_error("Failed to set dependencies. Possible reasons:")
        print("  - Circular dependency detected")
        print("  - Self-dependency (task cannot depend on itself)")
        print("  - Invalid task IDs")


# ----------------------------------------------------------------------------
# Recurring Task & Template Handlers
# ----------------------------------------------------------------------------

def handle_set_recurring():
    """Handle setting recurring pattern for a task."""
    print("\n===== SET RECURRING TASK =====")

    task_id = get_task_id()
    task = storage.get_task_by_id(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    print(f"\nCurrent task: {task['description']} ({task['priority'].capitalize()}, {task['category'].capitalize()})")

    # Check if task has due date
    if not task.get("due_date"):
        display_error("Recurring tasks must have a due date.")
        print("Please set a due date first using option 13.")
        return

    print(f"Due date: {task['due_date']}")

    current_recurring = task.get("recurring")
    if current_recurring:
        print(f"Current recurring: {current_recurring['type'].capitalize()} (every {current_recurring['interval']})")

    print("\nRecurrence pattern:")
    print("  1. Daily")
    print("  2. Weekly")
    print("  3. Monthly")
    print("  4. Remove recurring")

    try:
        choice = int(input("Enter choice (1-4): "))
    except ValueError:
        display_error("Invalid input. Please enter a number.")
        return

    if choice == 4:
        # Remove recurring
        task["recurring"] = None
        display_success("Recurring pattern removed!")
        return

    pattern_map = {1: "daily", 2: "weekly", 3: "monthly"}
    if choice not in pattern_map:
        display_error("Invalid choice.")
        return

    recurring_type = pattern_map[choice]

    # Get interval
    print(f"\nHow often? (e.g., 1 = every {recurring_type[:-2]}, 2 = every 2 {recurring_type})")
    try:
        interval = int(input(f"Interval [1]: ").strip() or "1")
        if interval < 1:
            display_error("Interval must be at least 1.")
            return
    except ValueError:
        display_error("Invalid input. Using interval of 1.")
        interval = 1

    if storage.set_recurring(task_id, recurring_type, interval):
        display_success(f"Task set to recur {recurring_type} (every {interval})!")
        print(f"\n[INFO] When this task is marked complete, a new instance will be created with due date: ", end="")
        next_due = todo.calculate_next_due_date(task['due_date'], recurring_type, interval)
        print(next_due)
    else:
        display_error("Failed to set recurring pattern.")


def handle_save_template():
    """Handle saving task as template."""
    print("\n===== SAVE TASK AS TEMPLATE =====")

    task_id = get_task_id()
    task = storage.get_task_by_id(task_id)

    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return

    print(f"\nCurrent task: {task['description']} ({task['priority'].capitalize()}, {task['category'].capitalize()})")

    template_name = input("\nEnter template name: ").strip()

    if not template_name:
        display_error("Template name cannot be empty.")
        return

    if storage.save_as_template(task_id, template_name):
        display_success(f"Template '{template_name}' saved!")
    else:
        display_error("Failed to save template.")


def handle_list_templates():
    """Handle listing all templates."""
    templates = storage.list_templates()

    if not templates:
        print("\n===== TASK TEMPLATES =====")
        print("No templates found. Save a task as template first!")
        return

    print("\n===== TASK TEMPLATES =====")
    for i, name in enumerate(templates, 1):
        template = storage.create_from_template(name)
        print(f"{i}. {name}")
        print(f"   - {template['description']}")
        print(f"   - Priority: {template['priority'].capitalize()}, Category: {template['category'].capitalize()}")

    print(f"\nTotal: {len(templates)} template(s)")


def handle_create_from_template():
    """Handle creating task from template."""
    templates = storage.list_templates()

    if not templates:
        print("\n===== CREATE FROM TEMPLATE =====")
        print("No templates found. Save a task as template first!")
        return

    print("\n===== CREATE FROM TEMPLATE =====")
    print("\nAvailable templates:")
    for i, name in enumerate(templates, 1):
        print(f"  {i}. {name}")

    template_name = input("\nEnter template name: ").strip()

    if not template_name:
        display_error("Template name cannot be empty.")
        return

    template = storage.create_from_template(template_name)

    if template is None:
        display_error(f"Template '{template_name}' not found.")
        return

    print(f"\nTemplate loaded:")
    print(f"  - Description: {template['description']}")
    print(f"  - Priority: {template['priority'].capitalize()}")
    print(f"  - Category: {template['category'].capitalize()}")
    if template.get('notes'):
        print(f"  - Has notes: Yes")

    # Ask if want to modify
    modify = input("\nModify before creating? (y/n): ").strip().lower()

    if modify == 'y':
        description = get_optional_input("New description", template['description']) or template['description']
        print(f"\nCurrent priority: {template['priority']}")
        new_priority = get_priority_input(template['priority'])
        print(f"\nCurrent category: {template['category']}")
        new_category = get_category_input()
    else:
        description = template['description']
        new_priority = template['priority']
        new_category = template['category']

    # Create the task
    if storage.add_task(description, new_priority, new_category):
        tasks = storage.get_all_tasks()
        new_task_id = tasks[-1]['id']

        # Copy notes if present
        if template.get('notes'):
            storage.set_task_notes(new_task_id, template['notes'])

        # Copy recurring if present
        if template.get('recurring'):
            recurring = template['recurring']
            # Ask for due date since recurring requires it
            add_due = input("\nThis template has recurring pattern. Add due date? (y/n): ").strip().lower()
            if add_due == 'y':
                while True:
                    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
                    if due_date and todo.validate_date_format(due_date):
                        storage.set_due_date(new_task_id, due_date)
                        storage.set_recurring(new_task_id, recurring['type'], recurring['interval'])
                        break
                    else:
                        display_error("Invalid date format.")

        display_success(f"Task created from template! (ID: {new_task_id})")
    else:
        display_error("Failed to create task.")


# ----------------------------------------------------------------------------
# Bulk Operation Handlers
# ----------------------------------------------------------------------------

def handle_bulk_mark_complete():
    """Handle marking multiple tasks complete."""
    print("\n===== BULK MARK COMPLETE =====")

    # Show pending tasks
    tasks = [t for t in storage.get_all_tasks() if not t["completed"] and not t.get("archived", False)]

    if not tasks:
        print("No pending tasks to mark complete.")
        return

    print("\nCurrent pending tasks:")
    for task in tasks:
        display_task_enhanced(task)

    task_ids_input = input("\nEnter task IDs to mark complete (comma-separated): ").strip()

    if not task_ids_input:
        display_error("No task IDs provided.")
        return

    # Parse IDs
    try:
        task_ids = [int(x.strip()) for x in task_ids_input.split(',')]
    except ValueError:
        display_error("Invalid input. Please enter comma-separated task IDs.")
        return

    # Mark tasks complete
    success_count = 0
    failed_ids = []

    for task_id in task_ids:
        if storage.mark_task_complete(task_id, force=False):
            success_count += 1
        else:
            failed_ids.append(task_id)

    # Save undo state for bulk operation
    if success_count > 0:
        storage.save_undo_state("bulk_complete", {"task_ids": [tid for tid in task_ids if tid not in failed_ids]})

    display_success(f"Marked {success_count} task(s) as complete!")

    if failed_ids:
        print(f"\n[INFO] Failed to mark {len(failed_ids)} task(s): {', '.join(map(str, failed_ids))}")
        print("  Reasons: Task not found, or has incomplete dependencies")


def handle_bulk_delete():
    """Handle deleting multiple tasks."""
    print("\n===== BULK DELETE =====")

    tasks = storage.get_all_tasks()

    if not tasks:
        print("No tasks to delete.")
        return

    print("\nCurrent tasks:")
    for task in storage.get_root_tasks():
        display_task_enhanced(task, indent=0)
        for subtask in storage.get_subtasks(task['id']):
            display_task_enhanced(subtask, indent=1)

    task_ids_input = input("\nEnter task IDs to delete (comma-separated): ").strip()

    if not task_ids_input:
        display_error("No task IDs provided.")
        return

    # Parse IDs
    try:
        task_ids = [int(x.strip()) for x in task_ids_input.split(',')]
    except ValueError:
        display_error("Invalid input. Please enter comma-separated task IDs.")
        return

    # Confirm deletion
    print(f"\n[WARNING] You are about to delete {len(task_ids)} task(s). This cannot be undone without using Undo!")
    confirm = input("Confirm? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Bulk delete cancelled.")
        return

    # Delete tasks
    success_count = 0
    deleted_tasks = []

    for task_id in task_ids:
        task = storage.get_task_by_id(task_id)
        if task:
            import copy
            deleted_tasks.append(copy.deepcopy(task))
            if storage.delete_task(task_id):
                success_count += 1

    # Save undo state
    if deleted_tasks:
        storage.save_undo_state("bulk_delete", {"tasks": deleted_tasks})

    display_success(f"Deleted {success_count} task(s)!")


def handle_archive_completed():
    """Handle archiving all completed tasks."""
    print("\n===== ARCHIVE COMPLETED TASKS =====")

    completed_tasks = [t for t in storage.get_all_tasks() if t["completed"] and not t.get("archived", False)]

    if not completed_tasks:
        print("No completed tasks to archive.")
        return

    print(f"\nFound {len(completed_tasks)} completed task(s) ready for archiving:")
    for task in completed_tasks[:5]:  # Show first 5
        print(f"  - {task['id']}. {task['description']}")

    if len(completed_tasks) > 5:
        print(f"  ... and {len(completed_tasks) - 5} more")

    confirm = input(f"\nArchive all {len(completed_tasks)} completed task(s)? (y/n): ").strip().lower()

    if confirm != 'y':
        print("Archive cancelled.")
        return

    count = storage.archive_all_completed()
    display_success(f"Archived {count} task(s)!")
    print("\n[INFO] Archived tasks are hidden from default views.")
    print("      Use 'View Archived Tasks' to see them.")


def handle_view_archived():
    """Handle viewing archived tasks."""
    archived = storage.get_archived_tasks()

    if not archived:
        print("\n===== ARCHIVED TASKS =====")
        print("No archived tasks.")
        return

    print("\n===== ARCHIVED TASKS =====")
    for task in archived:
        display_task_enhanced(task)

    print(f"\nTotal: {len(archived)} archived task(s)")


def handle_undo():
    """Handle undoing the last action."""
    print("\n===== UNDO LAST ACTION =====")

    last_action = storage.get_last_action()

    if not last_action:
        print("No action to undo.")
        return

    print(f"\nLast action: {last_action['action'].capitalize()}")
    print(f"Performed at: {last_action['timestamp']}")

    # Show what will be undone
    action = last_action['action']
    data = last_action['data']

    if action == "add":
        print(f"  - Added task '{data['description']}' (ID: {data['task_id']})")
    elif action == "delete":
        print(f"  - Deleted task '{data['task']['description']}'")
    elif action == "edit":
        print(f"  - Edited task {data['task_id']}")
    elif action == "complete":
        print(f"  - Marked task {data['task_id']} as complete")
    elif action == "bulk_complete":
        print(f"  - Bulk marked {len(data['task_ids'])} task(s) complete")
    elif action == "bulk_delete":
        print(f"  - Bulk deleted {len(data['tasks'])} task(s)")

    confirm = input("\nUndo this action? (y/n): ").strip().lower()

    if confirm != 'y':
        print("Undo cancelled.")
        return

    success, description = storage.undo_last_action()

    if success:
        display_success(description)
    else:
        display_error(f"Undo failed: {description}")
