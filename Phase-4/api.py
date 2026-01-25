"""
FastAPI Backend for Todo App Phase 4
REST API for live task data management.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys
import os

# Add Phase-3 src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Phase-3'))

from src import storage

# Initialize FastAPI app
app = FastAPI(
    title="Todo App API",
    description="REST API for Todo App Phase 4 - Live task data management",
    version="4.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Pydantic Models
# ============================================================================

class TaskCreate(BaseModel):
    description: str
    priority: str = "medium"
    category: str = "other"


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: str
    priority: str
    category: str
    due_date: Optional[str] = None
    notes: str = ""
    parent_id: Optional[int] = None
    depends_on: List[int] = []
    recurring: Optional[dict] = None
    archived: bool = False
    completed_at: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Serve the Phase 4 web interface."""
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Kubernetes probes."""
    return {
        "status": "healthy",
        "version": "4.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/v1/tasks", response_model=List[TaskResponse])
async def get_all_tasks():
    """Get all tasks."""
    tasks = storage.get_all_tasks()
    return tasks


@app.get("/api/v1/tasks/active", response_model=List[TaskResponse])
async def get_active_tasks():
    """Get only non-archived tasks."""
    tasks = storage.get_all_tasks()
    return [t for t in tasks if not t.get("archived", False)]


@app.get("/api/v1/tasks/pending", response_model=List[TaskResponse])
async def get_pending_tasks():
    """Get only pending (non-completed) tasks."""
    tasks = storage.get_all_tasks()
    return [t for t in tasks if not t["completed"] and not t.get("archived", False)]


@app.get("/api/v1/tasks/completed", response_model=List[TaskResponse])
async def get_completed_tasks():
    """Get only completed tasks."""
    tasks = storage.get_all_tasks()
    return [t for t in tasks if t["completed"] and not t.get("archived", False)]


@app.get("/api/v1/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """Get a specific task by ID."""
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/v1/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task."""
    if not task.description.strip():
        raise HTTPException(status_code=400, detail="Task description cannot be empty")

    success = storage.add_task(task.description, task.priority, task.category)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to create task")

    # Return the newly created task
    all_tasks = storage.get_all_tasks()
    return all_tasks[-1]


@app.put("/api/v1/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task."""
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    success = storage.edit_task(
        task_id,
        description=task_update.description,
        priority=task_update.priority,
        category=task_update.category
    )

    if not success:
        raise HTTPException(status_code=400, detail="Failed to update task")

    return storage.get_task_by_id(task_id)


@app.post("/api/v1/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int):
    """Mark a task as completed."""
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["completed"]:
        raise HTTPException(status_code=400, detail="Task already completed")

    success = storage.mark_task_complete(task_id)
    if not success:
        # Check if there are incomplete dependencies
        all_complete, incomplete = storage.check_dependencies_complete(task_id)
        if not all_complete:
            dep_names = [t["description"] for t in incomplete[:3]]
            raise HTTPException(
                status_code=400,
                detail=f"Cannot complete task. Complete these tasks first: {', '.join(dep_names)}"
            )
        raise HTTPException(status_code=400, detail="Failed to complete task")

    return storage.get_task_by_id(task_id)


@app.post("/api/v1/tasks/{task_id}/uncomplete", response_model=TaskResponse)
async def uncomplete_task(task_id: int):
    """Mark a task as incomplete (undo complete)."""
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    success = storage.undo_last_action()
    if not success[0]:
        # Fallback if undo isn't possible (e.g. not the last action)
        task["completed"] = False
        task["completed_at"] = None
        storage.save_data()

    return storage.get_task_by_id(task_id)


@app.delete("/api/v1/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Delete a task."""
    success = storage.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


# ============================================================================
# Filter & Search Endpoints
# ============================================================================

@app.get("/api/v1/tasks/search/{keyword}", response_model=List[TaskResponse])
async def search_tasks(keyword: str):
    """Search tasks by keyword."""
    return storage.search_tasks(keyword)


@app.get("/api/v1/tasks/priority/{priority}", response_model=List[TaskResponse])
async def filter_by_priority(priority: str):
    """Filter tasks by priority level."""
    if priority not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="Invalid priority. Use: high, medium, or low")
    return storage.filter_tasks_by_priority(priority)


@app.get("/api/v1/tasks/category/{category}", response_model=List[TaskResponse])
async def filter_by_category(category: str):
    """Filter tasks by category."""
    return storage.filter_tasks_by_category(category)


@app.get("/api/v1/tasks/overdue", response_model=List[TaskResponse])
async def get_overdue_tasks():
    """Get overdue tasks."""
    return storage.get_overdue_tasks()


@app.get("/api/v1/tasks/due/today", response_model=List[TaskResponse])
async def get_today_tasks():
    """Get tasks due today."""
    return storage.get_tasks_by_due_date("today")


@app.get("/api/v1/tasks/due/tomorrow", response_model=List[TaskResponse])
async def get_tomorrow_tasks():
    """Get tasks due tomorrow."""
    return storage.get_tasks_by_due_date("tomorrow")


# ============================================================================
# Statistics Endpoints
# ============================================================================

@app.get("/api/v1/stats")
async def get_statistics():
    """Get task statistics."""
    all_tasks = storage.get_all_tasks()
    active_tasks = [t for t in all_tasks if not t.get("archived", False)]
    completed_tasks = [t for t in active_tasks if t["completed"]]
    pending_tasks = [t for t in active_tasks if not t["completed"]]

    # Priority breakdown for pending
    priority_breakdown = {}
    for p in ["high", "medium", "low"]:
        priority_breakdown[p] = len([t for t in pending_tasks if t["priority"] == p])

    # Category breakdown
    category_breakdown = {}
    for task in active_tasks:
        cat = task["category"]
        category_breakdown[cat] = category_breakdown.get(cat, 0) + 1

    return {
        "total": len(all_tasks),
        "active": len(active_tasks),
        "pending": len(pending_tasks),
        "completed": len(completed_tasks),
        "archived": len([t for t in all_tasks if t.get("archived", False)]),
        "completion_rate": round(len(completed_tasks) / len(active_tasks) * 100, 1) if active_tasks else 0,
        "by_priority": priority_breakdown,
        "by_category": category_breakdown
    }


# ============================================================================
# Undo Endpoint
# ============================================================================

@app.post("/api/v1/undo")
async def undo_last_action():
    """Undo the last action."""
    success, message = storage.undo_last_action()
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}


@app.get("/api/v1/undo/status")
async def get_undo_status():
    """Get undo status (whether there's an action to undo)."""
    last_action = storage.get_last_action()
    return {"has_action": last_action is not None, "action": last_action}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
