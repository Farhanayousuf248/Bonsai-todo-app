"""
Custom exceptions for Todo App.
"""


class TodoAppError(Exception):
    """Base exception for Todo App."""
    pass


class TaskNotFoundError(TodoAppError):
    """Raised when a task ID is not found."""
    pass


class InvalidInputError(TodoAppError):
    """Raised when user input is invalid."""
    pass


class EmptyDescriptionError(TodoAppError):
    """Raised when task description is empty."""
    pass
