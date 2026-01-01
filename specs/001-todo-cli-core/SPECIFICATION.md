# Todo App Phase 1 - Specification Document

**Project**: Todo App Phase 1
**Maintainer**: Farhana Yousuf (GIAIC)
**Document Status**: Draft
**Last Updated**: 2025-12-31

---

## 1. Project Overview

### 1.1 Purpose
A command-line Todo application for managing daily tasks with in-memory storage, built using Python standard library only.

### 1.2 Constitutional Constraints
- **CLI Only**: No GUI, web interface, or external UI frameworks
- **In-Memory Only**: No file persistence, no databases
- **Python Standard Library Only**: No external packages or frameworks
- **Workflow**: Strict adherence to constitution → specification → planning → execution → qa_validation → checklist_verification

---

## 2. Core Features

### 2.1 Feature List
1. **Add Task**: Create a new todo task with description
2. **View Tasks**: Display all tasks with their status
3. **Mark Task Complete**: Toggle task completion status
4. **Delete Task**: Remove a task from the list
5. **Exit Application**: Gracefully exit the program

### 2.2 Feature Priority
- **Must Have**: Add, View, Mark Complete, Exit
- **Should Have**: Delete Task
- **Nice to Have**: Edit Task (Phase 2)

---

## 3. Data Structure

### 3.1 Task Object
Each task will be represented as a dictionary with the following structure:

```python
{
    "id": int,           # Unique identifier (auto-increment)
    "description": str,  # Task description
    "completed": bool,   # Completion status (True/False)
    "created_at": str    # ISO format timestamp
}
```

### 3.2 Task Storage
- **Container**: Python list storing task dictionaries
- **Scope**: Module-level variable (in-memory)
- **Lifecycle**: Exists only during program execution

### 3.3 ID Management
- Auto-incrementing integer starting from 1
- IDs are never reused even after task deletion
- ID counter maintains state during application runtime

---

## 4. User Interface

### 4.1 Main Menu
```
===== TODO APP =====
1. Add Task
2. View Tasks
3. Mark Task Complete
4. Delete Task
5. Exit

Enter your choice (1-5):
```

### 4.2 Menu Flow

#### 4.2.1 Add Task Flow
```
Enter your choice (1-5): 1
Enter task description: Buy groceries
✓ Task added successfully! (ID: 1)

[Return to main menu]
```

#### 4.2.2 View Tasks Flow
```
Enter your choice (1-5): 2

===== YOUR TASKS =====
1. [ ] Buy groceries (Created: 2025-12-31 10:30:00)
2. [✓] Complete assignment (Created: 2025-12-31 09:15:00)

Total: 2 tasks (1 pending, 1 completed)

[Return to main menu]
```

#### 4.2.3 Mark Task Complete Flow
```
Enter your choice (1-5): 3
Enter task ID to mark complete: 1
✓ Task marked as complete!

[Return to main menu]
```

#### 4.2.4 Delete Task Flow
```
Enter your choice (1-5): 4
Enter task ID to delete: 2
✓ Task deleted successfully!

[Return to main menu]
```

#### 4.2.5 Exit Flow
```
Enter your choice (1-5): 5
Thank you for using Todo App! Goodbye!

[Application terminates]
```

---

## 5. Validation Rules

### 5.1 Input Validation

#### Menu Choice
- **Valid**: Integers 1-5
- **Invalid**: Non-integers, out-of-range numbers, empty input
- **Error Message**: "Invalid choice. Please enter a number between 1 and 5."

#### Task Description
- **Valid**: Non-empty string (after stripping whitespace)
- **Invalid**: Empty string, only whitespace
- **Error Message**: "Task description cannot be empty."
- **Max Length**: 200 characters (recommended)

#### Task ID
- **Valid**: Positive integer matching existing task ID
- **Invalid**: Non-integer, negative, zero, non-existent ID
- **Error Messages**:
  - "Invalid input. Please enter a valid task ID."
  - "Task with ID {id} not found."

### 5.2 State Validation
- Attempting to mark already completed task: Show warning "Task is already completed."
- Attempting to delete non-existent task: Show error "Task with ID {id} not found."

---

## 6. Edge Cases

### 6.1 Empty Task List
- **Scenario**: User selects "View Tasks" when no tasks exist
- **Behavior**: Display "No tasks found. Add your first task!"

### 6.2 Invalid Input Handling
- **Non-numeric menu input**: Catch ValueError, prompt again
- **Out-of-range menu choice**: Show error, prompt again
- **Empty task description**: Reject, prompt again
- **Non-numeric task ID**: Catch ValueError, prompt again

### 6.3 Duplicate Operations
- **Mark completed task again**: Allow (idempotent), show info message
- **Delete already deleted task**: Show error (ID no longer exists)

### 6.4 Whitespace Handling
- **Leading/trailing spaces in description**: Strip before saving
- **Multiple spaces in description**: Preserve (user intent)

---

## 7. Error Handling

### 7.1 Error Categories

#### User Input Errors
- Invalid menu choice
- Empty task description
- Invalid task ID format
- Non-existent task ID

#### System Errors
- Keyboard interrupt (Ctrl+C): Graceful exit with message
- Unexpected exceptions: Catch, log, continue operation

### 7.2 Error Response Pattern
```
[ERROR] {Clear error message}
{Suggested action or retry prompt}
```

---

## 8. Non-Functional Requirements

### 8.1 Usability
- Clear, concise menu text
- Consistent formatting
- Immediate feedback for all actions
- No ambiguous prompts

### 8.2 Performance
- Instant response for all operations (in-memory)
- No delays or loading states

### 8.3 Maintainability
- Clean, readable code
- Single Responsibility Principle for functions
- Clear function/variable naming
- Minimal comments (self-documenting code)

### 8.4 Code Quality
- No code duplication
- Functions under 20 lines where possible
- Maximum cyclomatic complexity: 5 per function
- Clear separation of concerns

---

## 9. Out of Scope (Phase 1)

The following features are explicitly NOT included in Phase 1:

- ❌ Task editing/updating
- ❌ Task priorities
- ❌ Task categories/tags
- ❌ Due dates or reminders
- ❌ Task searching/filtering
- ❌ Data persistence (file/database)
- ❌ Multi-user support
- ❌ Task sorting
- ❌ Undo/redo functionality
- ❌ Configuration file
- ❌ Color output/styling
- ❌ Task notes or metadata

---

## 10. Acceptance Criteria

### 10.1 Feature Acceptance

#### Add Task
- ✓ User can add task with description
- ✓ Task receives unique ID
- ✓ Empty descriptions are rejected
- ✓ Confirmation message displayed

#### View Tasks
- ✓ All tasks displayed with ID, status, description, timestamp
- ✓ Completed tasks marked with [✓]
- ✓ Pending tasks marked with [ ]
- ✓ Summary shows total/pending/completed counts
- ✓ Empty list shows helpful message

#### Mark Complete
- ✓ User can mark task complete by ID
- ✓ Status updates from pending to complete
- ✓ Invalid IDs show error message
- ✓ Confirmation message displayed

#### Delete Task
- ✓ User can delete task by ID
- ✓ Task removed from list
- ✓ Invalid IDs show error message
- ✓ Confirmation message displayed

#### Exit
- ✓ Application exits gracefully
- ✓ Goodbye message displayed
- ✓ No error or traceback

### 10.2 Quality Acceptance
- ✓ No crashes on invalid input
- ✓ All inputs validated
- ✓ Clear error messages
- ✓ Consistent UI formatting
- ✓ Code follows PEP 8 style guide
- ✓ No external dependencies

---

## 11. Success Metrics

### 11.1 Functional Metrics
- All 5 menu options work correctly
- Zero crashes during normal operation
- 100% input validation coverage

### 11.2 Code Quality Metrics
- Python standard library only (0 pip packages)
- Functions average < 15 lines
- No code duplication
- Clear variable/function names

---

## 12. Assumptions

1. User has Python 3.6+ installed
2. User runs application from command line
3. User understands basic CLI interaction
4. No concurrent users (single session)
5. Application lifetime = single execution
6. No data needs to persist between runs
7. English language only
8. ASCII character support sufficient

---

## 13. Dependencies

### 13.1 Python Standard Library Modules (Allowed)
- `datetime` - For timestamp generation
- `sys` - For clean exit handling
- `os` - For screen clearing (optional)

### 13.2 Prohibited Dependencies
- No pip packages
- No external libraries
- No frameworks
- No database drivers
- No file I/O libraries (for persistence)

---

## 14. Glossary

- **Task**: A single todo item with description and completion status
- **Task ID**: Unique integer identifier for each task
- **Pending**: Task that is not yet completed (completed=False)
- **Completed**: Task that is marked as done (completed=True)
- **In-Memory**: Data stored in RAM, lost when program exits
- **CLI**: Command Line Interface

---

## 15. Approval & Sign-off

**Specification Status**: Ready for Planning Phase

**Next Step**: Create execution plan following this specification

**Constitutional Compliance**: ✓ Verified
- ✓ CLI only
- ✓ In-memory only
- ✓ Python standard library only
- ✓ No databases, files, or frameworks
- ✓ Specification completed before planning

---

**Document Version**: 1.0
**Prepared By**: Claude Code
**Approved By**: [Pending User Approval]
