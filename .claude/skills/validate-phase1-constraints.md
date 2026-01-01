# Skill: validate-phase1-constraints

## Purpose
Enforce the strict technical boundaries of the Phase 1 Todo App: Python CLI, in-memory storage, no external databases, and no web components.

## Ownership
**Agent:** judge-review-evaluator

## When to Use
- During the review of any implementation plan (`/sp.plan`).
- Before finalizing a code change.
- To audit the current state of the repository for compliance.

## Inputs
- Current repository files and dependencies (`requirements.txt`, imports).

## Step-by-Step Process
1. **Dependency Audit:** Check `requirements.txt` or `imports` for forbidden libraries (SQLAlchemy, Django, Flask, Requests for web, etc.).
2. **Storage Verification:** Scan code for file I/O or database connection strings that suggest persistent storage (sqlite, json files, etc.).
3. **Architecture Scan:** Ensure all logic is accessible via the CLI and no unexpected web servers or listeners are present.
4. **Environment Check:** Confirm the project relies solely on standard Python 3.x features or approved minimal libraries.

## Output
A "Compliance Audit" report:
- **Status:** [PASSED / FAILED / WARNING]
- **Violations:** List any code or dependencies that break Phase 1 rules.
- **Remediation:** Specific steps to bring the code back into compliance.

## Failure Handling
- If architecture is ambiguous: Flag as "WARNING: Potential persistence logic detected; manual review required."
