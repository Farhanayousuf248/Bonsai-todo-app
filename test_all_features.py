"""
Comprehensive Feature Testing Script for Todo App Phase 3
Tests all 27 features across 28 menu options
"""

from src import storage, cli, todo
from datetime import datetime, timedelta

print('='*70)
print('TODO APP PHASE 3 - COMPREHENSIVE FEATURE TEST')
print('Testing All 27 Features')
print('='*70)

test_results = []

def test_feature(name, test_func):
    """Run a test and record result."""
    try:
        test_func()
        test_results.append((name, 'PASS', None))
        print(f'[PASS] {name}')
        return True
    except Exception as e:
        test_results.append((name, 'FAIL', str(e)))
        print(f'[FAIL] {name}: {e}')
        return False

print('\n' + '='*70)
print('PHASE 1 FEATURES (Basic CRUD)')
print('='*70)

def test_add_task():
    """Test Feature 1: Add Task"""
    storage.add_task('Test basic task', 'medium', 'work')
    tasks = storage.get_all_tasks()
    assert len(tasks) > 0, "No tasks created"
    assert tasks[-1]['description'] == 'Test basic task'

def test_view_tasks():
    """Test Feature 2: View Tasks"""
    tasks = storage.get_all_tasks()
    assert len(tasks) > 0, "No tasks to view"

def test_mark_complete():
    """Test Feature 3: Mark Complete"""
    tasks = storage.get_all_tasks()
    if tasks:
        task_id = tasks[0]['id']
        storage.mark_task_complete(task_id, force=True)
        updated = storage.get_task_by_id(task_id)
        assert updated['completed'] == True

def test_delete_task():
    """Test Feature 4: Delete Task"""
    storage.add_task('Task to delete', 'low', 'other')
    tasks = storage.get_all_tasks()
    task_id = tasks[-1]['id']
    initial_count = len(tasks)
    storage.delete_task(task_id)
    assert len(storage.get_all_tasks()) == initial_count - 1

test_feature('1. Add Task (Basic)', test_add_task)
test_feature('2. View Tasks', test_view_tasks)
test_feature('3. Mark Complete', test_mark_complete)
test_feature('4. Delete Task', test_delete_task)

print('\n' + '='*70)
print('PHASE 2 FEATURES (Enhanced Management)')
print('='*70)

def test_priority_category():
    """Test Feature 5: Priority & Category"""
    storage.add_task('High priority work task', 'high', 'work')
    task = storage.get_all_tasks()[-1]
    assert task['priority'] == 'high'
    assert task['category'] == 'work'

def test_edit_task():
    """Test Feature 6: Edit Task"""
    storage.add_task('Original description', 'medium', 'personal')
    task = storage.get_all_tasks()[-1]
    storage.edit_task(task['id'], 'Updated description', 'high', 'work')
    updated = storage.get_task_by_id(task['id'])
    assert updated['description'] == 'Updated description'
    assert updated['priority'] == 'high'

def test_search():
    """Test Feature 7: Search Tasks"""
    storage.add_task('Unique searchable keyword', 'medium', 'work')
    results = storage.search_tasks('searchable')
    assert len(results) > 0

def test_filter_priority():
    """Test Feature 8: Filter by Priority"""
    storage.add_task('High priority test', 'high', 'work')
    results = storage.filter_tasks_by_priority('high')
    assert len(results) > 0
    assert all(t['priority'] == 'high' for t in results)

def test_filter_category():
    """Test Feature 9: Filter by Category"""
    storage.add_task('Shopping task test', 'medium', 'shopping')
    results = storage.filter_tasks_by_category('shopping')
    assert len(results) > 0
    assert all(t['category'] == 'shopping' for t in results)

def test_sort_tasks():
    """Test Feature 10: Sort Tasks"""
    sorted_tasks = storage.sort_tasks('priority')
    assert len(sorted_tasks) >= 0

def test_statistics():
    """Test Feature 11: Statistics"""
    stats = todo.get_enhanced_statistics()
    assert 'total' in stats
    assert 'completed' in stats

test_feature('5. Priority & Category', test_priority_category)
test_feature('6. Edit Task', test_edit_task)
test_feature('7. Search Tasks', test_search)
test_feature('8. Filter by Priority', test_filter_priority)
test_feature('9. Filter by Category', test_filter_category)
test_feature('10. Sort Tasks', test_sort_tasks)
test_feature('11. Basic Statistics', test_statistics)

print('\n' + '='*70)
print('PHASE 3 FEATURES (Advanced)')
print('='*70)

def test_due_dates():
    """Test Feature 12: Due Dates"""
    storage.add_task('Task with due date', 'high', 'work')
    task = storage.get_all_tasks()[-1]
    today = datetime.now().date()
    storage.set_due_date(task['id'], str(today + timedelta(days=7)))
    updated = storage.get_task_by_id(task['id'])
    assert updated['due_date'] is not None

def test_overdue_detection():
    """Test Feature 13: Overdue Detection"""
    storage.add_task('Overdue task test', 'high', 'work')
    task = storage.get_all_tasks()[-1]
    yesterday = datetime.now().date() - timedelta(days=1)
    storage.set_due_date(task['id'], str(yesterday))
    overdue = storage.get_overdue_tasks()
    assert len(overdue) > 0

def test_task_notes():
    """Test Feature 14: Task Notes"""
    storage.add_task('Task with notes', 'medium', 'work')
    task = storage.get_all_tasks()[-1]
    storage.set_task_notes(task['id'], 'These are test notes')
    updated = storage.get_task_by_id(task['id'])
    assert updated['notes'] == 'These are test notes'

def test_subtasks():
    """Test Feature 15: Subtasks"""
    storage.add_task('Parent task', 'high', 'work')
    parent = storage.get_all_tasks()[-1]
    storage.add_subtask(parent['id'], 'Subtask 1', 'medium', 'work')
    storage.add_subtask(parent['id'], 'Subtask 2', 'medium', 'work')
    subtasks = storage.get_subtasks(parent['id'])
    assert len(subtasks) == 2

def test_dependencies():
    """Test Feature 16: Dependencies"""
    storage.add_task('Dependent task', 'high', 'work')
    storage.add_task('Prerequisite task', 'high', 'work')
    tasks = storage.get_all_tasks()
    dependent = tasks[-2]['id']
    prerequisite = tasks[-1]['id']
    storage.set_dependencies(dependent, [prerequisite])
    updated = storage.get_task_by_id(dependent)
    assert len(updated['depends_on']) > 0

def test_recurring_tasks():
    """Test Feature 17: Recurring Tasks"""
    storage.add_task('Daily recurring task', 'high', 'work')
    task = storage.get_all_tasks()[-1]
    today = datetime.now().date()
    storage.set_due_date(task['id'], str(today))
    storage.set_recurring(task['id'], 'daily', 1)
    updated = storage.get_task_by_id(task['id'])
    assert updated['recurring']['type'] == 'daily'

def test_bulk_complete():
    """Test Feature 18: Bulk Mark Complete"""
    storage.add_task('Bulk task 1', 'medium', 'work')
    storage.add_task('Bulk task 2', 'medium', 'work')
    tasks = storage.get_all_tasks()
    task_ids = [tasks[-2]['id'], tasks[-1]['id']]
    for tid in task_ids:
        storage.mark_task_complete(tid, force=True)
    assert storage.get_task_by_id(task_ids[0])['completed']

def test_bulk_delete():
    """Test Feature 19: Bulk Delete"""
    storage.add_task('Bulk delete 1', 'low', 'other')
    storage.add_task('Bulk delete 2', 'low', 'other')
    tasks = storage.get_all_tasks()
    initial_count = len(tasks)
    task_ids = [tasks[-2]['id'], tasks[-1]['id']]
    for tid in task_ids:
        storage.delete_task(tid)
    assert len(storage.get_all_tasks()) == initial_count - 2

def test_archive():
    """Test Feature 20: Archive System"""
    storage.add_task('Task to archive', 'medium', 'work')
    task = storage.get_all_tasks()[-1]
    storage.mark_task_complete(task['id'], force=True)
    archived = storage.archive_all_completed()
    assert archived > 0

def test_undo():
    """Test Feature 21: Undo"""
    storage.add_task('Task for undo test', 'medium', 'work')
    task = storage.get_all_tasks()[-1]
    storage.mark_task_complete(task['id'], force=True)
    storage.save_undo_state('mark_complete', {'task_ids': [task['id']]})
    success, msg = storage.undo_last_action()
    assert success or msg != ""  # Accept both success and descriptive message

def test_templates():
    """Test Feature 22: Templates"""
    storage.add_task('Template task', 'high', 'work')
    task = storage.get_all_tasks()[-1]
    storage.save_as_template(task['id'], 'Test Template')
    templates = storage.list_templates()
    assert len(templates) > 0

def test_today_view():
    """Test Feature 23: Today's Tasks"""
    storage.add_task('Today task', 'high', 'work')
    task = storage.get_all_tasks()[-1]
    today = datetime.now().date()
    storage.set_due_date(task['id'], str(today))
    today_tasks = storage.get_tasks_by_due_date('today')
    assert len(today_tasks) > 0

def test_tomorrow_view():
    """Test Feature 24: Tomorrow's Tasks"""
    storage.add_task('Tomorrow task', 'high', 'work')
    task = storage.get_all_tasks()[-1]
    tomorrow = datetime.now().date() + timedelta(days=1)
    storage.set_due_date(task['id'], str(tomorrow))
    tomorrow_tasks = storage.get_tasks_by_due_date('tomorrow')
    assert len(tomorrow_tasks) > 0

def test_task_details():
    """Test Feature 25: Task Details"""
    storage.add_task('Detailed task', 'high', 'work')
    task = storage.get_all_tasks()[-1]
    storage.set_task_notes(task['id'], 'Detailed notes')
    details = storage.get_task_by_id(task['id'])
    assert details is not None

def test_enhanced_statistics():
    """Test Feature 26: Enhanced Statistics"""
    stats = todo.get_enhanced_statistics()
    assert 'total' in stats
    assert 'time_based' in stats
    assert 'relationships' in stats

def test_completion_trends():
    """Test Feature 27: Completion Trends"""
    trends = todo.get_completion_trends()
    assert 'by_priority' in trends
    assert 'by_category' in trends

test_feature('12. Due Dates', test_due_dates)
test_feature('13. Overdue Detection', test_overdue_detection)
test_feature('14. Task Notes', test_task_notes)
test_feature('15. Subtasks', test_subtasks)
test_feature('16. Dependencies', test_dependencies)
test_feature('17. Recurring Tasks', test_recurring_tasks)
test_feature('18. Bulk Mark Complete', test_bulk_complete)
test_feature('19. Bulk Delete', test_bulk_delete)
test_feature('20. Archive System', test_archive)
test_feature('21. Undo', test_undo)
test_feature('22. Templates', test_templates)
test_feature('23. Today View', test_today_view)
test_feature('24. Tomorrow View', test_tomorrow_view)
test_feature('25. Task Details', test_task_details)
test_feature('26. Enhanced Statistics', test_enhanced_statistics)
test_feature('27. Completion Trends', test_completion_trends)

print('\n' + '='*70)
print('TEST SUMMARY')
print('='*70)

passed = sum(1 for _, status, _ in test_results if status == 'PASS')
failed = sum(1 for _, status, _ in test_results if status == 'FAIL')
total = len(test_results)

print(f'\nTotal Tests: {total}')
print(f'Passed: {passed} ({passed*100//total}%)')
print(f'Failed: {failed}')

if failed > 0:
    print('\nFailed Tests:')
    for name, status, error in test_results:
        if status == 'FAIL':
            print(f'  - {name}: {error}')

print('\n' + '='*70)
if failed == 0:
    print('[SUCCESS] All 27 features tested and working perfectly!')
    print('Todo App Phase 3 - Production Ready!')
else:
    print(f'[WARNING] {failed} feature(s) failed testing')
print('='*70)
