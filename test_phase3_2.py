"""
Test script for Phase 3.2: Task Notes
"""

from src import storage

def test_phase3_2():
    """Test Phase 3.2 features."""
    print("=" * 60)
    print("TESTING PHASE 3.2: TASK NOTES")
    print("=" * 60)

    # Test 1: Create task and add notes
    print("\n[TEST 1] Adding notes to a task...")
    storage.add_task("Task with notes", "high", "work")
    tasks = storage.get_all_tasks()
    task_id = tasks[-1]['id']

    notes = "This is a multi-line note.\nLine 2 of the note.\nLine 3 with details."
    storage.set_task_notes(task_id, notes)

    task = storage.get_task_by_id(task_id)
    print(f"[OK] Notes added to task {task_id}")
    print(f"  Notes content ({len(notes)} chars):")
    for i, line in enumerate(task['notes'].split('\n'), 1):
        print(f"    {i}. {line}")

    # Test 2: Update existing notes
    print("\n[TEST 2] Updating notes...")
    new_notes = "Updated notes content.\nThis replaces the old notes."
    storage.set_task_notes(task_id, new_notes)

    task = storage.get_task_by_id(task_id)
    print(f"[OK] Notes updated")
    print(f"  New notes: {task['notes'][:50]}...")
    assert task['notes'] == new_notes, "Notes should be updated"

    # Test 3: Empty notes
    print("\n[TEST 3] Setting empty notes...")
    storage.set_task_notes(task_id, "")

    task = storage.get_task_by_id(task_id)
    print(f"[OK] Notes set to empty string")
    print(f"  Notes: '{task['notes']}'")
    assert task['notes'] == "", "Notes should be empty string"

    # Test 4: Very long notes
    print("\n[TEST 4] Testing long notes...")
    long_notes = "A" * 1000
    storage.set_task_notes(task_id, long_notes)

    task = storage.get_task_by_id(task_id)
    print(f"[OK] Long notes added ({len(task['notes'])} chars)")
    assert len(task['notes']) == 1000, "Should handle 1000 character notes"

    # Test 5: Get task details
    print("\n[TEST 5] Getting task details...")
    storage.set_task_notes(task_id, "These are the final notes.\nWith multiple lines.")
    details = storage.get_task_details(task_id)

    print(f"[OK] Task details retrieved")
    print(f"  ID: {details['id']}")
    print(f"  Description: {details['description']}")
    print(f"  Priority: {details['priority']}")
    print(f"  Category: {details['category']}")
    print(f"  Notes: {details['notes'][:30]}...")

    # Test 6: Task without notes
    print("\n[TEST 6] Creating task without notes...")
    storage.add_task("Task without notes", "medium", "personal")
    tasks = storage.get_all_tasks()
    task_no_notes = tasks[-1]

    print(f"[OK] Task created")
    print(f"  Has notes: {bool(task_no_notes['notes'])}")
    print(f"  Notes value: '{task_no_notes['notes']}'")
    assert task_no_notes['notes'] == "", "Default notes should be empty string"

    # Test 7: Invalid task ID
    print("\n[TEST 7] Testing invalid task ID...")
    result = storage.set_task_notes(99999, "Some notes")
    print(f"[OK] Invalid task ID handled")
    print(f"  Result: {result}")
    assert result == False, "Should return False for invalid task ID"

    # Test 8: Notes preserved on other operations
    print("\n[TEST 8] Verifying notes preserved on edit...")
    storage.set_task_notes(task_id, "Important notes to preserve")
    storage.edit_task(task_id, description="Updated description")

    task = storage.get_task_by_id(task_id)
    print(f"[OK] Notes preserved after edit")
    print(f"  Description updated: {task['description']}")
    print(f"  Notes intact: {task['notes']}")
    assert task['notes'] == "Important notes to preserve", "Notes should be preserved"

    print("\n" + "=" * 60)
    print("ALL PHASE 3.2 TESTS PASSED!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  - Total tasks created: {len(storage.get_all_tasks())}")
    print(f"  - Tasks with notes: {sum(1 for t in storage.get_all_tasks() if t['notes'])}")

if __name__ == "__main__":
    test_phase3_2()
