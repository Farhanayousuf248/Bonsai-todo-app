"""
Core Todo operations and business logic.
"""

from typing import Dict, List, Optional
from src import storage


def normalize_priority(priority_input: str) -> str:
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


def get_priority_symbol(priority: str) -> str:
    """Get display symbol for priority."""
    return storage.PRIORITY_SYMBOLS.get(priority, "[-]")


def get_category_name(category_id: int) -> str:
    """Convert category ID to name."""
    return storage.CATEGORIES.get(category_id, "other")


def get_task_statistics() -> Dict:
    """Calculate task statistics."""
    tasks = storage.get_all_tasks()

    if not tasks:
        return {
            "total": 0,
            "completed": 0,
            "pending": 0,
            "by_priority": {"high": 0, "medium": 0, "low": 0},
            "by_category": {"work": 0, "personal": 0, "shopping": 0, "other": 0}
        }

    completed = sum(1 for task in tasks if task["completed"])
    pending = len(tasks) - completed

    by_priority = {"high": 0, "medium": 0, "low": 0}
    by_category = {"work": 0, "personal": 0, "shopping": 0, "other": 0}

    for task in tasks:
        by_priority[task["priority"]] += 1
        by_category[task["category"]] += 1

    return {
        "total": len(tasks),
        "completed": completed,
        "pending": pending,
        "by_priority": by_priority,
        "by_category": by_category
    }


# ============================================================================
# PHASE 3 FUNCTIONS
# ============================================================================

# ----------------------------------------------------------------------------
# Date Utilities
# ----------------------------------------------------------------------------

def validate_date_format(date_str: str) -> bool:
    """
    Validate date is in YYYY-MM-DD format and is a valid date.

    Args:
        date_str: Date string to validate

    Returns:
        True if valid, False otherwise
    """
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_overdue(task: Dict) -> tuple[bool, int]:
    """
    Check if task is overdue and calculate days overdue.

    Args:
        task: Task dictionary

    Returns:
        Tuple of (is_overdue: bool, days_overdue: int)
    """
    from datetime import datetime, date

    if task["completed"] or not task["due_date"]:
        return False, 0

    try:
        task_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        today = date.today()

        if task_date < today:
            days_overdue = (today - task_date).days
            return True, days_overdue
        return False, 0
    except ValueError:
        return False, 0


def calculate_next_due_date(current_due: str, recurring_type: str, interval: int) -> str:
    """
    Calculate next due date for recurring task.

    Args:
        current_due: Current due date (YYYY-MM-DD)
        recurring_type: "daily", "weekly", or "monthly"
        interval: Number of days/weeks/months to add

    Returns:
        Next due date as YYYY-MM-DD string
    """
    from datetime import datetime, timedelta

    current_date = datetime.strptime(current_due, "%Y-%m-%d").date()

    if recurring_type == "daily":
        next_date = current_date + timedelta(days=interval)
    elif recurring_type == "weekly":
        next_date = current_date + timedelta(weeks=interval)
    elif recurring_type == "monthly":
        # Add months manually (approximate using 30 days per month)
        # This is a simple approximation for stdlib-only constraint
        next_date = current_date + timedelta(days=30 * interval)
    else:
        next_date = current_date

    return next_date.strftime("%Y-%m-%d")


# ----------------------------------------------------------------------------
# Dependency Utilities
# ----------------------------------------------------------------------------

def build_dependency_graph() -> Dict[int, List[int]]:
    """
    Build adjacency list representation of task dependencies.

    Returns:
        Dictionary mapping task ID to list of dependency IDs
    """
    graph = {}
    tasks = storage.get_all_tasks()

    for task in tasks:
        graph[task["id"]] = task.get("depends_on", []).copy()

    return graph


# ----------------------------------------------------------------------------
# Enhanced Statistics (Sub-Phase 3.6)
# ----------------------------------------------------------------------------

def get_enhanced_statistics() -> Dict:
    """
    Get comprehensive statistics including Phase 3 metrics.

    Returns:
        Dictionary containing:
        - Basic stats (total, completed, pending)
        - Time-based breakdowns (overdue, today, tomorrow, week)
        - Relationship stats (subtasks, dependencies, recurring)
        - Archive stats
        - Completion trends
    """
    from datetime import datetime, timedelta

    tasks = storage.get_all_tasks()

    if not tasks:
        return {
            "total": 0,
            "completed": 0,
            "pending": 0,
            "archived": 0,
            "active": 0,
            "by_priority": {"high": 0, "medium": 0, "low": 0},
            "by_category": {"work": 0, "personal": 0, "shopping": 0, "other": 0},
            "time_based": {
                "overdue": 0,
                "today": 0,
                "tomorrow": 0,
                "this_week": 0,
                "no_due_date": 0
            },
            "relationships": {
                "root_tasks": 0,
                "subtasks": 0,
                "with_dependencies": 0,
                "recurring": 0
            },
            "completion_rate": 0
        }

    # Basic stats
    completed = sum(1 for t in tasks if t["completed"])
    archived = sum(1 for t in tasks if t.get("archived", False))
    active = len(tasks) - archived
    pending = sum(1 for t in tasks if not t["completed"] and not t.get("archived", False))

    # Priority and category breakdowns
    by_priority = {"high": 0, "medium": 0, "low": 0}
    by_category = {"work": 0, "personal": 0, "shopping": 0, "other": 0}

    for task in tasks:
        if not task.get("archived", False):
            by_priority[task["priority"]] += 1
            by_category[task["category"]] += 1

    # Time-based stats
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    week_end = today + timedelta(days=7)

    time_stats = {
        "overdue": 0,
        "today": 0,
        "tomorrow": 0,
        "this_week": 0,
        "no_due_date": 0
    }

    for task in tasks:
        if task.get("archived", False):
            continue

        due_date = task.get("due_date")
        if not due_date:
            time_stats["no_due_date"] += 1
            continue

        try:
            due = datetime.strptime(due_date, "%Y-%m-%d").date()

            if not task["completed"]:
                if due < today:
                    time_stats["overdue"] += 1
                elif due == today:
                    time_stats["today"] += 1
                elif due == tomorrow:
                    time_stats["tomorrow"] += 1
                elif due <= week_end:
                    time_stats["this_week"] += 1
        except ValueError:
            pass

    # Relationship stats
    root_tasks = sum(1 for t in tasks if t.get("parent_id") is None and not t.get("archived", False))
    subtasks = sum(1 for t in tasks if t.get("parent_id") is not None and not t.get("archived", False))
    with_dependencies = sum(1 for t in tasks if t.get("depends_on") and not t.get("archived", False))
    recurring = sum(1 for t in tasks if t.get("recurring") is not None and not t.get("archived", False))

    relationship_stats = {
        "root_tasks": root_tasks,
        "subtasks": subtasks,
        "with_dependencies": with_dependencies,
        "recurring": recurring
    }

    # Completion rate
    completion_rate = (completed * 100 // len(tasks)) if len(tasks) > 0 else 0

    return {
        "total": len(tasks),
        "completed": completed,
        "pending": pending,
        "archived": archived,
        "active": active,
        "by_priority": by_priority,
        "by_category": by_category,
        "time_based": time_stats,
        "relationships": relationship_stats,
        "completion_rate": completion_rate
    }


def get_completion_trends() -> Dict:
    """
    Calculate completion rates by various dimensions.

    Returns:
        Dictionary containing completion trends:
        - By priority (high, medium, low)
        - By category (work, personal, shopping, other)
        - Overall completion rate
    """
    tasks = storage.get_all_tasks()

    if not tasks:
        return {
            "by_priority": {"high": 0, "medium": 0, "low": 0},
            "by_category": {"work": 0, "personal": 0, "shopping": 0, "other": 0},
            "overall": 0
        }

    # Filter out archived tasks for trends
    active_tasks = [t for t in tasks if not t.get("archived", False)]

    if not active_tasks:
        return {
            "by_priority": {"high": 0, "medium": 0, "low": 0},
            "by_category": {"work": 0, "personal": 0, "shopping": 0, "other": 0},
            "overall": 0
        }

    # Completion by priority
    priority_trends = {}
    for priority in ["high", "medium", "low"]:
        priority_tasks = [t for t in active_tasks if t["priority"] == priority]
        if priority_tasks:
            completed_count = sum(1 for t in priority_tasks if t["completed"])
            priority_trends[priority] = (completed_count * 100) // len(priority_tasks)
        else:
            priority_trends[priority] = 0

    # Completion by category
    category_trends = {}
    for category in ["work", "personal", "shopping", "other"]:
        category_tasks = [t for t in active_tasks if t["category"] == category]
        if category_tasks:
            completed_count = sum(1 for t in category_tasks if t["completed"])
            category_trends[category] = (completed_count * 100) // len(category_tasks)
        else:
            category_trends[category] = 0

    # Overall completion
    overall = (sum(1 for t in active_tasks if t["completed"]) * 100) // len(active_tasks)

    return {
        "by_priority": priority_trends,
        "by_category": category_trends,
        "overall": overall
    }


def get_relationship_stats() -> Dict:
    """
    Get statistics on task relationships (subtasks, dependencies, recurring).

    Returns:
        Dictionary containing:
        - Total parent tasks
        - Total subtasks
        - Average subtasks per parent
        - Tasks with dependencies
        - Total recurring tasks
        - Dependency chains info
    """
    tasks = storage.get_all_tasks()
    active_tasks = [t for t in tasks if not t.get("archived", False)]

    if not active_tasks:
        return {
            "parent_tasks": 0,
            "subtasks": 0,
            "avg_subtasks_per_parent": 0,
            "tasks_with_dependencies": 0,
            "recurring_tasks": 0,
            "max_dependency_chain": 0
        }

    # Parent and subtask stats
    parent_tasks = [t for t in active_tasks if t.get("parent_id") is None]
    subtasks = [t for t in active_tasks if t.get("parent_id") is not None]

    parents_with_subtasks = set(t["parent_id"] for t in subtasks)
    avg_subtasks = len(subtasks) // len(parents_with_subtasks) if parents_with_subtasks else 0

    # Dependency stats
    tasks_with_deps = [t for t in active_tasks if t.get("depends_on")]

    # Find max dependency chain length
    max_chain = 0
    for task in active_tasks:
        chain_length = _get_dependency_chain_length(task["id"], active_tasks)
        max_chain = max(max_chain, chain_length)

    # Recurring tasks
    recurring_tasks = [t for t in active_tasks if t.get("recurring") is not None]

    return {
        "parent_tasks": len(parents_with_subtasks),
        "subtasks": len(subtasks),
        "avg_subtasks_per_parent": avg_subtasks,
        "tasks_with_dependencies": len(tasks_with_deps),
        "recurring_tasks": len(recurring_tasks),
        "max_dependency_chain": max_chain
    }


def _get_dependency_chain_length(task_id: int, tasks: List[Dict], visited: Optional[set] = None) -> int:
    """
    Helper function to calculate dependency chain length.

    Args:
        task_id: Task ID to start from
        tasks: List of all tasks
        visited: Set of visited task IDs (for cycle detection)

    Returns:
        Length of dependency chain
    """
    if visited is None:
        visited = set()

    if task_id in visited:
        return 0

    visited.add(task_id)

    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task or not task.get("depends_on"):
        return 0

    max_chain = 0
    for dep_id in task["depends_on"]:
        chain_length = 1 + _get_dependency_chain_length(dep_id, tasks, visited.copy())
        max_chain = max(max_chain, chain_length)

    return max_chain
