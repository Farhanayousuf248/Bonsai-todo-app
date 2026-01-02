"""
Test script for Phase 3.3: Relationships (Subtasks & Dependencies)
"""

from src import storage

def test_phase3_3():
    """Test Phase 3.3 features."""
    print("=" * 60)
    print("TESTING PHASE 3.3: RELATIONSHIPS")
    print("=" * 60)

    # Test 1: Create parent task
    print("\n[TEST 1] Creating parent task...")
    storage.add_task("Parent task", "high", "work")
    tasks = storage.get_all_tasks()
    parent_id = tasks[-1]['id']
    print(f"[OK] Parent task created (ID: {parent_id})")

    # Test 2: Add subtask
    print("\n[TEST 2] Adding subtask...")
    result = storage.add_subtask(parent_id, "Subtask 1", "medium", "work")
    assert result == True, "Should add subtask successfully"

    tasks = storage.get_all_tasks()
    subtask = tasks[-1]
    print(f"[OK] Subtask created (ID: {subtask['id']})")
    print(f"  - parent_id: {subtask['parent_id']}")
    assert subtask['parent_id'] == parent_id, "Subtask should have correct parent_id"

    # Test 3: Get subtasks
    print("\n[TEST 3] Getting subtasks...")
    subtasks = storage.get_subtasks(parent_id)
    print(f"[OK] Found {len(subtasks)} subtask(s)")
    assert len(subtasks) == 1, "Should find 1 subtask"

    # Test 4: Get root tasks
    print("\n[TEST 4] Getting root tasks...")
    root_tasks = storage.get_root_tasks()
    print(f"[OK] Found {len(root_tasks)} root task(s)")
    assert parent_id in [t['id'] for t in root_tasks], "Parent should be in root tasks"
    assert subtask['id'] not in [t['id'] for t in root_tasks], "Subtask should not be in root tasks"

    # Test 5: Subtask completion ratio
    print("\n[TEST 5] Testing subtask completion ratio...")
    completed, total = storage.get_subtask_completion_ratio(parent_id)
    print(f"[OK] Completion ratio: {completed}/{total}")
    assert completed == 0 and total == 1, "Should be 0/1 initially"

    # Mark subtask complete
    storage.mark_task_complete(subtask['id'], force=True)
    completed, total = storage.get_subtask_completion_ratio(parent_id)
    print(f"[OK] After completion: {completed}/{total}")
    assert completed == 1 and total == 1, "Should be 1/1 after completion"

    # Test 6: Enforce max depth (2 levels)
    print("\n[TEST 6] Testing max depth enforcement...")
    result = storage.add_subtask(subtask['id'], "Invalid nested subtask", "low", "work")
    print(f"[OK] Attempt to create 3rd level subtask: {result}")
    assert result == False, "Should reject 3rd level subtask"

    # Test 7: Set dependencies
    print("\n[TEST 7] Setting task dependencies...")
    storage.add_task("Task A", "high", "work")
    storage.add_task("Task B depends on A", "medium", "work")
    tasks = storage.get_all_tasks()
    task_a_id = tasks[-2]['id']
    task_b_id = tasks[-1]['id']

    result = storage.set_dependencies(task_b_id, [task_a_id])
    print(f"[OK] Dependencies set: Task {task_b_id} depends on Task {task_a_id}")
    assert result == True, "Should set dependencies successfully"

    task_b = storage.get_task_by_id(task_b_id)
    assert task_a_id in task_b['depends_on'], "Dependency should be in depends_on list"

    # Test 8: Check dependencies complete
    print("\n[TEST 8] Checking dependencies complete...")
    all_complete, incomplete = storage.check_dependencies_complete(task_b_id)
    print(f"[OK] Dependencies complete: {all_complete}")
    print(f"  - Incomplete tasks: {len(incomplete)}")
    assert all_complete == False, "Dependencies should not be complete"
    assert len(incomplete) == 1, "Should have 1 incomplete dependency"

    # Test 9: Cannot complete task with incomplete dependencies
    print("\n[TEST 9] Testing dependency blocking...")
    result = storage.mark_task_complete(task_b_id, force=False)
    print(f"[OK] Attempt to complete with incomplete dependencies: {result}")
    assert result == False, "Should block completion"

    # Test 10: Can complete after dependencies done
    print("\n[TEST 10] Completing after dependencies met...")
    storage.mark_task_complete(task_a_id, force=True)
    result = storage.mark_task_complete(task_b_id, force=False)
    print(f"[OK] Completion after dependencies met: {result}")
    assert result == True, "Should allow completion"

    # Test 11: Circular dependency detection
    print("\n[TEST 11] Testing circular dependency detection...")
    storage.add_task("Task X", "high", "work")
    storage.add_task("Task Y", "high", "work")
    storage.add_task("Task Z", "high", "work")
    tasks = storage.get_all_tasks()
    x_id = tasks[-3]['id']
    y_id = tasks[-2]['id']
    z_id = tasks[-1]['id']

    # X -> Y
    storage.set_dependencies(x_id, [y_id])
    # Y -> Z
    storage.set_dependencies(y_id, [z_id])
    # Try Z -> X (would create cycle)
    result = storage.set_dependencies(z_id, [x_id])
    print(f"[OK] Circular dependency detected: {result == False}")
    assert result == False, "Should detect circular dependency"

    # Test 12: Self-dependency rejection
    print("\n[TEST 12] Testing self-dependency rejection...")
    result = storage.set_dependencies(x_id, [x_id])
    print(f"[OK] Self-dependency rejected: {result == False}")
    assert result == False, "Should reject self-dependency"

    # Test 13: Remove from dependencies on delete
    print("\n[TEST 13] Testing dependency cleanup on delete...")
    storage.add_task("Task to delete", "low", "other")
    storage.add_task("Dependent task", "low", "other")
    tasks = storage.get_all_tasks()
    delete_id = tasks[-2]['id']
    dependent_id = tasks[-1]['id']

    storage.set_dependencies(dependent_id, [delete_id])
    dependent = storage.get_task_by_id(dependent_id)
    assert delete_id in dependent['depends_on'], "Dependency should be set"

    # Delete the task
    storage.delete_task(delete_id)
    dependent = storage.get_task_by_id(dependent_id)
    print(f"[OK] Dependencies after delete: {dependent['depends_on']}")
    assert delete_id not in dependent['depends_on'], "Dependency should be removed"

    # Test 14: Delete parent deletes subtasks
    print("\n[TEST 14] Testing cascading delete of subtasks...")
    storage.add_task("Parent to delete", "low", "other")
    tasks = storage.get_all_tasks()
    parent_del_id = tasks[-1]['id']

    storage.add_subtask(parent_del_id, "Subtask to delete", "low", "other")
    tasks = storage.get_all_tasks()
    subtask_del_id = tasks[-1]['id']

    # Verify subtask exists
    assert storage.get_task_by_id(subtask_del_id) is not None, "Subtask should exist"

    # Delete parent
    storage.delete_task(parent_del_id)

    # Verify both are deleted
    print(f"[OK] Parent deleted")
    assert storage.get_task_by_id(parent_del_id) is None, "Parent should be deleted"
    assert storage.get_task_by_id(subtask_del_id) is None, "Subtask should be deleted"

    # Test 15: Multiple dependencies
    print("\n[TEST 15] Testing multiple dependencies...")
    storage.add_task("Dep 1", "high", "work")
    storage.add_task("Dep 2", "high", "work")
    storage.add_task("Task with multiple deps", "high", "work")
    tasks = storage.get_all_tasks()
    dep1_id = tasks[-3]['id']
    dep2_id = tasks[-2]['id']
    multi_dep_id = tasks[-1]['id']

    result = storage.set_dependencies(multi_dep_id, [dep1_id, dep2_id])
    print(f"[OK] Set 2 dependencies: {result}")
    assert result == True, "Should set multiple dependencies"

    task = storage.get_task_by_id(multi_dep_id)
    assert len(task['depends_on']) == 2, "Should have 2 dependencies"

    print("\n" + "=" * 60)
    print("ALL PHASE 3.3 TESTS PASSED!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  - Total tasks: {len(storage.get_all_tasks())}")
    print(f"  - Root tasks: {len(storage.get_root_tasks())}")
    print(f"  - Tasks with dependencies: {sum(1 for t in storage.get_all_tasks() if t['depends_on'])}")
    print(f"  - Subtasks: {sum(1 for t in storage.get_all_tasks() if t['parent_id'] is not None)}")

if __name__ == "__main__":
    test_phase3_3()
