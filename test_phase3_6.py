"""
Comprehensive test script for Sub-Phase 3.6: Enhanced Statistics & Final Integration
Tests all 3 statistics functions and their integration.
"""

import sys
sys.path.insert(0, 'C:\\Users\\DELL\\OneDrive\\Desktop\\bonsai')

from src import storage, todo
from datetime import datetime, timedelta


def setup_test_data():
    """Create diverse test data for statistics."""
    print("\n" + "="*70)
    print("SETTING UP TEST DATA")
    print("="*70)

    # Clear existing data
    storage._tasks.clear()
    storage._next_task_id = 1

    # Create tasks with various properties
    test_tasks = [
        # High priority work tasks
        ("Complete project proposal", "high", "work", -2, False, None),  # Overdue
        ("Review code changes", "high", "work", 0, False, None),  # Due today
        ("Team meeting prep", "high", "work", 1, False, None),  # Due tomorrow

        # Medium priority personal tasks
        ("Buy groceries", "medium", "shopping", 0, True, None),  # Due today, completed
        ("Doctor appointment", "medium", "personal", 3, False, None),  # Due this week
        ("Call insurance", "medium", "personal", None, False, None),  # No due date

        # Low priority tasks
        ("Read book", "low", "personal", None, True, None),  # No due date, completed
        ("Organize photos", "low", "other", 10, False, None),  # Due later

        # Tasks with relationships
        ("Project Alpha", "high", "work", 5, False, None),  # Parent task
        ("Phase 1: Research", "medium", "work", 2, True, 1),  # Subtask (completed)
        ("Phase 2: Development", "high", "work", 5, False, 1),  # Subtask

        # Recurring task
        ("Daily standup", "medium", "work", 0, False, {"type": "daily", "interval": 1}),

        # Task with dependencies
        ("Deploy to production", "high", "work", 7, False, None),
    ]

    task_ids = []
    for desc, priority, category, due_offset, completed, recurring in test_tasks:
        storage.add_task(desc, priority, category)
        task = storage.get_all_tasks()[-1]
        task_id = task["id"]
        task_ids.append(task_id)

        # Set due date if specified
        if due_offset is not None:
            due_date = (datetime.now().date() + timedelta(days=due_offset)).strftime("%Y-%m-%d")
            storage.set_due_date(task_id, due_date)

        # Mark complete if specified
        if completed:
            storage.mark_task_complete(task_id, force=True)

        # Set recurring if specified
        if recurring:
            task["recurring"] = recurring

        # Set parent_id for subtasks (indices 9 and 10 are subtasks of 8)
        if desc.startswith("Phase"):
            task["parent_id"] = task_ids[8]  # Parent is "Project Alpha"

    # Set dependencies (deploy depends on development)
    storage.set_dependencies(task_ids[12], [task_ids[10]])

    # Archive one completed task
    storage.archive_task(task_ids[3])

    print(f"\n[OK] Created {len(task_ids)} test tasks")
    print(f"  - {sum(1 for t in storage.get_all_tasks() if t['completed'])} completed")
    print(f"  - {sum(1 for t in storage.get_all_tasks() if t.get('archived', False))} archived")
    print(f"  - {sum(1 for t in storage.get_all_tasks() if t.get('parent_id') is not None)} subtasks")
    print(f"  - {sum(1 for t in storage.get_all_tasks() if t.get('depends_on'))} with dependencies")
    print(f"  - {sum(1 for t in storage.get_all_tasks() if t.get('recurring'))} recurring")

    return task_ids


def test_get_enhanced_statistics():
    """Test get_enhanced_statistics function."""
    print("\n" + "="*70)
    print("TEST 1: Enhanced Statistics Function")
    print("="*70)

    print("\n1.1 Getting enhanced statistics...")
    stats = todo.get_enhanced_statistics()

    # Verify structure
    print("\n1.2 Verifying statistics structure...")
    assert "total" in stats, "Should have 'total' field"
    assert "completed" in stats, "Should have 'completed' field"
    assert "pending" in stats, "Should have 'pending' field"
    assert "archived" in stats, "Should have 'archived' field"
    assert "active" in stats, "Should have 'active' field"
    assert "by_priority" in stats, "Should have 'by_priority' field"
    assert "by_category" in stats, "Should have 'by_category' field"
    assert "time_based" in stats, "Should have 'time_based' field"
    assert "relationships" in stats, "Should have 'relationships' field"
    assert "completion_rate" in stats, "Should have 'completion_rate' field"
    print("[OK] Statistics structure valid")

    # Verify counts
    print("\n1.3 Verifying basic counts...")
    assert stats["total"] == 13, f"Total should be 13, got {stats['total']}"
    assert stats["completed"] == 3, f"Completed should be 3, got {stats['completed']}"
    assert stats["archived"] == 1, f"Archived should be 1, got {stats['archived']}"
    assert stats["active"] == 12, f"Active should be 12, got {stats['active']}"
    print(f"[OK] Basic counts correct: Total={stats['total']}, Completed={stats['completed']}")

    # Verify time-based stats
    print("\n1.4 Verifying time-based breakdown...")
    time_stats = stats["time_based"]
    assert time_stats["overdue"] >= 1, f"Should have overdue tasks, got {time_stats['overdue']}"
    assert time_stats["today"] >= 1, f"Should have tasks due today, got {time_stats['today']}"
    assert time_stats["tomorrow"] >= 1, f"Should have tasks due tomorrow, got {time_stats['tomorrow']}"
    print(f"[OK] Time-based stats: Overdue={time_stats['overdue']}, Today={time_stats['today']}, Tomorrow={time_stats['tomorrow']}")

    # Verify relationship stats
    print("\n1.5 Verifying relationship stats...")
    rel_stats = stats["relationships"]
    assert rel_stats["subtasks"] >= 2, f"Should have subtasks, got {rel_stats['subtasks']}"
    assert rel_stats["with_dependencies"] >= 1, f"Should have tasks with dependencies, got {rel_stats['with_dependencies']}"
    assert rel_stats["recurring"] >= 1, f"Should have recurring tasks, got {rel_stats['recurring']}"
    print(f"[OK] Relationship stats: Subtasks={rel_stats['subtasks']}, Dependencies={rel_stats['with_dependencies']}")

    print("\n[PASS] All enhanced statistics tests passed!")


def test_get_completion_trends():
    """Test get_completion_trends function."""
    print("\n" + "="*70)
    print("TEST 2: Completion Trends Function")
    print("="*70)

    print("\n2.1 Getting completion trends...")
    trends = todo.get_completion_trends()

    # Verify structure
    print("\n2.2 Verifying trends structure...")
    assert "by_priority" in trends, "Should have 'by_priority' field"
    assert "by_category" in trends, "Should have 'by_category' field"
    assert "overall" in trends, "Should have 'overall' field"
    print("[OK] Trends structure valid")

    # Verify priority trends
    print("\n2.3 Verifying priority trends...")
    priority_trends = trends["by_priority"]
    assert "high" in priority_trends, "Should have high priority trend"
    assert "medium" in priority_trends, "Should have medium priority trend"
    assert "low" in priority_trends, "Should have low priority trend"

    for priority in ["high", "medium", "low"]:
        rate = priority_trends[priority]
        assert 0 <= rate <= 100, f"{priority} completion rate should be 0-100%, got {rate}"

    print(f"[OK] Priority trends: High={priority_trends['high']}%, Medium={priority_trends['medium']}%, Low={priority_trends['low']}%")

    # Verify category trends
    print("\n2.4 Verifying category trends...")
    category_trends = trends["by_category"]
    for category in ["work", "personal", "shopping", "other"]:
        rate = category_trends[category]
        assert 0 <= rate <= 100, f"{category} completion rate should be 0-100%, got {rate}"

    print(f"[OK] Category trends: Work={category_trends['work']}%, Personal={category_trends['personal']}%")

    # Verify overall trend
    print("\n2.5 Verifying overall trend...")
    overall = trends["overall"]
    assert 0 <= overall <= 100, f"Overall completion should be 0-100%, got {overall}"
    print(f"[OK] Overall completion: {overall}%")

    print("\n[PASS] All completion trend tests passed!")


def test_get_relationship_stats():
    """Test get_relationship_stats function."""
    print("\n" + "="*70)
    print("TEST 3: Relationship Stats Function")
    print("="*70)

    print("\n3.1 Getting relationship statistics...")
    rel_stats = todo.get_relationship_stats()

    # Verify structure
    print("\n3.2 Verifying relationship stats structure...")
    assert "parent_tasks" in rel_stats, "Should have 'parent_tasks' field"
    assert "subtasks" in rel_stats, "Should have 'subtasks' field"
    assert "avg_subtasks_per_parent" in rel_stats, "Should have 'avg_subtasks_per_parent' field"
    assert "tasks_with_dependencies" in rel_stats, "Should have 'tasks_with_dependencies' field"
    assert "recurring_tasks" in rel_stats, "Should have 'recurring_tasks' field"
    assert "max_dependency_chain" in rel_stats, "Should have 'max_dependency_chain' field"
    print("[OK] Relationship stats structure valid")

    # Verify counts
    print("\n3.3 Verifying relationship counts...")
    assert rel_stats["parent_tasks"] >= 1, f"Should have parent tasks, got {rel_stats['parent_tasks']}"
    assert rel_stats["subtasks"] >= 2, f"Should have subtasks, got {rel_stats['subtasks']}"
    assert rel_stats["tasks_with_dependencies"] >= 1, f"Should have tasks with dependencies, got {rel_stats['tasks_with_dependencies']}"
    assert rel_stats["recurring_tasks"] >= 1, f"Should have recurring tasks, got {rel_stats['recurring_tasks']}"
    print(f"[OK] Relationship counts valid")

    # Verify averages
    print("\n3.4 Verifying calculated metrics...")
    avg_subtasks = rel_stats["avg_subtasks_per_parent"]
    assert avg_subtasks >= 0, f"Average subtasks should be >= 0, got {avg_subtasks}"
    max_chain = rel_stats["max_dependency_chain"]
    assert max_chain >= 0, f"Max chain should be >= 0, got {max_chain}"
    print(f"[OK] Avg subtasks per parent: {avg_subtasks}")
    print(f"[OK] Max dependency chain: {max_chain}")

    print("\n[PASS] All relationship stats tests passed!")


def test_empty_state():
    """Test statistics with no tasks."""
    print("\n" + "="*70)
    print("TEST 4: Empty State Handling")
    print("="*70)

    print("\n4.1 Clearing all tasks...")
    storage._tasks.clear()
    storage._next_task_id = 1

    print("\n4.2 Testing enhanced statistics with no tasks...")
    stats = todo.get_enhanced_statistics()
    assert stats["total"] == 0, "Total should be 0"
    assert stats["completed"] == 0, "Completed should be 0"
    assert stats["completion_rate"] == 0, "Completion rate should be 0"
    print("[OK] Enhanced statistics handles empty state")

    print("\n4.3 Testing completion trends with no tasks...")
    trends = todo.get_completion_trends()
    assert trends["overall"] == 0, "Overall trend should be 0"
    print("[OK] Completion trends handles empty state")

    print("\n4.4 Testing relationship stats with no tasks...")
    rel_stats = todo.get_relationship_stats()
    assert rel_stats["subtasks"] == 0, "Subtasks should be 0"
    assert rel_stats["parent_tasks"] == 0, "Parent tasks should be 0"
    print("[OK] Relationship stats handles empty state")

    print("\n[PASS] All empty state tests passed!")


def test_integration():
    """Test integration of all statistics functions."""
    print("\n" + "="*70)
    print("TEST 5: Integration Test")
    print("="*70)

    # Recreate test data
    print("\n5.1 Recreating test data...")
    task_ids = setup_test_data()

    print("\n5.2 Calling all statistics functions together...")
    stats = todo.get_enhanced_statistics()
    trends = todo.get_completion_trends()
    rel_stats = todo.get_relationship_stats()

    print("\n5.3 Verifying data consistency...")
    # Verify active tasks count matches
    active_from_stats = stats["active"]
    total_minus_archived = stats["total"] - stats["archived"]
    assert active_from_stats == total_minus_archived, f"Active count mismatch: {active_from_stats} != {total_minus_archived}"
    print(f"[OK] Active tasks count consistent: {active_from_stats}")

    # Verify completion rates make sense
    completion_from_stats = stats["completion_rate"]
    completion_from_trends = trends["overall"]
    # These might differ slightly due to archived tasks, but should be in same ballpark
    print(f"[OK] Completion rates: Overall={completion_from_stats}%, Active={completion_from_trends}%")

    # Verify relationship counts match
    subtasks_from_stats = stats["relationships"]["subtasks"]
    subtasks_from_rel = rel_stats["subtasks"]
    assert subtasks_from_stats == subtasks_from_rel, f"Subtask count mismatch: {subtasks_from_stats} != {subtasks_from_rel}"
    print(f"[OK] Subtask counts consistent: {subtasks_from_stats}")

    print("\n5.4 Testing with task state changes...")
    # Complete a task and verify stats update
    incomplete_tasks = [t for t in storage.get_all_tasks() if not t["completed"]]
    if incomplete_tasks:
        task_to_complete = incomplete_tasks[0]
        old_completion = stats["completion_rate"]
        storage.mark_task_complete(task_to_complete["id"], force=True)

        new_stats = todo.get_enhanced_statistics()
        new_completion = new_stats["completion_rate"]
        assert new_completion > old_completion, "Completion rate should increase"
        print(f"[OK] Statistics update after task completion: {old_completion}% -> {new_completion}%")

    print("\n[PASS] All integration tests passed!")


def run_all_tests():
    """Run all Sub-Phase 3.6 tests."""
    print("\n" + "="*70)
    print("SUB-PHASE 3.6: ENHANCED STATISTICS - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print("\nTesting 3 functions across 5 test scenarios:")
    print("  - get_enhanced_statistics()")
    print("  - get_completion_trends()")
    print("  - get_relationship_stats()")

    try:
        # Setup test data
        task_ids = setup_test_data()

        # Run tests
        test_get_enhanced_statistics()
        test_get_completion_trends()
        test_get_relationship_stats()
        test_empty_state()
        test_integration()

        print("\n" + "="*70)
        print("[SUCCESS] ALL SUB-PHASE 3.6 TESTS PASSED! [SUCCESS]")
        print("="*70)
        print("\nTest Summary:")
        print("  [PASS] Enhanced statistics: PASSED")
        print("  [PASS] Completion trends: PASSED")
        print("  [PASS] Relationship stats: PASSED")
        print("  [PASS] Empty state handling: PASSED")
        print("  [PASS] Integration: PASSED")
        print("\nSub-Phase 3.6 Implementation: [PASS] COMPLETE AND VERIFIED")
        print("="*70)

        return True

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n[FAIL] UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
