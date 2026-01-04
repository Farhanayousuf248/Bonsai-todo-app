# Todo App Phase 2 - Execution Plan

**Project**: Todo App Phase 2
**Maintainer**: Farhana Yousuf (GIAIC)
**Document Status**: Planning
**Last Updated**: 2025-12-31
**Based On**: SPECIFICATION_PHASE2.md v1.0

---

## 1. Planning Overview

### 1.1 Purpose
This document provides a step-by-step execution plan for implementing Todo App Phase 2, building upon the completed Phase 1 foundation while adding 8 new major features.

### 1.2 Workflow Position
✓ Constitution → ✓ Specification → **→ Planning** → Execution → QA Validation → Checklist Verification

### 1.3 Phase 1 Foundation
Phase 2 builds upon:
- ✓ Phase 1 Complete (100/100 quality score)
- ✓ 19 existing functions
- ✓ 230 lines of code
- ✓ 5 core features working
- ✓ In-memory state management

---

## 2. Implementation Strategy

### 2.1 Development Approach
- **Incremental Enhancement**: Add features without breaking Phase 1
- **Backward Compatibility**: Ensure all Phase 1 functions continue working
- **Phased Implementation**: Implement in 3 sub-phases (2.1, 2.2, 2.3)
- **Test After Each Feature**: Validate each addition before proceeding
- **Single File Structure**: Continue using todo_app.py

### 2.2 File Structure
```
bonsai/
├── Phase 1 Files (Complete):
│   ├── SPECIFICATION.md
│   ├── PLAN.md
│   ├── todo_app.py (v1.0)
│   ├── EXECUTION_LOG.md
│   ├── QA_VALIDATION.md
│   └── CHECKLIST.md
│
├── Phase 2 Files (In Progress):
│   ├── SPECIFICATION_PHASE2.md (✓ Complete)
│   ├── PLAN_PHASE2.md (Current document)
│   ├── todo_app_v2.py (To be created)
│   ├── EXECUTION_LOG_PHASE2.md (To be created)
│   ├── QA_VALIDATION_PHASE2.md (To be created)
│   └── CHECKLIST_PHASE2.md (To be created)
```

### 2.3 Migration Strategy
- **Preserve Phase 1**: Keep todo_app.py as v1.0
- **Create Phase 2**: Build todo_app_v2.py with enhancements
- **Data Migration**: Auto-assign default priority/category to existing tasks

---

## 3. Code Architecture (Phase 2)

### 3.1 Enhanced Module-Level Variables
```python
tasks = []                    # List to store task dictionaries (unchanged)
next_task_id = 1              # Global counter for task IDs (unchanged)

# NEW: Priority and category mappings
PRIORITY_SYMBOLS = {
    "high": "[!]",
    "medium": "[-]",
    "low": "[~]"
}

PRIORITY_SORT = {
    "high": 1,
    "medium": 2,
    "low": 3
}

CATEGORIES = {
    1: "work",
    2: "personal",
    3: "shopping",
    4: "other"
}
```

### 3.2 Function Structure (Phase 2)

**Total Functions Planned**: 38 (19 from Phase 1 + 19 new)

#### Phase 1 Functions (19 - Preserved)
All existing functions remain unchanged and operational.

#### New Core Data Functions (6)
1. `edit_task(task_id, description=None, priority=None, category=None)` → bool
   - Updates task fields, keeps existing if None provided

2. `set_task_priority(task_id, priority)` → bool
   - Sets priority for existing task

3. `set_task_category(task_id, category)` → bool
   - Sets category for existing task

4. `search_tasks(keyword)` → list
   - Returns list of tasks matching keyword (case-insensitive)

5. `filter_tasks_by_priority(priority)` → list
   - Returns tasks filtered by priority level

6. `filter_tasks_by_category(category)` → list
   - Returns tasks filtered by category

#### New Utility Functions (4)
7. `normalize_priority(priority_input)` → str
   - Converts h/m/l or full names to standard format
   - Returns "medium" if invalid

8. `get_priority_symbol(priority)` → str
   - Returns symbol for display ([!], [-], [~])

9. `get_category_name(category_id)` → str
   - Converts category ID to name

10. `sort_tasks(sort_by)` → list
    - Returns sorted copy of tasks
    - sort_by: "id", "priority", "date_new", "date_old"

#### New Display Functions (4)
11. `display_menu_v2()` → None
    - Displays enhanced menu with 11 options

12. `display_task_enhanced(task)` → None
    - Displays single task with priority and category

13. `display_tasks_v2(tasks_list=None, title="YOUR TASKS")` → None
    - Enhanced display with priority symbols and categories
    - Accepts optional filtered list

14. `display_statistics()` → None
    - Shows comprehensive task statistics

#### New Input Functions (5)
15. `get_menu_choice_v2()` → int
    - Gets and validates menu choice (1-11)

16. `get_priority_input(default="medium")` → str
    - Gets priority with default value
    - Accepts h/m/l or full names

17. `get_category_input(default=4)` → str
    - Gets category with default value
    - Returns category name

18. `get_search_keyword()` → str
    - Gets and validates search keyword

19. `get_sort_choice()` → str
    - Gets sort preference from user

#### New Menu Handler Functions (6)
20. `handle_add_task_v2()` → None
    - Enhanced add with priority and category

21. `handle_view_tasks_v2()` → None
    - Calls display_tasks_v2()

22. `handle_edit_task()` → None
    - Handles task editing workflow

23. `handle_search_tasks()` → None
    - Handles search functionality

24. `handle_filter_priority()` → None
    - Handles priority filtering

25. `handle_filter_category()` → None
    - Handles category filtering

26. `handle_sort_tasks()` → None
    - Handles task sorting

27. `handle_statistics()` → None
    - Displays task statistics

#### Enhanced Main Function (1)
28. `main_v2()` → None
    - Enhanced main loop with 11 menu options

---

## 4. Step-by-Step Execution Plan

### Phase 2.1: Core Features (Steps 1-5)

#### Step 1: Setup and Data Structure Enhancement
**Task**: Create todo_app_v2.py and enhance data structure
**Actions**:
- Copy todo_app.py to todo_app_v2.py
- Add new module constants (PRIORITY_SYMBOLS, CATEGORIES, etc.)
- Update create_task() to include priority and category
- Add default values for existing tasks

**Validation**: File exists, constants defined, no syntax errors

---

#### Step 2: Implement Priority Functions
**Task**: Add priority-related functions
**Actions**:
- Implement `normalize_priority(priority_input)`
- Implement `get_priority_symbol(priority)`
- Implement `set_task_priority(task_id, priority)`
- Update `create_task()` to accept priority parameter

**Validation**: Priority functions tested with valid/invalid inputs

---

#### Step 3: Implement Category Functions
**Task**: Add category-related functions
**Actions**:
- Implement `get_category_name(category_id)`
- Implement `set_task_category(task_id, category)`
- Update `create_task()` to accept category parameter

**Validation**: Category functions tested

---

#### Step 4: Enhance Display Functions
**Task**: Update display to show priority and category
**Actions**:
- Implement `display_task_enhanced(task)`
- Implement `display_tasks_v2()`
- Implement `display_menu_v2()`

**Validation**: Visual inspection of enhanced output

---

#### Step 5: Implement Enhanced Add Task
**Task**: Update add task to include priority/category
**Actions**:
- Implement `get_priority_input()`
- Implement `get_category_input()`
- Implement `handle_add_task_v2()`

**Validation**: Test adding tasks with various priority/category combinations

---

### Phase 2.2: Edit and Search Features (Steps 6-9)

#### Step 6: Implement Edit Task
**Task**: Add task editing functionality
**Actions**:
- Implement `edit_task(task_id, description, priority, category)`
- Implement `handle_edit_task()`
- Add menu option 5 (Edit Task)

**Validation**: Test editing description, priority, category, and combinations

---

#### Step 7: Implement Search Functionality
**Task**: Add search capability
**Actions**:
- Implement `search_tasks(keyword)`
- Implement `get_search_keyword()`
- Implement `handle_search_tasks()`
- Add menu option 6 (Search Tasks)

**Validation**: Test with various keywords, case sensitivity, partial matches

---

#### Step 8: Implement Priority Filter
**Task**: Add filter by priority
**Actions**:
- Implement `filter_tasks_by_priority(priority)`
- Implement `handle_filter_priority()`
- Add menu option 7 (Filter by Priority)

**Validation**: Test filtering high/medium/low, no results case

---

#### Step 9: Implement Category Filter
**Task**: Add filter by category
**Actions**:
- Implement `filter_tasks_by_category(category)`
- Implement `handle_filter_category()`
- Add menu option 8 (Filter by Category)

**Validation**: Test filtering each category, no results case

---

### Phase 2.3: Advanced Features (Steps 10-12)

#### Step 10: Implement Sort Functionality
**Task**: Add task sorting
**Actions**:
- Implement `sort_tasks(sort_by)`
- Implement `get_sort_choice()`
- Implement `handle_sort_tasks()`
- Add menu option 9 (Sort Tasks)

**Validation**: Test sort by ID, priority, date (both directions)

---

#### Step 11: Implement Task Statistics
**Task**: Add statistics display
**Actions**:
- Implement `calculate_statistics()` helper function
- Implement `display_statistics()`
- Implement `handle_statistics()`
- Add menu option 10 (Task Statistics)

**Validation**: Verify calculations with known test data

---

#### Step 12: Integrate Main Loop
**Task**: Update main function with all features
**Actions**:
- Implement `main_v2()` with 11 menu options
- Update `get_menu_choice_v2()` for 1-11 range
- Wire all handlers to menu options
- Update exit to option 11

**Validation**: Full application runs with all features

---

### Phase 2.4: Testing & Refinement (Steps 13-15)

#### Step 13: Comprehensive Feature Testing
**Task**: Test all Phase 2 features
**Test Scenarios**:
1. Add tasks with different priorities and categories
2. Edit multiple fields simultaneously
3. Search with various keywords
4. Filter by each priority level
5. Filter by each category
6. Sort by all options
7. View statistics with diverse data
8. Test Phase 1 features still work

**Validation**: All features work as specified

---

#### Step 14: Edge Case Testing
**Task**: Test error handling and edge cases
**Test Cases**:
1. Edit non-existent task ID
2. Search with no results
3. Filter with no matching tasks
4. Invalid priority input
5. Invalid category input
6. Empty inputs where required
7. Case sensitivity handling
8. Backward compatibility with Phase 1 data

**Validation**: All edge cases handled gracefully

---

#### Step 15: Code Quality Review
**Task**: Review and refine code quality
**Actions**:
- Check for code duplication
- Verify function sizes (< 20 lines target)
- Verify naming clarity
- Check PEP 8 compliance
- Verify no external dependencies
- Ensure backward compatibility

**Validation**: Code meets quality standards

---

### Phase 2.5: Documentation (Step 16)

#### Step 16: Create Execution Log
**Task**: Document Phase 2 implementation
**Actions**:
- Create EXECUTION_LOG_PHASE2.md
- Document each implementation step
- Note deviations from plan
- List all new functions
- Document test results
- Record migration process

**Validation**: Log complete and accurate

---

## 5. Quality Assurance Strategy

### 5.1 Testing Approach
- **Feature Testing**: Each feature tested individually
- **Integration Testing**: All features work together
- **Regression Testing**: Phase 1 features still work
- **Edge Case Testing**: All error paths tested
- **Backward Compatibility Testing**: Old data works with new features

### 5.2 Test Coverage Goals
- 100% feature coverage
- 100% edge case coverage
- 100% Phase 1 regression coverage
- Zero defects target

---

## 6. Risk Management

### 6.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking Phase 1 features | Low | Critical | Preserve original functions, thorough regression testing |
| Data structure migration issues | Low | High | Default values strategy, validation |
| Menu complexity | Medium | Medium | Clear numbering, consistent patterns |
| Performance with search/filter | Low | Medium | In-memory operations remain fast |

### 6.2 Implementation Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Feature creep beyond Phase 2 | Medium | Medium | Strict adherence to specification |
| Code complexity increase | Medium | Medium | Keep functions small, clear naming |
| Testing insufficient | Low | High | Comprehensive test plan, checklist |

---

## 7. Success Criteria

### 7.1 Functional Success
- ✓ All 8 new features implemented
- ✓ All 60+ acceptance criteria met
- ✓ All Phase 1 features still working
- ✓ Zero crashes on invalid input
- ✓ All edge cases handled

### 7.2 Technical Success
- ✓ Python standard library only
- ✓ In-memory storage maintained
- ✓ CLI interface only
- ✓ Single file implementation
- ✓ PEP 8 compliant
- ✓ Backward compatible

### 7.3 Process Success
- ✓ Constitution followed
- ✓ Specification followed
- ✓ Plan followed
- ✓ All workflow steps completed in order

---

## 8. Implementation Checklist

### Pre-Execution Checklist
- [✓] Phase 1 complete and verified
- [✓] Phase 2 specification approved
- [✓] Phase 2 planning document complete (this document)
- [ ] Python 3.6+ available
- [ ] Phase 1 backup created

### Phase 2.1 Checklist (Core Features)
- [ ] Step 1: Data structure enhancement
- [ ] Step 2: Priority functions
- [ ] Step 3: Category functions
- [ ] Step 4: Enhanced display
- [ ] Step 5: Enhanced add task

### Phase 2.2 Checklist (Edit & Search)
- [ ] Step 6: Edit task
- [ ] Step 7: Search functionality
- [ ] Step 8: Priority filter
- [ ] Step 9: Category filter

### Phase 2.3 Checklist (Advanced)
- [ ] Step 10: Sort functionality
- [ ] Step 11: Task statistics
- [ ] Step 12: Main loop integration

### Phase 2.4 Checklist (Testing)
- [ ] Step 13: Feature testing
- [ ] Step 14: Edge case testing
- [ ] Step 15: Code quality review

### Phase 2.5 Checklist (Documentation)
- [ ] Step 16: Execution log

---

## 9. Timeline Estimation

### Effort Breakdown
- Phase 2.1 (Core Features): 45 minutes
- Phase 2.2 (Edit & Search): 40 minutes
- Phase 2.3 (Advanced): 35 minutes
- Phase 2.4 (Testing): 60 minutes
- Phase 2.5 (Documentation): 15 minutes

**Total Estimated Effort**: 195 minutes (~3 hours 15 minutes)

---

## 10. Code Style Guidelines (Phase 2)

### 10.1 Naming Conventions
- Functions: `snake_case` with `_v2` suffix for enhanced versions
- Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE` for new constants

### 10.2 Function Design
- Single Responsibility maintained
- Maximum 20 lines per function
- Clear input/output types
- Backward compatible signatures

### 10.3 Documentation
- Function docstrings for all new functions
- Module docstring updated for Phase 2
- Comments only where logic is complex

---

## 11. Backward Compatibility Plan

### 11.1 Data Migration
```python
# Auto-migrate Phase 1 tasks
for task in tasks:
    if "priority" not in task:
        task["priority"] = "medium"
    if "category" not in task:
        task["category"] = "other"
```

### 11.2 Function Preservation
- All Phase 1 functions remain unchanged
- New functions use different names (_v2 suffix)
- Phase 1 menu options (1-5) remain identical

### 11.3 Testing Strategy
- Run Phase 1 test suite against Phase 2 code
- Verify all Phase 1 features work identically
- Check Phase 1 data format compatibility

---

## 12. New Function Summary

### 12.1 Function Categories

| Category | Count | Functions |
|----------|-------|-----------|
| Core Data Functions | 6 | edit_task, set_priority, set_category, search, filter_priority, filter_category |
| Utility Functions | 4 | normalize_priority, get_priority_symbol, get_category_name, sort_tasks |
| Display Functions | 4 | display_menu_v2, display_task_enhanced, display_tasks_v2, display_statistics |
| Input Functions | 5 | get_menu_choice_v2, get_priority_input, get_category_input, get_search_keyword, get_sort_choice |
| Menu Handlers | 8 | handle_add_v2, handle_view_v2, handle_edit, handle_search, handle_filter_priority, handle_filter_category, handle_sort, handle_statistics |
| Main Function | 1 | main_v2 |

**Total New Functions**: 28
**Total Functions (Phase 1 + Phase 2)**: 47

---

## 13. Dependencies Audit (Phase 2)

### 13.1 Allowed Imports (Same as Phase 1)
```python
from datetime import datetime  # Existing
import sys                      # Existing
# Optional: import re for enhanced search (if needed)
```

### 13.2 Prohibited
- ❌ Any pip packages
- ❌ Any frameworks
- ❌ Any database libraries
- ❌ Any file I/O for persistence

---

## 14. Next Steps

### 14.1 Immediate Next Action
**Proceed to Execution Phase (Phase 2.1)**
- Start with Step 1: Data structure enhancement
- Follow steps sequentially through all sub-phases
- Document progress in EXECUTION_LOG_PHASE2.md
- Do not skip any steps

### 14.2 After Execution
**Proceed to QA Validation Phase**
- Create QA_VALIDATION_PHASE2.md
- Run all test scenarios
- Verify all acceptance criteria
- Verify backward compatibility
- Document findings

### 14.3 After QA
**Proceed to Checklist Verification Phase**
- Create CHECKLIST_PHASE2.md
- Verify all requirements met
- Final constitutional compliance check
- Project sign-off

---

## 15. Approval & Sign-off

**Planning Status**: ✓ Complete and Ready for Execution

**Constitutional Compliance**: ✓ Verified
- ✓ Planning follows specification
- ✓ No prohibited dependencies planned
- ✓ CLI-only approach maintained
- ✓ In-memory storage maintained
- ✓ Backward compatibility ensured

**Phase 1 Compatibility**: ✓ Preserved
- ✓ No breaking changes planned
- ✓ All Phase 1 functions preserved
- ✓ Data migration strategy defined

**Next Step**: Begin Execution Phase 2.1 with Step 1

---

**Document Version**: 1.0
**Prepared By**: Claude Code
**Based On**: Phase 1 Complete (100/100) + SPECIFICATION_PHASE2.md
**Approved By**: [Pending User Approval]
**Ready for Execution**: Yes

---

## Appendix A: Function Call Graph (Phase 2)

```
main_v2()
├── display_menu_v2()
├── get_menu_choice_v2()
└── [Based on choice 1-11]
    ├── 1. handle_add_task_v2()
    │   ├── get_task_description()
    │   ├── get_priority_input() → normalize_priority()
    │   ├── get_category_input() → get_category_name()
    │   ├── create_task() [enhanced]
    │   └── display_success()
    │
    ├── 2. handle_view_tasks_v2()
    │   └── display_tasks_v2()
    │       ├── display_task_enhanced() [for each task]
    │       │   └── get_priority_symbol()
    │       └── summary stats
    │
    ├── 3. handle_mark_complete() [Phase 1, unchanged]
    │
    ├── 4. handle_delete_task() [Phase 1, unchanged]
    │
    ├── 5. handle_edit_task()
    │   ├── get_task_id()
    │   ├── get_task_by_id()
    │   ├── get_priority_input() [optional]
    │   ├── get_category_input() [optional]
    │   ├── edit_task()
    │   └── display_success()
    │
    ├── 6. handle_search_tasks()
    │   ├── get_search_keyword()
    │   ├── search_tasks()
    │   └── display_tasks_v2() [filtered]
    │
    ├── 7. handle_filter_priority()
    │   ├── get_priority_input()
    │   ├── filter_tasks_by_priority()
    │   └── display_tasks_v2() [filtered]
    │
    ├── 8. handle_filter_category()
    │   ├── get_category_input()
    │   ├── filter_tasks_by_category()
    │   └── display_tasks_v2() [filtered]
    │
    ├── 9. handle_sort_tasks()
    │   ├── get_sort_choice()
    │   ├── sort_tasks()
    │   └── display_tasks_v2() [sorted]
    │
    ├── 10. handle_statistics()
    │   └── display_statistics()
    │       └── [Calculate all metrics]
    │
    └── 11. handle_exit() [Phase 1, unchanged]
```

---

## Appendix B: Sample Enhanced Task Display

```python
===== YOUR TASKS =====
1. [ ] [!] Complete project report (Work, Created: 2025-12-31 10:30:00)
2. [X] [-] Buy groceries (Shopping, Created: 2025-12-31 09:15:00)
3. [ ] [~] Read book (Personal, Created: 2025-12-31 08:00:00)

Total: 3 tasks (2 pending, 1 completed)
Priority: 1 high, 1 medium, 1 low
Categories: 1 work, 1 personal, 1 shopping

Legend:
  Status: [ ] = Pending, [X] = Completed
  Priority: [!] = High, [-] = Medium, [~] = Low
```

---

**END OF PHASE 2 PLANNING DOCUMENT**
