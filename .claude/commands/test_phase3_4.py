"""
Test script for Phase 3.4: Automation (Recurring Tasks & Templates)
"""

from src import storage, todo
from datetime import date, timedelta

def test_phase3_4():
    """Test Phase 3.4 features."""
    print("=" * 60)
    print("TESTING PHASE 3.4: AUTOMATION")
    print("=" * 60)

    # Test 1: Set recurring pattern
    print("\n[TEST 1] Setting recurring pattern...")
    storage.add_task("Daily standup", "medium", "work")
    tasks = storage.get_all_tasks()
    task_id = tasks[-1]['id']

    # Set due date first
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    storage.set_due_date(task_id, tomorrow)

    result = storage.set_recurring(task_id, "daily", 1)
    print(f"[OK] Recurring set: {result}")
    assert result == True, "Should set recurring successfully"

    task = storage.get_task_by_id(task_id)
    assert task['recurring'] is not None, "Task should have recurring pattern"
    assert task['recurring']['type'] == "daily", "Recurring type should be daily"
    assert task['recurring']['interval'] == 1, "Interval should be 1"

    # Test 2: Recurring requires due date
    print("\n[TEST 2] Testing recurring requires due date...")
    storage.add_task("Task without due date", "low", "other")
    tasks = storage.get_all_tasks()
    no_due_id = tasks[-1]['id']

    result = storage.set_recurring(no_due_id, "weekly", 1)
    print(f"[OK] Set recurring without due date: {result}")
    assert result == False, "Should reject recurring without due date"

    # Test 3: Create recurring instance
    print("\n[TEST 3] Creating recurring instance...")
    initial_count = len(storage.get_all_tasks())

    result = storage.create_recurring_instance(task_id)
    print(f"[OK] Recurring instance created: {result}")
    assert result == True, "Should create instance successfully"

    new_count = len(storage.get_all_tasks())
    assert new_count == initial_count + 1, "Should have one more task"

    # Verify new instance
    tasks = storage.get_all_tasks()
    new_task = tasks[-1]
    print(f"[OK] New instance due date: {new_task['due_date']}")
    assert new_task['description'] == task['description'], "Description should match"
    assert new_task['recurring'] is not None, "New instance should also be recurring"

    # Test 4: Auto-create on mark complete
    print("\n[TEST 4] Testing auto-creation on mark complete...")
    storage.add_task("Weekly meeting", "high", "work")
    tasks = storage.get_all_tasks()
    weekly_id = tasks[-1]['id']

    # Set up recurring
    next_week = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    storage.set_due_date(weekly_id, next_week)
    storage.set_recurring(weekly_id, "weekly", 1)

    before_count = len(storage.get_all_tasks())
    storage.mark_task_complete(weekly_id, force=True)
    after_count = len(storage.get_all_tasks())

    print(f"[OK] Tasks before: {before_count}, after: {after_count}")
    assert after_count == before_count + 1, "Should auto-create new instance"

    # Test 5: Custom intervals
    print("\n[TEST 5] Testing custom intervals...")
    storage.add_task("Bi-weekly task", "medium", "work")
    tasks = storage.get_all_tasks()
    bi_weekly_id = tasks[-1]['id']

    storage.set_due_date(bi_weekly_id, tomorrow)
    result = storage.set_recurring(bi_weekly_id, "weekly", 2)
    print(f"[OK] Set recurring every 2 weeks: {result}")
    assert result == True, "Should set custom interval"

    task = storage.get_task_by_id(bi_weekly_id)
    assert task['recurring']['interval'] == 2, "Interval should be 2"

    # Test 6: Monthly recurring
    print("\n[TEST 6] Testing monthly recurring...")
    storage.add_task("Monthly report", "high", "work")
    tasks = storage.get_all_tasks()
    monthly_id = tasks[-1]['id']

    storage.set_due_date(monthly_id, "2025-01-15")
    result = storage.set_recurring(monthly_id, "monthly", 1)
    print(f"[OK] Monthly recurring set: {result}")
    assert result == True, "Should set monthly recurring"

    # Calculate next date
    next_due = todo.calculate_next_due_date("2025-01-15", "monthly", 1)
    print(f"[OK] Next due date would be: {next_due}")
    # Approximate check (30 days)
    assert next_due == "2025-02-14", "Should be approximately 1 month later"

    # Test 7: Save task as template
    print("\n[TEST 7] Saving task as template...")
    storage.add_task("Template task", "high", "work")
    tasks = storage.get_all_tasks()
    template_task_id = tasks[-1]['id']

    storage.set_task_notes(template_task_id, "These are template notes")

    result = storage.save_as_template(template_task_id, "my-template")
    print(f"[OK] Template saved: {result}")
    assert result == True, "Should save template successfully"

    # Test 8: List templates
    print("\n[TEST 8] Listing templates...")
    templates = storage.list_templates()
    print(f"[OK] Found {len(templates)} template(s)")
    assert "my-template" in templates, "Should find saved template"

    # Test 9: Create from template
    print("\n[TEST 9] Creating from template...")
    template = storage.create_from_template("my-template")
    print(f"[OK] Template loaded")
    assert template is not None, "Should load template"
    assert template['description'] == "Template task", "Description should match"
    assert template['priority'] == "high", "Priority should match"
    assert template['notes'] == "These are template notes", "Notes should match"

    # Test 10: Template with recurring
    print("\n[TEST 10] Testing template with recurring pattern...")
    storage.add_task("Recurring template", "medium", "personal")
    tasks = storage.get_all_tasks()
    rec_temp_id = tasks[-1]['id']

    storage.set_due_date(rec_temp_id, "2025-02-01")
    storage.set_recurring(rec_temp_id, "daily", 1)
    storage.save_as_template(rec_temp_id, "recurring-temp")

    template = storage.create_from_template("recurring-temp")
    print(f"[OK] Recurring template loaded")
    assert template['recurring'] is not None, "Should preserve recurring pattern"
    assert template['recurring']['type'] == "daily", "Should preserve type"

    # Test 11: Delete template
    print("\n[TEST 11] Deleting template...")
    result = storage.delete_template("my-template")
    print(f"[OK] Template deleted: {result}")
    assert result == True, "Should delete successfully"

    templates = storage.list_templates()
    assert "my-template" not in templates, "Template should be gone"

    # Test 12: Invalid recurring type
    print("\n[TEST 12] Testing invalid recurring type...")
    storage.add_task("Invalid recurring", "low", "other")
    tasks = storage.get_all_tasks()
    invalid_id = tasks[-1]['id']

    storage.set_due_date(invalid_id, tomorrow)
    result = storage.set_recurring(invalid_id, "invalid-type", 1)
    print(f"[OK] Invalid type rejected: {result == False}")
    assert result == False, "Should reject invalid type"

    # Test 13: Invalid interval
    print("\n[TEST 13] Testing invalid interval...")
    storage.add_task("Invalid interval", "low", "other")
    tasks = storage.get_all_tasks()
    invalid_int_id = tasks[-1]['id']

    storage.set_due_date(invalid_int_id, tomorrow)
    result = storage.set_recurring(invalid_int_id, "daily", 0)
    print(f"[OK] Invalid interval rejected: {result == False}")
    assert result == False, "Should reject interval < 1"

    # Test 14: Template name normalization
    print("\n[TEST 14] Testing template name normalization...")
    storage.add_task("Test task", "medium", "work")
    tasks = storage.get_all_tasks()
    test_id = tasks[-1]['id']

    storage.save_as_template(test_id, "  My-Template  ")
    templates = storage.list_templates()
    print(f"[OK] Templates: {templates}")
    assert "my-template" in templates, "Should normalize to lowercase and trim"

    # Test 15: Empty template name
    print("\n[TEST 15] Testing empty template name...")
    result = storage.save_as_template(test_id, "")
    print(f"[OK] Empty name rejected: {result == False}")
    assert result == False, "Should reject empty name"

    print("\n" + "=" * 60)
    print("ALL PHASE 3.4 TESTS PASSED!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  - Total tasks: {len(storage.get_all_tasks())}")
    print(f"  - Recurring tasks: {sum(1 for t in storage.get_all_tasks() if t.get('recurring'))}")
    print(f"  - Templates: {len(storage.list_templates())}")

if __name__ == "__main__":
    test_phase3_4()
