# Todo App: User Guide & Tutorial (Phase 3)

The Todo App is a professional, CLI-based task management system built with pure Python. It features advanced organization, time management, and automation tools—all running in-memory with zero external dependencies.

---

## 🚀 Quick Start

### 1. Installation & Requirements
*   **Prerequisites:** Python 3.6 or higher.
*   **Installation:** None required. No external packages (like `requests` or `pandas`) are used.

### 2. Running the App
Open your terminal in the project root and run:
```bash
python -m src.main
```

### 3. Your First Task
1.  Choose **1** to "Add Task".
2.  Type: `Complete documentation`.
3.  Set priority to `h` (High) and category to `1` (Work).
4.  Choose **2** to "View Tasks" and see your new task with the `[!]` high-priority symbol.

---

## 🛠️ Main Menu Overview

The app features 28 professional menu options organized into logical categories:

| Category | Key Operations |
| :--- | :--- |
| **Basic** | Add, View, Mark Complete, Delete, Edit |
| **Search/Filter** | Keyword search, Priority/Category filters, Overdue/Today/Tomorrow views |
| **Advanced Org** | Due Dates, Subtasks, Dependencies, Recurring patterns, Notes |
| **Automation** | Templates (Save/Create), Bulk operations, Archive system |
| **System** | Statistics dashboard, Undo last action, Exit |

---

## 💡 Key Features & Workflow Tutorials

### 1. Hierarchical Task Management (Subtasks)
You can create a parent-child relationship between tasks to manage complex projects.
*   **How:** Use Menu **16 (Add Subtask)**.
*   **Visuals:** Subtasks are indented with `|--` in the task list.

**Example View:**
```text
1. [ ] [!] Finalize Project Launch
  |-- 2. [ ] [-] Design Landing Page
  |-- 3. [ ] [-] Setup Server
```

### 2. Task Dependencies
Ensure tasks are done in order (e.g., "Review Code" cannot be completed until "Write Code" is done).
*   **How:** Use Menu **17 (Set Dependencies)**.
*   **Safety:** The app includes circular dependency detection to prevent infinite loops.

**Dependency Alert:**
```text
[ERROR] Cannot complete Task 3.
It depends on Task 2 which is still pending.
```

### 3. Time Management
*   **Due Dates:** Set deadlines (YYYY-MM-DD) via Menu **13**.
*   **Overdue Tracking:** The app automatically highlights overdue tasks and shows exactly how many days late they are.

**Overdue Preview:**
```text
1. [ ] [!] Submit Tax Report (Work)
   DUE: 2025-12-31 [OVERDUE by 2 days]
```

*   **Recurring Tasks:** Set tasks to repeat daily, weekly, or monthly via Menu **18**.

### 4. Templates for Speed
If you have a set of tasks you create often (e.g., "Weekly Review"), save them as templates.
*   **Save:** Menu **19** saves a current task configuration.
*   **Create:** Menu **21** creates a new task instantly from a template.

### 5. Task Symbols Reference
*   `[!]` High Priority
*   `[-]` Medium Priority
*   `[~]` Low Priority
*   `[ ]` Pending
*   `[X]` Completed

---

## 📊 Analytics & Reporting
Use Menu **26 (Task Statistics)** to see a full health report of your productivity, including:
*   Completion rates by category and priority.
*   Time-based breakdown (Overdue vs. Upcoming).
*   Structure metrics (Subtask counts, Dependency links).

---

## 🛡️ Safety & Reliability
*   **Undo:** Made a mistake? Use Menu **27** to revert your last action.
*   **Bulk Actions:** Use Menu **22/23** to manage groups of tasks at once (requires confirmation).
*   **Error Handling:** The app validates all inputs, including date formats and task IDs.

---

## 🧪 Test Plan

To ensure the application is functioning correctly, follow this standard test plan:

### 1. Functional Testing
- [ ] **Task Lifecycle:** Create a task, edit it, mark it complete, and delete it.
- [ ] **Hierarchy:** Create a parent task and add 2 subtasks. Verify indentation in view.
- [ ] **Dependencies:** Create Task B depending on Task A. Try to complete Task B first (should fail). Complete Task A, then Task B (should pass).
- [ ] **Validation:** Enter an invalid date (e.g., `2025-13-40`). Application should prompt for a corrected entry.

### 2. Time Management Testing
- [ ] **Today/Tomorrow:** Add a task with today's date and another with tomorrow's. Verify they appear in their respective filter views (Menus 10 & 11).
- [ ] **Overdue:** Add a task with a date from last week. Verify it is flagged as `OVERDUE` in the list view.
- [ ] **Recurring:** Create a daily recurring task. Mark it complete and verify a new instance is created for the next day.

### 3. System & Logic Testing
- [ ] **Undo:** Delete a task, then use Menu 27. The task should reappear.
- [ ] **Search:** Search for a partial word (e.g., "doc" for "documentation"). Results should be found.
- [ ] **Bulk Ops:** Archive all completed tasks using Menu 24. Verify they no longer appear in the main "View Tasks" list.

---

## ❓ Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **"ModuleNotFoundError: No module named 'src'"** | Ensure you are running the app from the project root using `python -m src.main`. |
| **"Invalid date format"** | Dates must follow the `YYYY-MM-DD` format (e.g., 2025-01-01). |
| **"Circular dependency detected"** | You cannot have Task A depend on Task B if Task B already depends on Task A. Review your task relations. |
| **"Task cannot be completed"** | Check if the task has unfinished dependencies. You must complete "depends on" tasks first. |
| **Data is missing after restart** | This app uses **in-memory storage**. All data is cleared when the program exits. |
| **Undo isn't working** | Undo only saves the *immediate* previous state. It cannot revert multiple steps back. |

---

## 💬 FAQ (Frequently Asked Questions)

**Q: Can I use this for multiple users?**
A: Currently, the app is designed for a single session. Since it uses in-memory storage, it does not support multiple persistent user accounts.

**Q: Where is my data saved?**
A: It's not! This project follows a strict "in-memory only" constitution. If you close the app, all tasks are deleted. This makes it perfect for temporary planning or privacy-focused tasking.

**Q: How many subtasks can I have?**
A: The app supports a 2-level hierarchy (Parent -> Subtask). This keeps the interface clean and manageable.

**Q: What happens if I delete a parent task with subtasks?**
A: The subtasks will be "orphaned" (become top-level tasks) or deleted depending on the specific phase implementation. In Phase 3, deleting a parent usually prompts for confirmation or cleans up children.

**Q: Can a task depend on something in the archive?**
A: No. Dependencies must be active tasks. Archiving a task that others depend on may cause those dependent tasks to remain "pending" until the dependency is resolved or removed.

---

## 🧬 Project Structure (For Developers)

The application follows a modular architecture with a clear separation of concerns.

### Core Modules
| Module | Responsibility |
| :--- | :--- |
| **`src/main.py`** | Entry point. Contains the main input loop and menu routing logic. |
| **`src/cli.py`** | View Layer. Handles all user prompts, ASCII formatting, and input validation. |
| **`src/storage.py`** | Data Layer. Manages the global state (in-memory dicts/lists), task IDs, and raw data transformations. |
| **`src/todo.py`** | Domain Logic. Contains business rules like overdue calculation, dependency validation, and sorting algorithms. |
| **`src/exceptions.py`** | Custom error types used for graceful error handling across the layers. |

### Development Workflow
This project uses **Spec-Driven Development (SDD)**:
1.  **Specification:** Define features in `SPECIFICATION_PHASE3.md`.
2.  **Planning:** Draft implementation steps in `PLAN_PHASE3.md`.
3.  **Implementation:** Write clean, modular code following the plan.
4.  **QA:** Verify against `test_all_features.py` and modular tests.

### How to Extend the App
1.  **Add a new menu option:** Add the option string to `main.py` and a corresponding `elif` branch.
2.  **Add a data field:** Update the task creation logic in `storage.py`.
3.  **Add business logic:** Add the processing function to `todo.py`.
4.  **Add UI handler:** Create a function in `cli.py` to prompt the user and show results.

---

## 🚀 Running the Demo

To see all features in action without manual input, simply run:
```bash
python demo_live.py
```

---

## 📢 Developer Feedback

We value your feedback! If you are a developer using or extending this project, please consider:

1.  **Reporting Bugs:** Found a logic error or a CLI quirk? Open an issue with a detailed description.
2.  **Suggesting Features:** Have an idea for Phase 4? We'd love to hear how to make this tool even better.
3.  **Code Review:** Notice a way to optimize our sorting algorithms or storage layer? Your suggestions are welcome.
4.  **Documentation Improvements:** If any part of this guide was unclear, let us know so we can fix it.

*Developed with ❤️ by Farhana Yousuf for the GIAIC Community.*
