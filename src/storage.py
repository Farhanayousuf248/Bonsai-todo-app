"""
In-memory storage module for Todo App.
Handles all data storage and retrieval operations.
"""

from datetime import datetime
from typing import List, Dict, Optional

# Module-level variables for in-memory state management
_tasks: List[Dict] = []
_next_task_id: int = 1

# Phase 3: Additional storage
_undo_stack: List[Dict] = []        # Stores last action for undo
_task_templates: Dict[str, Dict] = {}  # Stores task templates
_archived_tasks: List[Dict] = []    # Archived tasks storage

# Constants
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

# Phase 3: Recurring patterns
RECURRING_TYPES = ["daily", "weekly", "monthly"]


def generate_task_id() -> int:
    """Generate unique task ID and increment counter."""
    global _next_task_id
    current_id = _next_task_id
    _next_task_id += 1
    return current_id


def create_task(description: str, priority: str = "medium", category: str = "other") -> Dict:
    """Create a task dictionary with all required fields (Phase 1-3)."""
    task_id = generate_task_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        # Phase 1 & 2 fields
        "id": task_id,
        "description": description,
        "completed": False,
        "created_at": timestamp,
        "priority": priority,
        "category": category,
        # Phase 3 new fields
        "due_date": None,           # YYYY-MM-DD or None
        "notes": "",                # Multi-line notes
        "parent_id": None,          # Parent task ID for subtasks
        "depends_on": [],           # List of task IDs
        "recurring": None,          # Recurring pattern dict or None
        "archived": False,          # Archived status
        "completed_at": None        # ISO timestamp when completed
    }


def add_task(description: str, priority: str = "medium", category: str = "other") -> bool:
    """Add a new task to the tasks list."""
    if not description or not description.strip():
        return False
    task = create_task(description.strip(), priority, category)
    _tasks.append(task)

    # Phase 3.5: Save undo state
    save_undo_state("add", {
        "task_id": task["id"],
        "description": task["description"]
    })

    return True


def get_all_tasks() -> List[Dict]:
    """Get all tasks."""
    return _tasks.copy()


def get_task_by_id(task_id: int) -> Optional[Dict]:
    """Find and return a task by its ID."""
    for task in _tasks:
        if task["id"] == task_id:
            return task
    return None


def mark_task_complete(task_id: int, force: bool = False) -> bool:
    """
    Mark a task as completed by its ID.
    Phase 3.4: Creates new instance if recurring.
    Phase 3.5: Saves undo state.

    Args:
        task_id: Task ID
        force: If True, skip dependency check (used internally)

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    # Phase 3.3: Check dependencies unless forced
    if not force:
        all_complete, incomplete = check_dependencies_complete(task_id)
        if not all_complete:
            return False

    # Phase 3.5: Save undo state before changing
    save_undo_state("complete", {"task_id": task_id})

    task["completed"] = True
    task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Phase 3.4: Create recurring instance if applicable
    if task.get("recurring"):
        create_recurring_instance(task_id)

    return True


def delete_task(task_id: int) -> bool:
    """
    Delete a task by its ID.
    Phase 3.3: Also removes from dependencies and handles subtasks.
    Phase 3.5: Saves undo state.

    Args:
        task_id: Task ID

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    # Phase 3.5: Save undo state before deleting (save a copy)
    import copy
    save_undo_state("delete", {"task": copy.deepcopy(task)})

    # Phase 3.3: Remove from all dependencies
    remove_task_from_dependencies(task_id)

    # Phase 3.3: Delete all subtasks if this is a parent
    subtasks = get_subtasks(task_id)
    for subtask in subtasks:
        _tasks.remove(subtask)

    _tasks.remove(task)
    return True


def edit_task(task_id: int, description: Optional[str] = None,
              priority: Optional[str] = None, category: Optional[str] = None) -> bool:
    """Edit task fields. Only updates provided fields. Phase 3.5: Saves undo state."""
    task = get_task_by_id(task_id)
    if task is None:
        return False

    # Phase 3.5: Save undo state before editing
    save_undo_state("edit", {
        "task_id": task_id,
        "old_description": task["description"],
        "old_priority": task["priority"],
        "old_category": task["category"]
    })

    if description is not None and description.strip():
        task["description"] = description.strip()
    if priority is not None:
        task["priority"] = priority
    if category is not None:
        task["category"] = category

    return True


def search_tasks(keyword: str) -> List[Dict]:
    """Search tasks by keyword in description (case-insensitive)."""
    if not keyword:
        return []
    keyword_lower = keyword.lower()
    return [task for task in _tasks if keyword_lower in task["description"].lower()]


def filter_tasks_by_priority(priority: str) -> List[Dict]:
    """Filter tasks by priority level."""
    return [task for task in _tasks if task["priority"] == priority]


def filter_tasks_by_category(category: str) -> List[Dict]:
    """Filter tasks by category."""
    return [task for task in _tasks if task["category"] == category]


def get_task_count() -> int:
    """Get total number of tasks."""
    return len(_tasks)


def sort_tasks(sort_by: str = "id") -> List[Dict]:
    """
    Sort tasks by specified criteria.

    Args:
        sort_by: "id", "priority", "date_new", "date_old"

    Returns:
        Sorted list of tasks
    """
    if sort_by == "priority":
        return sorted(_tasks, key=lambda t: PRIORITY_SORT[t["priority"]])
    elif sort_by == "date_new":
        return sorted(_tasks, key=lambda t: t["created_at"], reverse=True)
    elif sort_by == "date_old":
        return sorted(_tasks, key=lambda t: t["created_at"])
    else:  # default: sort by id
        return sorted(_tasks, key=lambda t: t["id"])


# ============================================================================
# PHASE 3 FUNCTIONS
# ============================================================================

# ----------------------------------------------------------------------------
# Due Date Operations
# ----------------------------------------------------------------------------

def set_due_date(task_id: int, due_date: Optional[str]) -> bool:
    """
    Set or update due date for a task.

    Args:
        task_id: Task ID
        due_date: Date in YYYY-MM-DD format or None to remove

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False
    task["due_date"] = due_date
    return True


def get_overdue_tasks() -> List[Dict]:
    """
    Get list of overdue tasks (due_date < today AND not completed).

    Returns:
        List of overdue tasks
    """
    from datetime import date
    today = date.today()

    overdue = []
    for task in _tasks:
        if task["completed"] or task["archived"]:
            continue
        if task["due_date"]:
            try:
                task_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                if task_date < today:
                    overdue.append(task)
            except ValueError:
                continue

    return overdue


def get_tasks_by_due_date(date_filter: str) -> List[Dict]:
    """
    Get tasks filtered by due date.

    Args:
        date_filter: "today", "tomorrow", "this_week", "this_month"

    Returns:
        List of tasks matching filter
    """
    from datetime import date, timedelta

    today = date.today()
    filtered = []

    for task in _tasks:
        if task["archived"]:
            continue
        if not task["due_date"]:
            continue

        try:
            task_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()

            if date_filter == "today":
                if task_date == today:
                    filtered.append(task)
            elif date_filter == "tomorrow":
                if task_date == today + timedelta(days=1):
                    filtered.append(task)
            elif date_filter == "this_week":
                week_end = today + timedelta(days=7)
                if today <= task_date <= week_end:
                    filtered.append(task)
            elif date_filter == "this_month":
                if task_date.year == today.year and task_date.month == today.month:
                    filtered.append(task)
        except ValueError:
            continue

    return filtered


# ----------------------------------------------------------------------------
# Task Notes Operations
# ----------------------------------------------------------------------------

def set_task_notes(task_id: int, notes: str) -> bool:
    """
    Set or update notes for a task.

    Args:
        task_id: Task ID
        notes: Multi-line notes text

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False
    task["notes"] = notes
    return True


def get_task_details(task_id: int) -> Optional[Dict]:
    """
    Get complete task details including notes.

    Args:
        task_id: Task ID

    Returns:
        Task dictionary or None if not found
    """
    return get_task_by_id(task_id)


# ----------------------------------------------------------------------------
# Subtask Operations
# ----------------------------------------------------------------------------

def add_subtask(parent_id: int, description: str, priority: str = "medium",
                category: str = "other") -> bool:
    """
    Create a subtask under a parent task.

    Args:
        parent_id: Parent task ID
        description: Subtask description
        priority: Priority level
        category: Category (defaults to parent's category if not specified)

    Returns:
        True if successful, False otherwise
    """
    parent = get_task_by_id(parent_id)
    if parent is None:
        return False

    # Check if parent is archived
    if parent.get("archived", False):
        return False

    # Check if parent is already a subtask (enforce 2-level max depth)
    if parent.get("parent_id") is not None:
        return False

    # Create subtask with parent_id set
    task = create_task(description, priority, category)
    task["parent_id"] = parent_id

    # Inherit category from parent if using default
    if category == "other" and parent["category"] != "other":
        task["category"] = parent["category"]

    _tasks.append(task)
    return True


def get_subtasks(parent_id: int) -> List[Dict]:
    """
    Get all subtasks for a parent task.

    Args:
        parent_id: Parent task ID

    Returns:
        List of subtask dictionaries
    """
    return [task for task in _tasks if task.get("parent_id") == parent_id]


def get_root_tasks() -> List[Dict]:
    """
    Get only root-level tasks (tasks without parent).

    Returns:
        List of root task dictionaries
    """
    return [task for task in _tasks if task.get("parent_id") is None]


def get_subtask_completion_ratio(parent_id: int) -> tuple[int, int]:
    """
    Get completion ratio for subtasks.

    Args:
        parent_id: Parent task ID

    Returns:
        Tuple of (completed_count, total_count)
    """
    subtasks = get_subtasks(parent_id)
    if not subtasks:
        return 0, 0

    completed = sum(1 for t in subtasks if t["completed"])
    return completed, len(subtasks)


# ----------------------------------------------------------------------------
# Dependency Operations
# ----------------------------------------------------------------------------

def set_dependencies(task_id: int, depends_on: List[int]) -> bool:
    """
    Set dependency list for a task.

    Args:
        task_id: Task ID
        depends_on: List of task IDs this task depends on

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    # Validate all dependency IDs exist
    for dep_id in depends_on:
        if get_task_by_id(dep_id) is None:
            return False

    # Check for self-dependency
    if task_id in depends_on:
        return False

    # Check for circular dependencies
    if has_circular_dependency(task_id, depends_on):
        return False

    task["depends_on"] = depends_on.copy()
    return True


def check_dependencies_complete(task_id: int) -> tuple[bool, List[Dict]]:
    """
    Check if all dependencies are complete.

    Args:
        task_id: Task ID

    Returns:
        Tuple of (all_complete: bool, incomplete_tasks: List[Dict])
    """
    task = get_task_by_id(task_id)
    if task is None:
        return True, []

    depends_on = task.get("depends_on", [])
    if not depends_on:
        return True, []

    incomplete = []
    for dep_id in depends_on:
        dep_task = get_task_by_id(dep_id)
        if dep_task and not dep_task["completed"]:
            incomplete.append(dep_task)

    return len(incomplete) == 0, incomplete


def has_circular_dependency(task_id: int, new_depends_on: List[int]) -> bool:
    """
    Check if adding dependencies would create a circular dependency.

    Args:
        task_id: Task ID
        new_depends_on: Proposed list of dependencies

    Returns:
        True if circular dependency detected, False otherwise
    """
    # Build dependency graph including the new dependencies
    graph = {}
    for task in _tasks:
        graph[task["id"]] = task.get("depends_on", []).copy()

    # Add the proposed dependencies
    graph[task_id] = new_depends_on.copy()

    # Use DFS to detect cycle
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    visited = set()
    rec_stack = set()

    return has_cycle(task_id, visited, rec_stack)


def remove_task_from_dependencies(task_id: int) -> None:
    """
    Remove a task ID from all other tasks' dependency lists.

    Args:
        task_id: Task ID to remove from dependencies
    """
    for task in _tasks:
        depends_on = task.get("depends_on", [])
        if task_id in depends_on:
            depends_on.remove(task_id)


# ----------------------------------------------------------------------------
# Recurring Task Operations
# ----------------------------------------------------------------------------

def set_recurring(task_id: int, recurring_type: str, interval: int = 1) -> bool:
    """
    Set recurring pattern for a task.

    Args:
        task_id: Task ID
        recurring_type: "daily", "weekly", or "monthly"
        interval: Number of days/weeks/months between recurrences

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    # Recurring tasks must have a due date
    if not task.get("due_date"):
        return False

    # Validate recurring type
    if recurring_type not in RECURRING_TYPES:
        return False

    # Validate interval
    if interval < 1:
        return False

    task["recurring"] = {
        "type": recurring_type,
        "interval": interval
    }
    return True


def create_recurring_instance(task_id: int) -> bool:
    """
    Create new instance of recurring task with next due date.

    Args:
        task_id: Task ID of recurring task

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    recurring = task.get("recurring")
    if not recurring:
        return False

    # Import here to avoid circular dependency
    from src import todo

    # Calculate next due date
    current_due = task["due_date"]
    next_due = todo.calculate_next_due_date(
        current_due,
        recurring["type"],
        recurring["interval"]
    )

    # Create new task with same properties but new due date
    new_task = create_task(
        task["description"],
        task["priority"],
        task["category"]
    )

    # Copy recurring fields
    new_task["due_date"] = next_due
    new_task["notes"] = task["notes"]
    new_task["recurring"] = recurring.copy()

    _tasks.append(new_task)
    return True


# ----------------------------------------------------------------------------
# Template Operations
# ----------------------------------------------------------------------------

def save_as_template(task_id: int, template_name: str) -> bool:
    """
    Save task as template.

    Args:
        task_id: Task ID
        template_name: Name for the template

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    # Validate template name
    if not template_name or not template_name.strip():
        return False

    template_name = template_name.strip().lower()

    # Create template (exclude id, timestamps, completion status)
    template = {
        "description": task["description"],
        "priority": task["priority"],
        "category": task["category"],
        "notes": task.get("notes", ""),
        "recurring": task.get("recurring")
    }

    _task_templates[template_name] = template
    return True


def list_templates() -> List[str]:
    """
    List all template names.

    Returns:
        List of template names
    """
    return sorted(_task_templates.keys())


def create_from_template(template_name: str) -> Optional[Dict]:
    """
    Get template configuration for creating new task.

    Args:
        template_name: Template name

    Returns:
        Template dictionary or None if not found
    """
    template_name = template_name.strip().lower()
    return _task_templates.get(template_name)


def delete_template(template_name: str) -> bool:
    """
    Delete a template.

    Args:
        template_name: Template name

    Returns:
        True if successful, False otherwise
    """
    template_name = template_name.strip().lower()
    if template_name in _task_templates:
        del _task_templates[template_name]
        return True
    return False


# ----------------------------------------------------------------------------
# Archive Operations
# ----------------------------------------------------------------------------

def archive_task(task_id: int) -> bool:
    """
    Archive a task (move to archived state).

    Args:
        task_id: Task ID

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    task["archived"] = True
    return True


def unarchive_task(task_id: int) -> bool:
    """
    Unarchive a task (restore to active state).

    Args:
        task_id: Task ID

    Returns:
        True if successful, False otherwise
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    task["archived"] = False
    return True


def get_archived_tasks() -> List[Dict]:
    """
    Get all archived tasks.

    Returns:
        List of archived tasks
    """
    return [task for task in _tasks if task.get("archived", False)]


def archive_all_completed() -> int:
    """
    Archive all completed tasks.

    Returns:
        Number of tasks archived
    """
    count = 0
    for task in _tasks:
        if task["completed"] and not task.get("archived", False):
            task["archived"] = True
            count += 1
    return count


# ----------------------------------------------------------------------------
# Undo Operations
# ----------------------------------------------------------------------------

def save_undo_state(action: str, data: Dict) -> None:
    """
    Save state for undo operation.

    Args:
        action: Action name ("add", "delete", "edit", "complete", "bulk_complete", "bulk_delete")
        data: Data needed to undo the action
    """
    global _undo_stack
    _undo_stack = [{
        "action": action,
        "data": data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }]


def undo_last_action() -> tuple[bool, str]:
    """
    Undo the last action.

    Returns:
        Tuple of (success: bool, description: str)
    """
    global _undo_stack

    if not _undo_stack:
        return False, "No action to undo"

    undo_info = _undo_stack[0]
    action = undo_info["action"]
    data = undo_info["data"]

    try:
        if action == "add":
            # Undo add by deleting the task
            task_id = data["task_id"]
            task = get_task_by_id(task_id)
            if task:
                _tasks.remove(task)
                description = f"Undid: Add task '{data['description']}'"
            else:
                return False, "Task no longer exists"

        elif action == "delete":
            # Undo delete by restoring the task
            task = data["task"]
            _tasks.append(task)
            description = f"Undid: Delete task '{task['description']}'"

        elif action == "edit":
            # Undo edit by restoring old values
            task_id = data["task_id"]
            task = get_task_by_id(task_id)
            if task:
                task["description"] = data["old_description"]
                task["priority"] = data["old_priority"]
                task["category"] = data["old_category"]
                description = f"Undid: Edit task {task_id}"
            else:
                return False, "Task no longer exists"

        elif action == "complete":
            # Undo complete by marking incomplete
            task_id = data["task_id"]
            task = get_task_by_id(task_id)
            if task:
                task["completed"] = False
                task["completed_at"] = None
                description = f"Undid: Mark task {task_id} complete"
            else:
                return False, "Task no longer exists"

        elif action == "bulk_complete":
            # Undo bulk complete
            for task_id in data["task_ids"]:
                task = get_task_by_id(task_id)
                if task:
                    task["completed"] = False
                    task["completed_at"] = None
            description = f"Undid: Bulk complete {len(data['task_ids'])} task(s)"

        elif action == "bulk_delete":
            # Undo bulk delete by restoring tasks
            for task in data["tasks"]:
                _tasks.append(task)
            description = f"Undid: Bulk delete {len(data['tasks'])} task(s)"

        else:
            return False, f"Cannot undo action: {action}"

        # Clear undo stack after successful undo
        _undo_stack = []
        return True, description

    except Exception as e:
        return False, f"Undo failed: {str(e)}"


def get_last_action() -> Optional[Dict]:
    """
    Get information about the last action.

    Returns:
        Dictionary with action info or None if no action
    """
    if not _undo_stack:
        return None
    return _undo_stack[0]
