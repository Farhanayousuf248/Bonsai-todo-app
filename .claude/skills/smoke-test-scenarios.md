# Skill: smoke-test-scenarios

## Purpose
Verify that the core business logic of the Todo App functions correctly and handles edge cases gracefully without crashing.

## Ownership
**Agent:** judge-review-evaluator

## When to Use
- After implementing a core domain feature (Add, Edit, Delete, List).
- To validate that a bug fix doesn't introduce regressions.
- Proactively to find "hidden" logic bugs.

## Inputs
- Specific feature to test (e.g., "Task Deletion").
- Current implementation details.

## Step-by-Step Process
1. **Scenario Generation:** Create 3 test cases: 1 Happy Path, 1 Boundary Case, 1 Malicious/Invalid Input Case.
2. **Execution Simulation:** Mentally or via script execution, trace the path of these inputs through the logic.
3. **State Verification:** Confirm the in-memory state (Task List) is correct after each operation.
4. **Error Handling Check:** Ensure that invalid inputs result in a user-friendly message rather than a Python traceback.

## Output
A "Smoke Test Results" summary:
- **Test Case:** [Name] | **Input:** [Values] | **Result:** [Pass/Fail]
- **Bugs Found:** Description of any logic flaws or crashes.
- **Improved Validation:** Suggestions for missing input checks.

## Failure Handling
- If logic is too complex for manual tracing: Recommend creating an automated unit test.
- If storage is inconsistent: Flag as "DATA INTEGRITY ERROR".
