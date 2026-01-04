# Todo App Phase 2 - Specification Document

**Project**: Todo App Phase 2
**Maintainer**: Farhana Yousuf (GIAIC)
**Document Status**: Draft
**Created**: 2025-12-31
**Based On**: Phase 1 v1.0 (Complete)

---

## 1. Project Overview

### 1.1 Purpose
Extend the Todo App Phase 1 with enhanced features including task editing, priorities, categories, search/filter capabilities, and task sorting while maintaining constitutional compliance.

### 1.2 Phase 1 Foundation
Phase 2 builds upon the completed Phase 1 which includes:
- ✓ Add Task
- ✓ View Tasks
- ✓ Mark Task Complete
- ✓ Delete Task
- ✓ Exit Application

### 1.3 Constitutional Constraints (Maintained)
- **CLI Only**: No GUI, web interface, or external UI frameworks
- **In-Memory Only**: No file persistence, no databases
- **Python Standard Library Only**: No external packages or frameworks
- **Workflow**: Strict adherence to constitution → specification → planning → execution → qa_validation → checklist_verification

---

## 2. Phase 2 New Features

### 2.1 Feature List

#### Priority Features (Must Have)
1. **Edit Task** - Update existing task descriptions
2. **Task Priorities** - Assign High/Medium/Low priority to tasks
3. **Search Tasks** - Find tasks by keyword in description
4. **View by Priority** - Filter tasks by priority level
5. **View by Status** - Filter tasks by completion status

#### Secondary Features (Should Have)
6. **Task Categories** - Assign categories (Work, Personal, Shopping, Other)
7. **Sort Tasks** - Sort by ID, priority, or creation date
8. **Task Statistics** - Show detailed statistics and insights

#### Nice to Have Features (Phase 3 candidates)
- Due dates and reminders
- Task notes/metadata
- Undo/redo functionality
- Color output (optional, with fallback)

---

## 3. Enhanced Data Structure

### 3.1 Updated Task Object
```python
{
    "id": int,              # Unique identifier (unchanged)
    "description": str,     # Task description (unchanged)
    "completed": bool,      # Completion status (unchanged)
    "created_at": str,      # ISO format timestamp (unchanged)
    "priority": str,        # NEW: "high", "medium", "low"
    "category": str         # NEW: "work", "personal", "shopping", "other"
}
```

### 3.2 Default Values
- **priority**: "medium" (default for new tasks)
- **category**: "other" (default for new tasks)

### 3.3 Backward Compatibility
- Phase 1 tasks will be migrated with default priority="medium" and category="other"
- All Phase 1 functions remain operational

---

## 4. New Menu Structure

### 4.1 Main Menu (Expanded)
```
===== TODO APP (Phase 2) =====
1. Add Task
2. View All Tasks
3. Mark Task Complete
4. Delete Task
5. Edit Task
6. Search Tasks
7. Filter by Priority
8. Filter by Category
9. Sort Tasks
10. Task Statistics
11. Exit

Enter your choice (1-11):
```

### 4.2 Menu Flows

#### 4.2.1 Add Task Flow (Enhanced)
```
Enter your choice: 1
Enter task description: Buy groceries
Select priority (h/m/l) [m]: h
Select category:
  1. Work
  2. Personal
  3. Shopping
  4. Other
Enter choice [4]: 3

[SUCCESS] Task added successfully! (ID: 1, Priority: High, Category: Shopping)
```

#### 4.2.2 Edit Task Flow (NEW)
```
Enter your choice: 5
Enter task ID to edit: 1
Current description: Buy groceries
Enter new description (or press Enter to keep): Buy groceries and fruits
Update priority? (y/n) [n]: y
Select priority (h/m/l) [h]: m
Update category? (y/n) [n]: n

[SUCCESS] Task updated successfully!
```

#### 4.2.3 Search Tasks Flow (NEW)
```
Enter your choice: 6
Enter search keyword: grocery
Found 2 matching tasks:

1. [X] Buy groceries (High, Shopping)
5. [ ] Get grocery bags (Low, Shopping)
```

#### 4.2.4 Filter by Priority Flow (NEW)
```
Enter your choice: 7
Select priority to filter:
  1. High
  2. Medium
  3. Low
  4. All
Enter choice [4]: 1

===== HIGH PRIORITY TASKS =====
1. [ ] Complete project report (High, Work)
3. [ ] Doctor appointment (High, Personal)

Total: 2 high priority tasks
```

#### 4.2.5 Filter by Category Flow (NEW)
```
Enter your choice: 8
Select category to filter:
  1. Work
  2. Personal
  3. Shopping
  4. Other
  5. All
Enter choice [5]: 2

===== PERSONAL TASKS =====
2. [ ] Call mom (Medium, Personal)
3. [X] Doctor appointment (High, Personal)

Total: 2 personal tasks
```

#### 4.2.6 Sort Tasks Flow (NEW)
```
Enter your choice: 9
Sort by:
  1. ID (default)
  2. Priority (High → Low)
  3. Creation Date (Newest first)
  4. Creation Date (Oldest first)
Enter choice [1]: 2

===== YOUR TASKS (Sorted by Priority) =====
[HIGH PRIORITY]
1. [ ] Complete project report (Created: 2025-12-31)

[MEDIUM PRIORITY]
2. [ ] Buy groceries (Created: 2025-12-31)

[LOW PRIORITY]
4. [ ] Read book (Created: 2025-12-31)
```

#### 4.2.7 Task Statistics Flow (NEW)
```
Enter your choice: 10

===== TASK STATISTICS =====
Total Tasks: 10
Completed: 3 (30%)
Pending: 7 (70%)

By Priority:
  High: 2 (20%)
  Medium: 5 (50%)
  Low: 3 (30%)

By Category:
  Work: 4 (40%)
  Personal: 3 (30%)
  Shopping: 2 (20%)
  Other: 1 (10%)

Completion Rate by Priority:
  High: 50% (1/2 completed)
  Medium: 20% (1/5 completed)
  Low: 33% (1/3 completed)
```

---

## 5. Validation Rules (Phase 2)

### 5.1 Input Validation

#### Menu Choice
- **Valid**: Integers 1-11
- **Invalid**: Non-integers, out-of-range numbers
- **Error Message**: "Invalid choice. Please enter a number between 1 and 11."

#### Priority Input
- **Valid**: "h", "high", "m", "medium", "l", "low" (case-insensitive)
- **Default**: "m" (medium) if Enter pressed
- **Error Message**: "Invalid priority. Please enter h/m/l."

#### Category Input
- **Valid**: Integers 1-4
- **Default**: 4 (other) if Enter pressed
- **Error Message**: "Invalid category. Please enter a number between 1 and 4."

#### Search Keyword
- **Valid**: Any non-empty string
- **Invalid**: Empty string
- **Error Message**: "Search keyword cannot be empty."

#### Edit Task
- **Empty new description**: Keep existing description
- **Empty responses for priority/category**: Keep existing values

---

## 6. Edge Cases (Phase 2)

### 6.1 New Edge Cases

#### Edit Non-Existent Task
- **Scenario**: User tries to edit task ID that doesn't exist
- **Behavior**: Display error "Task with ID {id} not found."

#### Search with No Results
- **Scenario**: Search keyword matches no tasks
- **Behavior**: Display "No tasks found matching '{keyword}'."

#### Filter with No Results
- **Scenario**: No tasks match selected priority/category
- **Behavior**: Display "No {priority/category} tasks found."

#### Edit Task - Press Enter for All Fields
- **Scenario**: User presses Enter without changing anything
- **Behavior**: Display "No changes made." and return to menu

#### Priority/Category Case Insensitivity
- **Scenario**: User enters "H", "HIGH", "high"
- **Behavior**: All treated as "high" priority

---

## 7. Enhanced Error Handling

### 7.1 New Error Categories

#### Edit Operation Errors
- Invalid task ID for editing
- No changes provided during edit
- Invalid priority format
- Invalid category selection

#### Search Operation Errors
- Empty search keyword
- No results found

#### Filter Operation Errors
- Invalid filter selection
- No tasks match filter criteria

---

## 8. Non-Functional Requirements (Phase 2)

### 8.1 Performance
- All operations remain instant (in-memory)
- Search should handle 1000+ tasks efficiently
- Filter operations should be immediate

### 8.2 Usability
- Default values for all optional inputs
- Clear formatting for priority/category display
- Consistent color/symbol scheme for priorities
- Help text for new features

### 8.3 Backward Compatibility
- Phase 1 functionality remains unchanged
- Existing tasks work with new features
- Menu numbering extended (1-5 becomes 1-11)

---

## 9. Priority and Category Specifications

### 9.1 Priority Levels

| Priority | Short Code | Display Symbol | Sort Order |
|----------|-----------|----------------|------------|
| High | h | [!] | 1 (highest) |
| Medium | m | [-] | 2 |
| Low | l | [~] | 3 (lowest) |

### 9.2 Category Types

| Category | ID | Use Case |
|----------|-----|----------|
| Work | 1 | Professional tasks, meetings, projects |
| Personal | 2 | Personal errands, self-care, family |
| Shopping | 3 | Groceries, purchases, shopping lists |
| Other | 4 | Miscellaneous tasks |

---

## 10. Display Enhancements

### 10.1 Task Display Format (Enhanced)
```
ID. [Status] [Priority] Description (Category, Created: timestamp)

Example:
1. [ ] [!] Complete project report (Work, Created: 2025-12-31 10:30:00)
2. [X] [-] Buy groceries (Shopping, Created: 2025-12-31 09:15:00)
3. [ ] [~] Read book (Personal, Created: 2025-12-31 08:00:00)

Legend:
  Status: [ ] = Pending, [X] = Completed
  Priority: [!] = High, [-] = Medium, [~] = Low
```

### 10.2 Summary Display (Enhanced)
```
Total: 10 tasks (7 pending, 3 completed)
Priority: 2 high, 5 medium, 3 low
Categories: 4 work, 3 personal, 2 shopping, 1 other
```

---

## 11. Out of Scope (Phase 2)

The following features are explicitly NOT included in Phase 2:

- ❌ Due dates or reminders
- ❌ Data persistence (file/database) - remains in-memory only
- ❌ Multi-user support
- ❌ Undo/redo functionality
- ❌ Configuration file
- ❌ Color output (text-only for compatibility)
- ❌ Task notes or detailed metadata
- ❌ Recurring tasks
- ❌ Task dependencies
- ❌ Export/import functionality

---

## 12. Acceptance Criteria (Phase 2)

### 12.1 Edit Task Feature
- ✓ User can edit task description by ID
- ✓ User can update task priority
- ✓ User can update task category
- ✓ User can skip changes by pressing Enter
- ✓ Invalid IDs show error message
- ✓ Confirmation message displayed
- ✓ Original values preserved if not changed

### 12.2 Task Priority Feature
- ✓ All tasks have priority (high/medium/low)
- ✓ New tasks default to medium priority
- ✓ Priority displayed with tasks
- ✓ Priority symbols clear and consistent
- ✓ Case-insensitive priority input

### 12.3 Task Category Feature
- ✓ All tasks have category (work/personal/shopping/other)
- ✓ New tasks default to "other" category
- ✓ Category displayed with tasks
- ✓ Category selection via numbered menu
- ✓ All 4 categories supported

### 12.4 Search Tasks Feature
- ✓ User can search by keyword
- ✓ Search is case-insensitive
- ✓ Search matches partial descriptions
- ✓ Multiple results displayed
- ✓ No results message shown when appropriate
- ✓ Empty search rejected

### 12.5 Filter by Priority Feature
- ✓ User can filter by high/medium/low
- ✓ Filtered tasks displayed correctly
- ✓ No results message shown when appropriate
- ✓ Filter count displayed

### 12.6 Filter by Category Feature
- ✓ User can filter by work/personal/shopping/other
- ✓ Filtered tasks displayed correctly
- ✓ No results message shown when appropriate
- ✓ Filter count displayed

### 12.7 Sort Tasks Feature
- ✓ User can sort by ID
- ✓ User can sort by priority (high to low)
- ✓ User can sort by creation date (newest/oldest)
- ✓ Sorted view displayed correctly
- ✓ Original order preserved in memory

### 12.8 Task Statistics Feature
- ✓ Total task count displayed
- ✓ Completion rate calculated and displayed
- ✓ Priority distribution shown
- ✓ Category distribution shown
- ✓ Completion rate by priority shown
- ✓ Percentages calculated correctly

### 12.9 Backward Compatibility
- ✓ All Phase 1 features still work
- ✓ Phase 1 tasks work with Phase 2 features
- ✓ No breaking changes to existing functionality

### 12.10 Quality Criteria
- ✓ No crashes on invalid input
- ✓ All inputs validated
- ✓ Clear error messages
- ✓ Consistent UI formatting
- ✓ Code follows PEP 8 style guide
- ✓ No external dependencies
- ✓ All functions under 20 lines target
- ✓ In-memory storage maintained

**Total Acceptance Criteria**: 60+ criteria across all features

---

## 13. Success Metrics (Phase 2)

### 13.1 Functional Metrics
- All 11 menu options work correctly
- Zero crashes during normal operation
- 100% input validation coverage
- All Phase 1 features continue working
- All new features functional

### 13.2 Code Quality Metrics
- Python standard library only (0 pip packages)
- Functions average < 20 lines
- No code duplication
- Clear variable/function names
- Comprehensive error handling

### 13.3 Usability Metrics
- Enhanced user experience with new features
- Clear help text and defaults
- Intuitive navigation
- Consistent formatting

---

## 14. Migration from Phase 1

### 14.1 Data Migration
- Existing tasks will receive default values:
  - priority: "medium"
  - category: "other"
- No data loss during migration
- All existing task properties preserved

### 14.2 Function Migration
- All Phase 1 functions remain intact
- New functions added for Phase 2 features
- No breaking changes to existing code

---

## 15. Assumptions (Phase 2)

1. User has Python 3.6+ installed
2. Phase 1 is complete and working
3. User understands Phase 1 functionality
4. In-memory storage remains acceptable
5. No data needs to persist between runs
6. CLI interface sufficient for new features
7. English language only
8. ASCII characters for priority symbols

---

## 16. Dependencies (Phase 2)

### 16.1 Python Standard Library Modules (Allowed)
- `datetime` - For timestamp generation (existing)
- `sys` - For clean exit handling (existing)
- `re` - For search functionality (NEW, optional)

### 16.2 Prohibited Dependencies
- No pip packages
- No external libraries
- No frameworks
- No database drivers
- No file I/O libraries (for persistence)

---

## 17. Implementation Priorities

### 17.1 Phase 2.1 - Core Features (Priority 1)
1. Edit Task
2. Task Priorities
3. Enhanced Add Task (with priority/category)

### 17.2 Phase 2.2 - Search & Filter (Priority 2)
4. Search Tasks
5. Filter by Priority
6. Filter by Category

### 17.3 Phase 2.3 - Advanced Features (Priority 3)
7. Sort Tasks
8. Task Statistics

---

## 18. Approval & Sign-off

**Specification Status**: Ready for Planning Phase

**Next Step**: Create Phase 2 execution plan following this specification

**Constitutional Compliance**: ✓ Verified
- ✓ CLI only
- ✓ In-memory only
- ✓ Python standard library only
- ✓ No databases, files, or frameworks
- ✓ Specification completed before planning

**Phase 1 Compatibility**: ✓ Maintained
- ✓ No breaking changes
- ✓ All Phase 1 features preserved
- ✓ Backward compatible data structure

---

**Document Version**: 1.0
**Prepared By**: Claude Code
**Based On**: Phase 1 Complete (100/100)
**Approved By**: [Pending User Approval]

---

**END OF PHASE 2 SPECIFICATION**
