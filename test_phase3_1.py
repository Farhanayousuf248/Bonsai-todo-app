"""
Test script for Phase 3.1: Due Dates & Overdue Detection
"""

from src import storage, todo
from datetime import date, timedelta

def test_phase3_1():
    """Test Phase 3.1 features."""
    print("=" * 60)
    print("TESTING PHASE 3.1: DUE DATES & OVERDUE DETECTION")
    print("=" * 60)

    # Test 1: Create task with all Phase 3 fields
    print("\n[TEST 1] Creating task with Phase 3 fields...")
    storage.add_task("Test task", "high", "work")
    tasks = storage.get_all_tasks()
    task = tasks[-1]

    print(f"[OK] Task created with ID: {task['id']}")
    print(f"  - due_date: {task['due_date']}")
    print(f"  - notes: '{task['notes']}'")
    print(f"  - parent_id: {task['parent_id']}")
    print(f"  - depends_on: {task['depends_on']}")
    print(f"  - recurring: {task['recurring']}")
    print(f"  - archived: {task['archived']}")
    print(f"  - completed_at: {task['completed_at']}")

    # Test 2: Set due date
    print("\n[TEST 2] Setting due date...")
    future_date = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
    storage.set_due_date(task['id'], future_date)
    task = storage.get_task_by_id(task['id'])
    print(f"[OK] Due date set to: {task['due_date']}")

    # Test 3: Validate date format
    print("\n[TEST 3] Testing date validation...")
    assert todo.validate_date_format("2025-01-15") == True, "Valid date should pass"
    assert todo.validate_date_format("2025-13-01") == False, "Invalid month should fail"
    assert todo.validate_date_format("invalid") == False, "Invalid format should fail"
    print("[OK] Date validation working correctly")

    # Test 4: Create overdue task
    print("\n[TEST 4] Creating overdue task...")
    storage.add_task("Overdue task", "high", "work")
    tasks = storage.get_all_tasks()
    overdue_task = tasks[-1]
    past_date = (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")
    storage.set_due_date(overdue_task['id'], past_date)
    print(f"[OK] Task created with past due date: {past_date}")

    # Test 5: Check overdue detection
    print("\n[TEST 5] Testing overdue detection...")
    is_over, days = todo.is_overdue(overdue_task)
    print(f"[OK] Task is overdue: {is_over}, Days: {days}")
    assert is_over == True, "Should detect overdue"
    assert days == 5, "Should calculate 5 days overdue"

    # Test 6: Get overdue tasks
    print("\n[TEST 6] Getting all overdue tasks...")
    overdue_tasks = storage.get_overdue_tasks()
    print(f"[OK] Found {len(overdue_tasks)} overdue task(s)")
    assert len(overdue_tasks) >= 1, "Should find at least 1 overdue task"

    # Test 7: Today's tasks
    print("\n[TEST 7] Testing today's tasks filter...")
    storage.add_task("Today's task", "medium", "personal")
    tasks = storage.get_all_tasks()
    today_task = tasks[-1]
    storage.set_due_date(today_task['id'], date.today().strftime("%Y-%m-%d"))
    today_tasks = storage.get_tasks_by_due_date("today")
    print(f"[OK] Found {len(today_tasks)} task(s) due today")
    assert len(today_tasks) >= 1, "Should find at least 1 task due today"

    # Test 8: Tomorrow's tasks
    print("\n[TEST 8] Testing tomorrow's tasks filter...")
    storage.add_task("Tomorrow's task", "low", "shopping")
    tasks = storage.get_all_tasks()
    tomorrow_task = tasks[-1]
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    storage.set_due_date(tomorrow_task['id'], tomorrow)
    tomorrow_tasks = storage.get_tasks_by_due_date("tomorrow")
    print(f"[OK] Found {len(tomorrow_tasks)} task(s) due tomorrow")
    assert len(tomorrow_tasks) >= 1, "Should find at least 1 task due tomorrow"

    # Test 9: Mark complete sets completed_at
    print("\n[TEST 9] Testing completed_at timestamp...")
    storage.mark_task_complete(task['id'])
    completed_task = storage.get_task_by_id(task['id'])
    print(f"[OK] Task marked complete")
    print(f"  - completed: {completed_task['completed']}")
    print(f"  - completed_at: {completed_task['completed_at']}")
    assert completed_task['completed_at'] is not None, "Should set completed_at"

    # Test 10: Overdue tasks exclude completed
    print("\n[TEST 10] Verifying completed tasks not in overdue list...")
    storage.mark_task_complete(overdue_task['id'])
    overdue_tasks = storage.get_overdue_tasks()
    overdue_ids = [t['id'] for t in overdue_tasks]
    assert overdue_task['id'] not in overdue_ids, "Completed tasks should not be overdue"
    print("[OK] Completed tasks correctly excluded from overdue list")

    print("\n" + "=" * 60)
    print("ALL PHASE 3.1 TESTS PASSED!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  - Total tasks created: {len(storage.get_all_tasks())}")
    print(f"  - Tasks with due dates: {sum(1 for t in storage.get_all_tasks() if t['due_date'])}")
    print(f"  - Overdue tasks: {len(storage.get_overdue_tasks())}")
    print(f"  - Today's tasks: {len(storage.get_tasks_by_due_date('today'))}")
    print(f"  - Tomorrow's tasks: {len(storage.get_tasks_by_due_date('tomorrow'))}")

if __name__ == "__main__":
    test_phase3_1()
