# Todo App Phase 1 - Execution Plan

**Project**: Todo App Phase 1
**Maintainer**: Farhana Yousuf (GIAIC)
**Document Status**: Planning
**Last Updated**: 2025-12-31
**Based On**: SPECIFICATION.md v1.0

---

## 1. Planning Overview

### 1.1 Purpose
This document provides a step-by-step execution plan for implementing the Todo App Phase 1, ensuring constitutional compliance and specification adherence.

### 1.2 Workflow Position
✓ Constitution → ✓ Specification → **→ Planning** → Execution → QA Validation → Checklist Verification

---

## 2. Implementation Strategy

### 2.1 Development Approach
- **Bottom-Up Implementation**: Build core functions first, then integrate
- **Incremental Testing**: Test each function as it's built
- **Single File Structure**: All code in one Python file (todo_app.py)
- **Function-First Design**: Implement utility functions before main loop

### 2.2 File Structure
```
bonsai/
├── SPECIFICATION.md       (✓ Complete)
├── PLAN.md               (Current document)
├── todo_app.py           (To be created)
├── EXECUTION_LOG.md      (To be created during execution)
├── QA_VALIDATION.md      (To be created during QA)
└── CHECKLIST.md          (To be created for verification)
```

---

## 3. Code Architecture

### 3.1 Module-Level Variables
```python
tasks = []           # List to store task dictionaries
next_task_id = 1     # Global counter for task IDs
```

### 3.2 Function Structure (15 functions planned)

#### Core Data Functions
1. `generate_task_id()` → int
   - Returns current ID and increments counter

2. `create_task(description: str)` → dict
   - Creates task dictionary with ID, description, completed=False, timestamp

3. `add_task(description: str)` → bool
   - Validates description, creates task, appends to tasks list
   - Returns True on success, False on failure

4. `get_task_by_id(task_id: int)` → dict or None
   - Searches tasks list for matching ID
   - Returns task dict or None if not found

5. `mark_task_complete(task_id: int)` → bool
   - Finds task by ID, sets completed=True
   - Returns True on success, False if not found

6. `delete_task(task_id: int)` → bool
   - Finds task by ID, removes from list
   - Returns True on success, False if not found

#### Display Functions
7. `display_menu()` → None
   - Prints main menu with options 1-5

8. `display_tasks()` → None
   - Prints all tasks with formatting
   - Shows [✓] for completed, [ ] for pending
   - Displays summary count
   - Handles empty list case

9. `display_success(message: str)` → None
   - Prints success message with ✓ symbol

10. `display_error(message: str)` → None
    - Prints error message with [ERROR] prefix

#### Input Functions
11. `get_menu_choice()` → int
    - Gets user input for menu choice
    - Validates range 1-5
    - Loops until valid input
    - Returns validated integer

12. `get_task_description()` → str
    - Gets user input for task description
    - Strips whitespace
    - Validates non-empty
    - Loops until valid input
    - Returns validated string

13. `get_task_id()` → int
    - Gets user input for task ID
    - Validates integer format
    - Loops until valid input
    - Returns validated integer (existence checked separately)

#### Menu Handler Functions
14. `handle_add_task()` → None
    - Calls get_task_description()
    - Calls add_task()
    - Displays success/error message

15. `handle_view_tasks()` → None
    - Calls display_tasks()

16. `handle_mark_complete()` → None
    - Calls get_task_id()
    - Calls mark_task_complete()
    - Displays success/error message

17. `handle_delete_task()` → None
    - Calls get_task_id()
    - Calls delete_task()
    - Displays success/error message

18. `handle_exit()` → None
    - Displays goodbye message
    - Exits program cleanly

#### Main Function
19. `main()` → None
    - Main application loop
    - Displays menu
    - Gets choice
    - Dispatches to handler
    - Handles KeyboardInterrupt (Ctrl+C)

---

## 4. Step-by-Step Execution Plan

### Phase 1: Project Setup (Steps 1-3)

#### Step 1: Create Main File
**Task**: Create `todo_app.py` with module docstring and imports
**Actions**:
- Create file: `todo_app.py`
- Add module docstring
- Import required modules: `datetime`, `sys`
- Add module-level variables: `tasks`, `next_task_id`

**Validation**: File exists, imports work, no syntax errors

---

#### Step 2: Implement Core Data Functions
**Task**: Implement functions for task management
**Actions**:
- Implement `generate_task_id()`
- Implement `create_task(description)`
- Implement `add_task(description)`
- Implement `get_task_by_id(task_id)`
- Implement `mark_task_complete(task_id)`
- Implement `delete_task(task_id)`

**Validation**: Each function tested individually with sample data

---

#### Step 3: Implement Display Functions
**Task**: Implement all output formatting functions
**Actions**:
- Implement `display_menu()`
- Implement `display_tasks()`
- Implement `display_success(message)`
- Implement `display_error(message)`

**Validation**: Visual inspection of output formatting

---

### Phase 2: User Input & Validation (Steps 4-5)

#### Step 4: Implement Input Functions
**Task**: Implement user input with validation
**Actions**:
- Implement `get_menu_choice()` with try-except for ValueError
- Implement `get_task_description()` with whitespace stripping
- Implement `get_task_id()` with integer validation

**Validation**: Test with valid and invalid inputs

---

#### Step 5: Implement Menu Handlers
**Task**: Create handler functions for each menu option
**Actions**:
- Implement `handle_add_task()`
- Implement `handle_view_tasks()`
- Implement `handle_mark_complete()`
- Implement `handle_delete_task()`
- Implement `handle_exit()`

**Validation**: Test each handler with valid scenarios

---

### Phase 3: Main Application Loop (Step 6)

#### Step 6: Implement Main Function
**Task**: Create main application loop with menu dispatch
**Actions**:
- Implement `main()` function with infinite loop
- Add menu display
- Add choice input
- Add if-elif chain for menu dispatch
- Add KeyboardInterrupt handling
- Add `if __name__ == "__main__":` guard
- Call `main()`

**Validation**: Full application runs without crashes

---

### Phase 4: Testing & Refinement (Steps 7-9)

#### Step 7: Test Happy Path Scenarios
**Task**: Test all features with valid inputs
**Test Cases**:
1. Add 3 tasks successfully
2. View tasks (verify display)
3. Mark task 2 as complete
4. View tasks (verify completed status)
5. Delete task 1
6. View tasks (verify deletion)
7. Exit application

**Validation**: All operations work as specified

---

#### Step 8: Test Edge Cases
**Task**: Test error handling and edge cases
**Test Cases**:
1. View tasks when list is empty
2. Mark complete with non-existent ID
3. Delete with non-existent ID
4. Add task with empty description
5. Add task with only whitespace
6. Invalid menu choices (0, 6, -1, "abc")
7. Invalid task IDs (0, -1, "abc", 999)
8. Keyboard interrupt (Ctrl+C)

**Validation**: All edge cases handled gracefully

---

#### Step 9: Code Quality Review
**Task**: Review and refine code quality
**Actions**:
- Check for code duplication
- Verify function sizes (< 20 lines target)
- Verify variable naming clarity
- Verify PEP 8 compliance (indentation, spacing)
- Remove unnecessary comments
- Verify no external dependencies

**Validation**: Code is clean, readable, maintainable

---

### Phase 5: Documentation (Step 10)

#### Step 10: Create Execution Log
**Task**: Document what was implemented
**Actions**:
- Create `EXECUTION_LOG.md`
- Document each implementation step
- Note any deviations from plan
- Document actual vs planned effort
- List all functions implemented
- Document test results

**Validation**: Log is complete and accurate

---

## 5. Quality Assurance Strategy

### 5.1 Testing Approach
- **Manual Testing**: All features tested by hand
- **Scenario-Based**: Test realistic user workflows
- **Boundary Testing**: Test limits and edge cases
- **Error Testing**: Test all error paths

### 5.2 Test Scenarios Matrix

| Feature | Valid Input | Invalid Input | Edge Case |
|---------|-------------|---------------|-----------|
| Add Task | "Buy milk" | "" | "   " (whitespace) |
| View Tasks | N/A | N/A | Empty list |
| Mark Complete | Existing ID | Non-existent ID | Already completed |
| Delete Task | Existing ID | Non-existent ID | Last remaining task |
| Menu Choice | 1-5 | 0, 6, "abc" | Ctrl+C |

### 5.3 Acceptance Testing
Each acceptance criterion from SPECIFICATION.md will be tested and verified.

---

## 6. Risk Management

### 6.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Global variable issues | Low | Medium | Proper scoping, clear naming |
| Input validation gaps | Medium | High | Comprehensive try-except blocks |
| ID collision after delete | Low | Medium | Never reuse IDs (incrementing counter) |
| Unicode/encoding issues | Low | Low | Stick to ASCII for Phase 1 |

### 6.2 Process Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scope creep | Medium | High | Strict adherence to specification |
| Skip testing steps | Low | High | Follow checklist rigorously |
| External dependency added | Low | Critical | Code review, import audit |

---

## 7. Success Criteria

### 7.1 Functional Success
- ✓ All 5 menu options implemented
- ✓ All acceptance criteria met
- ✓ Zero crashes on invalid input
- ✓ All edge cases handled

### 7.2 Technical Success
- ✓ Python standard library only
- ✓ In-memory storage only
- ✓ CLI interface only
- ✓ Single file implementation
- ✓ PEP 8 compliant

### 7.3 Process Success
- ✓ Constitution followed
- ✓ Specification followed
- ✓ Plan followed
- ✓ All workflow steps completed in order

---

## 8. Implementation Checklist

### Pre-Execution Checklist
- [ ] Constitution document exists
- [ ] Specification document approved
- [ ] Planning document complete (this document)
- [ ] Python 3.6+ available
- [ ] Working directory confirmed

### Execution Checklist (To be used during implementation)
- [ ] Step 1: Project setup complete
- [ ] Step 2: Core data functions implemented
- [ ] Step 3: Display functions implemented
- [ ] Step 4: Input functions implemented
- [ ] Step 5: Menu handlers implemented
- [ ] Step 6: Main function implemented
- [ ] Step 7: Happy path testing complete
- [ ] Step 8: Edge case testing complete
- [ ] Step 9: Code quality review complete
- [ ] Step 10: Execution log created

### Post-Execution Checklist (For QA phase)
- [ ] All acceptance criteria validated
- [ ] All test scenarios passed
- [ ] No external dependencies
- [ ] Code quality verified
- [ ] Documentation complete

---

## 9. Timeline Estimation

### Effort Breakdown (Development Time)
- Phase 1 (Setup): 15 minutes
- Phase 2 (Input/Validation): 20 minutes
- Phase 3 (Main Loop): 10 minutes
- Phase 4 (Testing): 30 minutes
- Phase 5 (Documentation): 10 minutes

**Total Estimated Effort**: 85 minutes (1 hour 25 minutes)

**Note**: This is an estimate for actual coding time, not including planning or review.

---

## 10. Code Style Guidelines

### 10.1 Naming Conventions
- Functions: `snake_case` (e.g., `get_task_by_id`)
- Variables: `snake_case` (e.g., `next_task_id`)
- Constants: `UPPER_SNAKE_CASE` (if any)

### 10.2 Function Design
- Single Responsibility Principle
- Maximum 20 lines per function (target)
- Clear input/output types
- Minimal side effects (except handlers)

### 10.3 Error Handling
- Use try-except for input validation
- Never use bare `except:`
- Always provide clear error messages
- No silent failures

### 10.4 Documentation
- Module docstring at top
- Function docstrings for complex logic only
- No redundant comments
- Code should be self-documenting

---

## 11. Dependencies Audit

### 11.1 Allowed Imports
```python
from datetime import datetime  # For timestamps
import sys                      # For sys.exit()
```

### 11.2 Prohibited
- ❌ Any pip packages
- ❌ `import json` (no file I/O needed)
- ❌ `import pickle` (no persistence)
- ❌ `import sqlite3` (no database)
- ❌ Any framework imports

---

## 12. Next Steps

### 12.1 Immediate Next Action
**Proceed to Execution Phase**
- Start with Step 1: Create main file
- Follow steps sequentially
- Document progress in EXECUTION_LOG.md
- Do not skip any steps

### 12.2 After Execution
**Proceed to QA Validation Phase**
- Create QA_VALIDATION.md
- Run all test scenarios
- Verify acceptance criteria
- Document findings

### 12.3 After QA
**Proceed to Checklist Verification Phase**
- Create CHECKLIST.md
- Verify all requirements met
- Final constitutional compliance check
- Project sign-off

---

## 13. Approval & Sign-off

**Planning Status**: ✓ Complete and Ready for Execution

**Constitutional Compliance**: ✓ Verified
- ✓ Planning follows specification
- ✓ No prohibited dependencies planned
- ✓ CLI-only approach confirmed
- ✓ In-memory storage confirmed

**Next Step**: Begin Execution Phase with Step 1

---

**Document Version**: 1.0
**Prepared By**: Claude Code
**Approved By**: [Pending User Approval]
**Ready for Execution**: Yes

---

## Appendix A: Function Call Graph

```
main()
├── display_menu()
├── get_menu_choice()
└── [Based on choice]
    ├── handle_add_task()
    │   ├── get_task_description()
    │   ├── add_task()
    │   │   ├── generate_task_id()
    │   │   └── create_task()
    │   ├── display_success()
    │   └── display_error()
    │
    ├── handle_view_tasks()
    │   └── display_tasks()
    │
    ├── handle_mark_complete()
    │   ├── get_task_id()
    │   ├── mark_task_complete()
    │   │   └── get_task_by_id()
    │   ├── display_success()
    │   └── display_error()
    │
    ├── handle_delete_task()
    │   ├── get_task_id()
    │   ├── delete_task()
    │   │   └── get_task_by_id()
    │   ├── display_success()
    │   └── display_error()
    │
    └── handle_exit()
        └── sys.exit()
```

---

## Appendix B: Sample Code Structure

```python
"""
Todo App Phase 1
A simple CLI-based todo application with in-memory storage.
"""

from datetime import datetime
import sys

# Module-level variables
tasks = []
next_task_id = 1

# Core Data Functions
def generate_task_id():
    # Implementation here
    pass

def create_task(description):
    # Implementation here
    pass

# ... (remaining functions)

def main():
    # Implementation here
    pass

if __name__ == "__main__":
    main()
```

---

**END OF PLANNING DOCUMENT**
