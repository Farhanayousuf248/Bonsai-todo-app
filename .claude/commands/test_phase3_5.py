"""
Test script for Phase 3.5: Bulk Operations & Undo
"""

from src import storage

def test_phase3_5():
    """Test Phase 3.5 features."""
    print("=" * 60)
    print("TESTING PHASE 3.5: BULK OPERATIONS & UNDO")
    print("=" * 60)

    # Test 1: Archive task
    print("\n[TEST 1] Archiving a task...")
    storage.add_task("Task to archive", "medium", "work")
    tasks = storage.get_all_tasks()
    task_id = tasks[-1]['id']

    storage.mark_task_complete(task_id, force=True)
    result = storage.archive_task(task_id)
    print(f"[OK] Task archived: {result}")
    assert result == True, "Should archive successfully"

    task = storage.get_task_by_id(task_id)
    assert task['archived'] == True, "Task should be archived"

    # Test 2: Get archived tasks
    print("\n[TEST 2] Getting archived tasks...")
    archived = storage.get_archived_tasks()
    print(f"[OK] Found {len(archived)} archived task(s)")
    assert len(archived) >= 1, "Should find at least 1 archived task"

    # Test 3: Unarchive task
    print("\n[TEST 3] Unarchiving a task...")
    result = storage.unarchive_task(task_id)
    print(f"[OK] Task unarchived: {result}")
    assert result == True, "Should unarchive successfully"

    task = storage.get_task_by_id(task_id)
    assert task['archived'] == False, "Task should not be archived"

    # Test 4: Archive all completed
    print("\n[TEST 4] Archiving all completed tasks...")
    # Create and complete several tasks
    for i in range(3):
        storage.add_task(f"Task {i}", "low", "other")
        tasks = storage.get_all_tasks()
        storage.mark_task_complete(tasks[-1]['id'], force=True)

    count = storage.archive_all_completed()
    print(f"[OK] Archived {count} completed task(s)")
    assert count >= 3, "Should archive at least 3 tasks"

    # Test 5: Undo add task
    print("\n[TEST 5] Testing undo add task...")
    initial_count = len(storage.get_all_tasks())
    storage.add_task("Task to undo", "high", "work")
    tasks = storage.get_all_tasks()
    added_id = tasks[-1]['id']

    print(f"[OK] Added task {added_id}, count: {len(storage.get_all_tasks())}")

    success, desc = storage.undo_last_action()
    print(f"[OK] Undo result: {success}, {desc}")
    assert success == True, "Undo should succeed"

    final_count = len(storage.get_all_tasks())
    assert final_count == initial_count, "Task count should be restored"
    assert storage.get_task_by_id(added_id) is None, "Task should be removed"

    # Test 6: Undo delete task
    print("\n[TEST 6] Testing undo delete task...")
    storage.add_task("Task to delete and restore", "medium", "personal")
    tasks = storage.get_all_tasks()
    del_task_id = tasks[-1]['id']
    del_task_desc = tasks[-1]['description']

    storage.delete_task(del_task_id)
    print(f"[OK] Task {del_task_id} deleted")
    assert storage.get_task_by_id(del_task_id) is None, "Task should be deleted"

    success, desc = storage.undo_last_action()
    print(f"[OK] Undo result: {success}, {desc}")
    assert success == True, "Undo should succeed"

    restored_task = storage.get_task_by_id(del_task_id)
    assert restored_task is not None, "Task should be restored"
    assert restored_task['description'] == del_task_desc, "Description should match"

    # Test 7: Undo edit task
    print("\n[TEST 7] Testing undo edit task...")
    storage.add_task("Original description", "low", "work")
    tasks = storage.get_all_tasks()
    edit_task_id = tasks[-1]['id']

    original_desc = tasks[-1]['description']
    original_priority = tasks[-1]['priority']

    storage.edit_task(edit_task_id, "Edited description", "high", "personal")
    task = storage.get_task_by_id(edit_task_id)
    print(f"[OK] Task edited: {task['description']}, {task['priority']}")

    success, desc = storage.undo_last_action()
    print(f"[OK] Undo result: {success}")
    assert success == True, "Undo should succeed"

    task = storage.get_task_by_id(edit_task_id)
    assert task['description'] == original_desc, "Description should be restored"
    assert task['priority'] == original_priority, "Priority should be restored"

    # Test 8: Undo mark complete
    print("\n[TEST 8] Testing undo mark complete...")
    storage.add_task("Task to complete and undo", "medium", "work")
    tasks = storage.get_all_tasks()
    complete_task_id = tasks[-1]['id']

    storage.mark_task_complete(complete_task_id, force=True)
    task = storage.get_task_by_id(complete_task_id)
    print(f"[OK] Task marked complete: {task['completed']}")
    assert task['completed'] == True, "Task should be completed"

    success, desc = storage.undo_last_action()
    print(f"[OK] Undo result: {success}")
    assert success == True, "Undo should succeed"

    task = storage.get_task_by_id(complete_task_id)
    assert task['completed'] == False, "Task should be incomplete"
    assert task['completed_at'] is None, "Completed timestamp should be cleared"

    # Test 9: No action to undo
    print("\n[TEST 9] Testing no action to undo...")
    # Clear undo stack by performing an undo
    success, desc = storage.undo_last_action()

    # Try to undo again (nothing to undo)
    success, desc = storage.undo_last_action()
    print(f"[OK] No undo available: {success == False}")
    assert success == False, "Should return False when nothing to undo"
    assert "No action to undo" in desc, "Should have appropriate message"

    # Test 10: Get last action
    print("\n[TEST 10] Testing get last action...")
    storage.add_task("Test last action", "high", "work")

    last_action = storage.get_last_action()
    print(f"[OK] Last action: {last_action['action'] if last_action else 'None'}")
    assert last_action is not None, "Should have last action"
    assert last_action['action'] == "add", "Last action should be add"

    # Test 11: Undo clears stack
    print("\n[TEST 11] Testing undo clears stack...")
    storage.add_task("Task for stack clear test", "low", "other")

    last_action = storage.get_last_action()
    assert last_action is not None, "Should have action before undo"

    storage.undo_last_action()
    last_action = storage.get_last_action()
    print(f"[OK] After undo, last action: {last_action}")
    assert last_action is None, "Undo should clear stack"

    # Test 12: Undo state saved on each operation
    print("\n[TEST 12] Testing undo overwrites previous...")
    storage.add_task("First action", "medium", "work")
    tasks = storage.get_all_tasks()
    first_id = tasks[-1]['id']

    storage.add_task("Second action", "high", "personal")
    tasks = storage.get_all_tasks()
    second_id = tasks[-1]['id']

    # Undo should only undo the second action
    success, desc = storage.undo_last_action()
    print(f"[OK] Undid second action: {success}")

    assert storage.get_task_by_id(second_id) is None, "Second task should be removed"
    assert storage.get_task_by_id(first_id) is not None, "First task should remain"

    # Test 13: Invalid task for archive
    print("\n[TEST 13] Testing archive invalid task...")
    result = storage.archive_task(99999)
    print(f"[OK] Archive invalid task: {result == False}")
    assert result == False, "Should return False for invalid ID"

    # Test 14: Undo preserves task data
    print("\n[TEST 14] Testing undo preserves all task data...")
    storage.add_task("Complex task", "high", "work")
    tasks = storage.get_all_tasks()
    complex_id = tasks[-1]['id']

    # Add notes, due date, etc.
    storage.set_task_notes(complex_id, "Important notes")
    storage.set_due_date(complex_id, "2025-02-01")

    # Delete it
    storage.delete_task(complex_id)

    # Undo should restore everything
    success, desc = storage.undo_last_action()
    restored = storage.get_task_by_id(complex_id)

    print(f"[OK] Restored task notes: {restored.get('notes', '')[:20]}...")
    assert restored is not None, "Task should be restored"
    assert restored['notes'] == "Important notes", "Notes should be preserved"
    assert restored['due_date'] == "2025-02-01", "Due date should be preserved"

    print("\n" + "=" * 60)
    print("ALL PHASE 3.5 TESTS PASSED!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  - Total tasks: {len(storage.get_all_tasks())}")
    print(f"  - Archived tasks: {len(storage.get_archived_tasks())}")
    print(f"  - Undo stack: {'Available' if storage.get_last_action() else 'Empty'}")

if __name__ == "__main__":
    test_phase3_5()
