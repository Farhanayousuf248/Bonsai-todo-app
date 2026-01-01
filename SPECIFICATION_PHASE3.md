# Todo App Phase 3 - Specification Document

**Project**: Todo App Phase 3
**Maintainer**: Farhana Yousuf (GIAIC)
**Document Status**: Draft
**Created**: 2025-12-31
**Based On**: Phase 2 v2.0.0 (Complete)

---

## 1. Project Overview

### 1.1 Purpose
Extend the Todo App Phase 2 with advanced time-based features, task relationships, bulk operations, and enhanced user experience while maintaining constitutional compliance.

### 1.2 Phase 2 Foundation
Phase 3 builds upon the completed Phase 2 which includes:
- ✓ Add Task with Priority & Category
- ✓ View Enhanced Tasks
- ✓ Mark Task Complete
- ✓ Delete Task
- ✓ Edit Task
- ✓ Search Tasks
- ✓ Filter by Priority
- ✓ Filter by Category
- ✓ Sort Tasks
- ✓ Task Statistics

### 1.3 Constitutional Constraints (Maintained)
- **CLI Only**: No GUI, web interface, or external UI frameworks
- **In-Memory Only**: No file persistence, no databases
- **Python Standard Library Only**: No external packages or frameworks
- **Workflow**: Strict adherence to constitution → specification → planning → execution → qa_validation → checklist_verification

---

## 2. Phase 3 New Features

### 2.1 Feature List

#### Priority Features (Must Have)
1. **Due Dates** - Assign and track due dates for tasks
2. **Overdue Detection** - Automatically identify overdue tasks
3. **Task Notes** - Add detailed notes/descriptions to tasks
4. **View Overdue Tasks** - Filter to show only overdue tasks
5. **Bulk Operations** - Mark multiple tasks complete or delete at once

#### Secondary Features (Should Have)
6. **Subtasks** - Create subtasks under parent tasks
7. **Task Dependencies** - Define task dependencies (Task B depends on Task A)
8. **Recurring Tasks** - Set tasks to repeat daily/weekly/monthly
9. **Archive Completed** - Archive completed tasks (remove from main view)
10. **Undo Last Action** - Undo the most recent operation

#### Enhanced User Experience (Nice to Have)
11. **Quick Add** - Add tasks with inline syntax (e.g., "Buy milk !h @work due:2025-01-15")
12. **Today/Tomorrow Views** - Quick filters for tasks due today or tomorrow
13. **Task Templates** - Create and use task templates
14. **Enhanced Statistics** - Time-based analytics and completion trends

---

## 3. Enhanced Data Structure

### 3.1 Updated Task Object
```python
{
    # Phase 1 & 2 Fields (unchanged)
    "id": int,                  # Unique identifier
    "description": str,         # Task description
    "completed": bool,          # Completion status
    "created_at": str,          # ISO format timestamp
    "priority": str,            # "high", "medium", "low"
    "category": str,            # "work", "personal", "shopping", "other"

    # Phase 3 New Fields
    "due_date": str | None,     # ISO date format (YYYY-MM-DD) or None
    "notes": str,               # Multi-line notes (default: "")
    "parent_id": int | None,    # Parent task ID for subtasks (None = root task)
    "depends_on": list[int],    # List of task IDs this task depends on
    "recurring": dict | None,   # Recurring pattern: {"type": "daily|weekly|monthly", "interval": int}
    "archived": bool,           # Archived status (default: False)
    "completed_at": str | None  # ISO timestamp when marked complete
}
```

### 3.2 Default Values
- **due_date**: None (no due date)
- **notes**: "" (empty string)
- **parent_id**: None (root-level task)
- **depends_on**: [] (no dependencies)
- **recurring**: None (one-time task)
- **archived**: False (active task)
- **completed_at**: None (not completed yet)

### 3.3 Backward Compatibility
- Phase 2 tasks will be migrated with Phase 3 default values
- All Phase 1 & 2 functions remain operational
- Archived tasks are hidden from default views but can be accessed

---

## 4. New Menu Structure

### 4.1 Main Menu (Expanded to 20 Options)
```
===== TODO APP (Phase 3) =====

BASIC OPERATIONS:
1.  Add Task
2.  View All Tasks
3.  Mark Task Complete
4.  Delete Task
5.  Edit Task

SEARCH & FILTER:
6.  Search Tasks
7.  Filter by Priority
8.  Filter by Category
9.  View Overdue Tasks
10. View Today's Tasks
11. View Tomorrow's Tasks

ORGANIZATION:
12. Sort Tasks
13. Add Subtask
14. Set Task Dependency
15. Add/Edit Task Notes

BULK OPERATIONS:
16. Bulk Mark Complete
17. Bulk Delete
18. Archive Completed Tasks

ADVANCED:
19. Task Statistics
20. Undo Last Action
21. Exit

Enter your choice (1-21):
```

### 4.2 Quick Add Syntax
Allow users to add tasks with inline formatting:
```
Format: description [!priority] [@category] [due:YYYY-MM-DD] [#notes]

Examples:
- "Complete Phase 3 spec !h @work due:2025-01-05"
- "Buy groceries @shopping due:2025-01-01"
- "Review PR !m @work #Check for edge cases"
```

---

## 5. Feature Specifications

### 5.1 Due Dates

#### 5.1.1 Functional Requirements
- Users can assign a due date when creating or editing a task
- Due dates are in YYYY-MM-DD format
- System validates date format and ensures it's not in the past
- Tasks without due dates are valid (default: None)

#### 5.1.2 User Interface Flow
```
Enter task description: Complete Phase 3 implementation
Priority [m]: h
Category [4]: 1

Add due date? (y/n): y
Enter due date (YYYY-MM-DD): 2025-01-10

[SUCCESS] Task added with due date 2025-01-10!
```

#### 5.1.3 Display Format
```
1. [ ] [!] Complete Phase 3 implementation (Work, Due: 2025-01-10, Created: 2025-12-31)
2. [ ] [-] Review documentation (Work, No due date, Created: 2025-12-31)
```

#### 5.1.4 Acceptance Criteria
- AC-301: Task can be created with due date
- AC-302: Task can be created without due date (None)
- AC-303: Due date format is validated (YYYY-MM-DD)
- AC-304: Past dates are rejected with error message
- AC-305: Due date is displayed in task view
- AC-306: Tasks can be edited to add/change/remove due date

---

### 5.2 Overdue Detection

#### 5.2.1 Functional Requirements
- System automatically detects overdue tasks (due_date < today AND not completed)
- Overdue tasks show special indicator in views
- "View Overdue Tasks" menu option filters only overdue tasks
- Overdue count shown in statistics

#### 5.2.2 User Interface Flow
```
===== OVERDUE TASKS =====
1. [ ] [!] Submit tax documents (Work, Due: 2024-12-15, OVERDUE by 16 days)
2. [ ] [-] Call dentist (Personal, Due: 2024-12-30, OVERDUE by 1 day)

Total: 2 overdue task(s)
```

#### 5.2.3 Display Indicator
```
[ ] [!] Task description (Work, Due: 2024-12-20, OVERDUE by 11 days)
```

#### 5.2.4 Acceptance Criteria
- AC-310: Overdue tasks are correctly identified based on current date
- AC-311: Overdue indicator shows days overdue
- AC-312: Completed tasks are never marked as overdue
- AC-313: View Overdue Tasks menu filters correctly
- AC-314: Tasks without due dates are not marked overdue
- AC-315: Statistics include overdue count

---

### 5.3 Task Notes

#### 5.3.1 Functional Requirements
- Each task can have multi-line notes
- Notes are optional (default: empty string)
- Users can add/edit notes after task creation
- Notes shown in detailed task view but not in list view

#### 5.3.2 User Interface Flow
```
===== ADD/EDIT TASK NOTES =====

Enter task ID: 5

Current task: Complete Phase 3 implementation (High, Work)
Current notes: [None]

Enter notes (type END on a new line to finish):
> This task requires:
> 1. Complete specification document
> 2. Create detailed plan
> 3. Implement all features
> END

[SUCCESS] Notes added to task 5!
```

#### 5.3.3 Display Format
```
===== TASK DETAILS =====
ID: 5
Description: Complete Phase 3 implementation
Status: Pending
Priority: High
Category: Work
Due Date: 2025-01-10
Created: 2025-12-31 18:00:00

Notes:
This task requires:
1. Complete specification document
2. Create detailed plan
3. Implement all features
```

#### 5.3.4 Acceptance Criteria
- AC-320: Notes can be added to any task
- AC-321: Multi-line notes are supported
- AC-322: Notes can be viewed with "View Task Details" option
- AC-323: Notes can be edited and updated
- AC-324: Empty notes are valid
- AC-325: Notes are preserved when editing other task fields

---

### 5.4 Subtasks

#### 5.4.1 Functional Requirements
- Tasks can have child tasks (subtasks)
- Subtasks have a parent_id field
- Subtasks inherit category from parent by default
- Maximum 2 levels deep (parent → subtask only, no nested subtasks)
- Parent task shows subtask completion count

#### 5.4.2 User Interface Flow
```
===== ADD SUBTASK =====

Enter parent task ID: 3

Parent: Complete Phase 3 implementation (High, Work)

Enter subtask description: Write specification document
Priority [m]: h

[SUCCESS] Subtask added! (ID: 10, Parent: 3)
```

#### 5.4.3 Display Format
```
===== YOUR TASKS =====
1. [ ] [!] Complete Phase 3 implementation (Work, Due: 2025-01-10, 2/5 subtasks complete)
   ├─ [X] [-] Write specification document
   ├─ [ ] [-] Create implementation plan
   ├─ [ ] [!] Implement due dates feature
   ├─ [ ] [!] Implement subtasks feature
   └─ [X] [-] Write tests

2. [ ] [-] Review documentation (Work, No subtasks)
```

#### 5.4.4 Acceptance Criteria
- AC-330: Subtasks can be created under parent tasks
- AC-331: Subtasks are displayed indented under parent
- AC-332: Parent shows completion ratio (X/Y subtasks complete)
- AC-333: Subtasks can be marked complete independently
- AC-334: Deleting parent task prompts for subtask handling
- AC-335: Subtasks cannot have their own subtasks (max 2 levels)
- AC-336: Filtering/sorting includes subtasks

---

### 5.5 Task Dependencies

#### 5.5.1 Functional Requirements
- Tasks can depend on other tasks (depends_on: list of task IDs)
- Dependent tasks show warning if dependencies not complete
- Cannot mark task complete if dependencies are incomplete
- Circular dependencies are detected and prevented

#### 5.5.2 User Interface Flow
```
===== SET TASK DEPENDENCY =====

Enter task ID: 8

Current: Deploy to production (High, Work)

Enter dependent task IDs (comma-separated): 5, 6, 7

Task 5: Complete Phase 3 implementation [X]
Task 6: Write tests [ ]
Task 7: Code review [ ]

[SUCCESS] Dependencies set! Task 8 depends on 3 task(s).
```

#### 5.5.3 Attempt to Complete with Incomplete Dependencies
```
Enter task ID: 8

[ERROR] Cannot complete task 8. Incomplete dependencies:
  - Task 6: Write tests (Pending)
  - Task 7: Code review (Pending)

Complete dependencies first, or remove them to proceed.
```

#### 5.5.4 Display Format
```
8. [ ] [!] Deploy to production (Work, Depends on: 3 tasks, 1/3 complete)
```

#### 5.5.5 Acceptance Criteria
- AC-340: Dependencies can be set for any task
- AC-341: Multiple dependencies are supported
- AC-342: System prevents marking task complete if dependencies incomplete
- AC-343: Circular dependencies are detected and rejected
- AC-344: Dependencies are displayed in task view
- AC-345: Deleting a task removes it from other tasks' dependencies
- AC-346: Dependency completion ratio shown in list view

---

### 5.6 Recurring Tasks

#### 5.6.1 Functional Requirements
- Tasks can be set to recur: daily, weekly, monthly
- When marked complete, a new instance is created with updated due date
- Original task shows [RECURRING] indicator
- Recurring interval can be customized (e.g., every 3 days)

#### 5.6.2 User Interface Flow
```
===== ADD RECURRING TASK =====

Enter task description: Weekly team standup
Priority [m]: m
Category [4]: 1
Due date (YYYY-MM-DD): 2025-01-06

Make this recurring? (y/n): y

Recurrence pattern:
1. Daily
2. Weekly
3. Monthly
4. Custom interval

Enter choice: 2

[SUCCESS] Recurring task created! Will repeat every Monday.
```

#### 5.6.3 Marking Complete Behavior
```
Mark task 15 as complete? (y/n): y

[SUCCESS] Task marked complete!
[INFO] New recurring instance created with due date: 2025-01-13
```

#### 5.6.4 Display Format
```
15. [ ] [-] Weekly team standup [RECURRING: Weekly] (Work, Due: 2025-01-06)
```

#### 5.6.5 Acceptance Criteria
- AC-350: Recurring tasks can be created with daily/weekly/monthly patterns
- AC-351: Custom intervals are supported (every N days/weeks/months)
- AC-352: Marking recurring task complete creates new instance
- AC-353: New instance has due date calculated correctly
- AC-354: Recurring indicator shown in views
- AC-355: Recurring tasks can be converted to one-time tasks
- AC-356: Statistics track recurring vs one-time tasks

---

### 5.7 Bulk Operations

#### 5.7.1 Bulk Mark Complete

**User Interface Flow:**
```
===== BULK MARK COMPLETE =====

Current pending tasks:
1. [ ] [!] Write tests (High, Work)
2. [ ] [-] Update documentation (Medium, Work)
3. [ ] [~] Buy groceries (Low, Shopping)

Enter task IDs to mark complete (comma-separated): 1, 2

[SUCCESS] Marked 2 task(s) as complete!
```

**Acceptance Criteria:**
- AC-360: Multiple tasks can be marked complete in one operation
- AC-361: Invalid IDs are skipped with warning
- AC-362: Already complete tasks are skipped with info message
- AC-363: Confirmation count shown after operation

#### 5.7.2 Bulk Delete

**User Interface Flow:**
```
===== BULK DELETE =====

Current tasks:
1. [X] [!] Write tests (High, Work)
2. [X] [-] Update documentation (Medium, Work)
3. [ ] [~] Buy groceries (Low, Shopping)

Enter task IDs to delete (comma-separated): 1, 2

WARNING: You are about to delete 2 task(s). This cannot be undone!
Confirm? (yes/no): yes

[SUCCESS] Deleted 2 task(s)!
```

**Acceptance Criteria:**
- AC-365: Multiple tasks can be deleted in one operation
- AC-366: Confirmation required before deletion
- AC-367: Invalid IDs are skipped with warning
- AC-368: Subtasks handling prompt if deleting parent

#### 5.7.3 Archive Completed Tasks

**User Interface Flow:**
```
===== ARCHIVE COMPLETED TASKS =====

Found 15 completed task(s) ready for archiving.

Archive all completed tasks? (y/n): y

[SUCCESS] Archived 15 task(s)!
[INFO] Archived tasks can be viewed with "View Archived Tasks" option.
```

**Acceptance Criteria:**
- AC-370: All completed tasks can be archived at once
- AC-371: Archived tasks removed from default views
- AC-372: Archived tasks can be viewed separately
- AC-373: Archived tasks can be unarchived
- AC-374: Statistics distinguish active vs archived tasks

---

### 5.8 Undo Last Action

#### 5.8.1 Functional Requirements
- System tracks last operation and can undo it
- Supports undo for: add, delete, mark complete, edit
- Only one level of undo (no redo)
- Clear message shows what will be undone

#### 5.8.2 User Interface Flow
```
===== UNDO LAST ACTION =====

Last action: Deleted task 5 "Complete Phase 3 implementation"
Performed at: 2025-12-31 18:30:15

Undo this action? (y/n): y

[SUCCESS] Action undone! Task 5 restored.
```

#### 5.8.3 Acceptance Criteria
- AC-380: Last action can be undone
- AC-381: Undo description clearly states what will be reversed
- AC-382: Confirmation required before undo
- AC-383: "No action to undo" message if nothing to undo
- AC-384: Bulk operations can be undone as single action

---

### 5.9 Today/Tomorrow Views

#### 5.9.1 View Today's Tasks
```
===== TODAY'S TASKS (2025-12-31) =====

1. [ ] [!] Submit report (Work, Due today)
2. [ ] [-] Call client (Work, Due today)

Total: 2 task(s) due today (0 completed)
```

#### 5.9.2 View Tomorrow's Tasks
```
===== TOMORROW'S TASKS (2025-01-01) =====

1. [ ] [!] Team meeting (Work, Due tomorrow)
2. [ ] [~] Buy groceries (Shopping, Due tomorrow)

Total: 2 task(s) due tomorrow
```

#### 5.9.3 Acceptance Criteria
- AC-390: Today's view shows tasks due on current date
- AC-391: Tomorrow's view shows tasks due on next date
- AC-392: Completed tasks included in today/tomorrow views
- AC-393: Tasks without due dates excluded from these views
- AC-394: Count and completion summary shown

---

### 5.10 Task Templates

#### 5.10.1 Functional Requirements
- Users can save a task as a template
- Templates store: description, priority, category, notes
- Templates can be instantiated to create new tasks
- Templates managed with add/edit/delete/list operations

#### 5.10.2 User Interface Flow
```
===== SAVE AS TEMPLATE =====

Enter task ID: 8

Current: Weekly team standup (Medium, Work)

Enter template name: weekly-standup

[SUCCESS] Template "weekly-standup" saved!

---

===== CREATE FROM TEMPLATE =====

Available templates:
1. weekly-standup
2. code-review
3. client-update

Enter template name: weekly-standup

Loaded: Weekly team standup (Medium, Work)

Modify before creating? (y/n): n
Add due date? (y/n): y
Due date (YYYY-MM-DD): 2025-01-06

[SUCCESS] Task created from template!
```

#### 5.10.3 Acceptance Criteria
- AC-400: Tasks can be saved as templates
- AC-401: Templates can be listed
- AC-402: New tasks can be created from templates
- AC-403: Template values can be modified before creating
- AC-404: Templates can be edited
- AC-405: Templates can be deleted
- AC-406: Templates don't count toward task statistics

---

## 6. Enhanced Statistics

### 6.1 Additional Metrics

#### 6.1.1 Time-Based Statistics
```
===== TASK STATISTICS =====

OVERVIEW:
Total Tasks: 45 (32 active, 13 archived)
Completed: 15 (33%)
Pending: 30 (67%)
Overdue: 5 (11%)

DUE DATE BREAKDOWN:
Today: 3 tasks
Tomorrow: 2 tasks
This Week: 8 tasks
This Month: 15 tasks
No Due Date: 12 tasks

PRIORITY DISTRIBUTION:
High: 12 (27%)
Medium: 20 (44%)
Low: 13 (29%)

CATEGORY DISTRIBUTION:
Work: 25 (56%)
Personal: 10 (22%)
Shopping: 5 (11%)
Other: 5 (11%)

TASK RELATIONSHIPS:
Root Tasks: 30
Subtasks: 15
Tasks with Dependencies: 8
Recurring Tasks: 5

COMPLETION RATE:
Overall: 33%
By Priority:
  High: 50% (6/12)
  Medium: 25% (5/20)
  Low: 31% (4/13)

RECENT ACTIVITY:
Tasks created today: 5
Tasks completed today: 3
Tasks overdue: 5 (oldest: 16 days)
```

#### 6.1.2 Acceptance Criteria
- AC-410: Statistics include time-based breakdowns
- AC-411: Overdue count and oldest overdue shown
- AC-412: Task relationships summarized
- AC-413: Recent activity tracked
- AC-414: Active vs archived stats distinguished

---

## 7. Input Validation & Error Handling

### 7.1 Due Date Validation
- **Valid formats**: YYYY-MM-DD, ISO 8601
- **Invalid inputs**: Past dates (for new tasks), invalid formats, non-existent dates
- **Error messages**: Clear indication of expected format

### 7.2 Dependency Validation
- **Circular dependency check**: A depends on B, B depends on A (reject)
- **Self-dependency check**: Task cannot depend on itself
- **Invalid task IDs**: Show error with available task IDs

### 7.3 Subtask Validation
- **Depth limit**: Maximum 2 levels (no subtasks of subtasks)
- **Parent existence**: Parent task ID must exist
- **Archived parent**: Cannot add subtask to archived task

### 7.4 Bulk Operation Validation
- **Empty input**: Show error if no IDs provided
- **Invalid IDs**: Skip invalid, process valid, show summary
- **Confirmation**: Require explicit confirmation for destructive operations

---

## 8. Display Enhancements

### 8.1 Task List Visual Hierarchy
```
1. [ ] [!] Parent Task (Work, Due: 2025-01-10, 2/3 subtasks complete)
   ├─ [X] [-] First subtask
   ├─ [X] [-] Second subtask
   └─ [ ] [!] Third subtask (Depends on: Task 5)

2. [ ] [-] Independent Task [RECURRING: Weekly] (Personal, Due today, OVERDUE by 2 days)

3. [ ] [~] Simple Task (Shopping, No due date)
```

### 8.2 Status Indicators
- `[ ]` - Pending task
- `[X]` - Completed task
- `[!]` - High priority
- `[-]` - Medium priority
- `[~]` - Low priority
- `[RECURRING: X]` - Recurring task pattern
- `OVERDUE by X days` - Overdue indicator
- `Depends on: X tasks` - Has dependencies
- `X/Y subtasks complete` - Subtask progress

---

## 9. Edge Cases & Business Rules

### 9.1 Due Dates
- **Past dates**: Allowed only when editing existing tasks (e.g., forgot to mark complete)
- **No due date**: Valid for all tasks (None is acceptable)
- **Far future dates**: Accepted without warning

### 9.2 Dependencies
- **Dependency chain**: A → B → C allowed (no circular)
- **Deleting dependency**: Removed from all tasks that depend on it
- **Completing with dependencies**: Blocked until dependencies complete

### 9.3 Subtasks
- **Deleting parent**: Three options: (1) Delete all, (2) Keep subtasks as root, (3) Cancel
- **Maximum depth**: Exactly 2 levels enforced
- **Subtask completion**: Parent shows ratio but can be marked complete independently

### 9.4 Recurring Tasks
- **Marking complete**: Creates new instance with calculated due date
- **Deleting recurring**: Deletes current instance only (future instances not created)
- **No due date**: Recurring tasks must have a due date

### 9.5 Archiving
- **Auto-archive**: Optional setting to auto-archive after X days of completion
- **Unarchive**: Returns task to active view
- **Archived subtasks**: Parent must be archived too

### 9.6 Undo
- **One level only**: No redo, no undo history
- **Bulk operations**: Entire bulk operation undone as one
- **Cannot undo**: View operations, search, filter, sort, statistics

---

## 10. Success Metrics

### 10.1 Functional Completeness
- ✅ All 14 Phase 3 features implemented
- ✅ All 75+ acceptance criteria validated
- ✅ Phase 1 & 2 features remain operational
- ✅ Zero regression bugs

### 10.2 Quality Standards
- ✅ 100% constitutional compliance
- ✅ Zero defects in production
- ✅ All edge cases handled
- ✅ Error messages clear and helpful

### 10.3 Performance Targets
- ✅ All operations < 50ms (in-memory)
- ✅ Handles 500+ tasks efficiently
- ✅ Bulk operations < 100ms for 50 tasks
- ✅ No memory leaks

### 10.4 User Experience
- ✅ Intuitive menu navigation
- ✅ Clear visual hierarchy
- ✅ Helpful prompts and defaults
- ✅ Consistent formatting

---

## 11. Testing Requirements

### 11.1 Unit Tests (150+ tests)
- Due date validation (15 tests)
- Overdue detection (10 tests)
- Subtask operations (20 tests)
- Dependency validation (15 tests)
- Recurring task logic (15 tests)
- Bulk operations (15 tests)
- Undo functionality (10 tests)
- Archive/unarchive (10 tests)
- Task templates (10 tests)
- Enhanced statistics (10 tests)
- All Phase 1 & 2 regression tests (70 tests)

### 11.2 Integration Tests (50+ tests)
- Complete user workflows
- Cross-feature interactions
- Data integrity across operations

### 11.3 Edge Case Tests (40+ tests)
- Boundary conditions
- Invalid inputs
- Error recovery

---

## 12. Phase 3 Implementation Plan Summary

### 12.1 Sub-Phases
1. **Foundation** (Due Dates, Overdue Detection, Notes) - 2 hours
2. **Relationships** (Subtasks, Dependencies) - 3 hours
3. **Automation** (Recurring Tasks, Templates) - 2 hours
4. **Bulk Operations** (Bulk Complete/Delete, Archive, Undo) - 2 hours
5. **Enhanced UX** (Today/Tomorrow Views, Quick Add, Enhanced Stats) - 1.5 hours

### 12.2 Total Estimated Time
- Implementation: 10.5 hours
- Testing: 4 hours
- Documentation: 2 hours
- **Total**: 16.5 hours

---

## 13. Acceptance Criteria Summary

### 13.1 Total Acceptance Criteria: 75

#### Due Dates & Overdue (AC-301 to AC-315): 15 criteria
#### Task Notes (AC-320 to AC-325): 6 criteria
#### Subtasks (AC-330 to AC-336): 7 criteria
#### Dependencies (AC-340 to AC-346): 7 criteria
#### Recurring Tasks (AC-350 to AC-356): 7 criteria
#### Bulk Mark Complete (AC-360 to AC-363): 4 criteria
#### Bulk Delete (AC-365 to AC-368): 4 criteria
#### Archive Operations (AC-370 to AC-374): 5 criteria
#### Undo Functionality (AC-380 to AC-384): 5 criteria
#### Today/Tomorrow Views (AC-390 to AC-394): 5 criteria
#### Task Templates (AC-400 to AC-406): 7 criteria
#### Enhanced Statistics (AC-410 to AC-414): 5 criteria

---

## 14. Risk Assessment

### 14.1 Technical Risks
- **Circular dependency detection**: Complex logic - mitigate with graph algorithms
- **Recurring task creation**: Date calculation edge cases - extensive testing needed
- **Undo state management**: Memory overhead - limit to last action only

### 14.2 Complexity Risks
- **Feature creep**: Too many features - stick to spec, no additions
- **Performance**: More data per task - monitor memory usage, limit to 500 tasks
- **User confusion**: Many options - clear menu organization, help text

### 14.3 Mitigation Strategies
- Thorough testing with edge cases
- Clear user prompts and error messages
- Performance testing with large task sets
- Strict adherence to specification

---

## 15. Future Considerations (Phase 4 Candidates)

These features are explicitly out of scope for Phase 3:

1. **Color output** - Terminal color support (optional with fallback)
2. **Export/Import** - Export tasks to CSV/JSON (breaks in-memory constraint)
3. **Task History** - Full audit log of changes
4. **Multi-user support** - Shared task lists
5. **Task tags** - Multiple tags per task beyond category
6. **Custom fields** - User-defined metadata
7. **Advanced search** - Boolean operators, regex
8. **Task estimates** - Time estimation and tracking
9. **Notifications** - Desktop notifications (requires OS integration)
10. **Calendar integration** - External calendar sync

---

## 16. Glossary

- **Root Task**: Task without a parent (parent_id = None)
- **Subtask**: Task with a parent task (parent_id = valid task ID)
- **Dependency**: Task that must be completed before another can be completed
- **Recurring Task**: Task that creates new instance when marked complete
- **Archived Task**: Completed task hidden from default views
- **Template**: Saved task configuration for quick task creation
- **Bulk Operation**: Action performed on multiple tasks simultaneously
- **Overdue Task**: Task with due date in the past and not completed
- **Quick Add**: Inline syntax for creating tasks with all properties

---

## 17. Approval & Sign-off

### 17.1 Document Review
- [ ] Technical specification complete
- [ ] All acceptance criteria defined
- [ ] Edge cases documented
- [ ] Success metrics clear

### 17.2 Ready for Planning Phase
This specification document must be reviewed and approved before proceeding to the Planning Phase.

**Specification Status**: ✅ **COMPLETE - Ready for Review**

---

**Document Version**: 1.0
**Last Updated**: 2025-12-31
**Next Phase**: Planning (PLAN_PHASE3.md)

---

**End of Specification Document**
