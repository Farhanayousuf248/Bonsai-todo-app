# Skill: review-demo-flow

## Purpose
Evaluate the application's CLI flow to ensure it is professional, intuitive, and "demo-ready" for judges. This skill identifies friction points in the user journey.

## Ownership
**Agent:** judge-review-evaluator

## When to Use
- After a new CLI feature is implemented.
- Before a project milestone or demo submission.
- When UX feedback is requested on the interaction model.

## Inputs
- Access to the application source code (entry point).
- A description of the feature or flow to be reviewed.

## Step-by-Step Process
1. **Entry Point Analysis:** Identify the main entry point and initial menu state.
2. **Path Mapping:** Simulate the user path for a specific task (e.g., "Add a task with a long title").
3. **Visibility Audit:** Check if the application provides clear feedback for every action (success messages, error visibility).
4. **Consistency Check:** Verify that menu numbering, casing, and terminology are consistent across all screens.
5. **Efficiency Scoring:** Evaluate if common tasks require excessive typing or menu nesting.

## Output
A "Demo Readiness Report" containing:
- **UX Score (1-10):** Quantitative assessment of the flow.
- **Friction Points:** Specific areas where a judge might get confused.
- **Polish Opportunities:** Recommendations for better formatting (e.g., using tables, colors, or better spacing).

## Failure Handling
- If the application fails to run: Report "CRITICAL: Flow blocked by runtime error."
- If the flow is cyclical/infinite: Report "UX BUG: Circular menu logic detected."
