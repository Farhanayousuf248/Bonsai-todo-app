"""
AI Smart-Input Analyzer for Todo App Phase 5
Automatically detects priority and category from task descriptions.
"""

import re
from typing import Dict, Tuple


# Priority detection keywords and patterns
PRIORITY_KEYWORDS = {
    "high": [
        "urgent", "urgently", "asap", "critical", "important", "emergency", "immediately",
        "priority", "crucial", "vital", "must", "deadline", "today", "now",
        "!!!", "urgent:", "asap:", "critical:", "high priority"
    ],
    "low": [
        "maybe", "sometime", "eventually", "when possible", "if time",
        "low priority", "not urgent", "optional", "consider", "think about",
        "someday", "later", "future"
    ]
}

# Category detection keywords
CATEGORY_KEYWORDS = {
    "work": [
        "meeting", "project", "deadline", "presentation", "report", "email",
        "client", "boss", "colleague", "office", "work", "business", "call",
        "proposal", "review", "document", "schedule", "team", "conference",
        "quarterly", "annual", "budget", "invoice", "contract", "deliver"
    ],
    "personal": [
        "doctor", "appointment", "health", "exercise", "gym", "workout",
        "family", "friend", "birthday", "anniversary", "vacation", "hobby",
        "read", "learn", "study", "course", "book", "personal", "self",
        "meditation", "therapy", "dentist", "haircut", "wellness"
    ],
    "shopping": [
        "buy", "purchase", "shop", "store", "order", "groceries", "grocery",
        "amazon", "mall", "supermarket", "market", "get", "pick up",
        "shopping", "items", "supplies", "food", "clothes", "gift"
    ]
}

# Contextual patterns for priority (regex)
PRIORITY_PATTERNS = {
    "high": [
        r"\b(due (today|tomorrow|this week))\b",
        r"\b(before \w+day)\b",
        r"[!]{2,}",  # Multiple exclamation marks
        r"\b(finish|complete|submit) (by|before)\b"
    ],
    "low": [
        r"\b(when (i|you) (can|have time))\b",
        r"\b(no (rush|hurry))\b"
    ]
}


def analyze_task_text(description: str) -> Dict[str, str]:
    """
    Analyze task description and extract priority and category.

    Args:
        description: Task description text

    Returns:
        Dictionary with 'priority' and 'category' keys
    """
    if not description or not description.strip():
        return {"priority": "medium", "category": "other"}

    text_lower = description.lower()

    # Explicit check for "urgently" keyword - always triggers HIGH priority
    if "urgently" in text_lower:
        priority = "high"
        category = detect_category(text_lower)
    else:
        priority = detect_priority(text_lower)
        category = detect_category(text_lower)

    return {
        "priority": priority,
        "category": category
    }


def detect_priority(text: str) -> str:
    """
    Detect priority level from task text.

    Args:
        text: Lowercase task text

    Returns:
        Priority level: "high", "medium", or "low"
    """
    # Score for each priority level
    scores = {"high": 0, "low": 0}

    # Check keywords
    for priority, keywords in PRIORITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                scores[priority] += 2

    # Check regex patterns
    for priority, patterns in PRIORITY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                scores[priority] += 3

    # Determine priority based on scores
    if scores["high"] > scores["low"]:
        return "high"
    elif scores["low"] > scores["high"]:
        return "low"
    else:
        return "medium"


def detect_category(text: str) -> str:
    """
    Detect category from task text.

    Args:
        text: Lowercase task text

    Returns:
        Category: "work", "personal", "shopping", or "other"
    """
    # Score for each category
    scores = {"work": 0, "personal": 0, "shopping": 0}

    # Check keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                scores[category] += 1

    # Find category with highest score
    max_score = max(scores.values())

    if max_score == 0:
        return "other"

    # Return category with highest score
    for category, score in scores.items():
        if score == max_score:
            return category

    return "other"


def get_analysis_confidence(description: str, detected: Dict[str, str]) -> Dict[str, float]:
    """
    Calculate confidence scores for detected priority and category.

    Args:
        description: Original task text
        detected: Detected priority and category

    Returns:
        Dictionary with confidence scores (0.0 to 1.0)
    """
    text_lower = description.lower()

    # Priority confidence
    priority_confidence = 0.5  # Default medium confidence

    if detected["priority"] != "medium":
        # Count matching keywords/patterns
        matches = 0
        if detected["priority"] in PRIORITY_KEYWORDS:
            for keyword in PRIORITY_KEYWORDS[detected["priority"]]:
                if keyword in text_lower:
                    matches += 1

        if detected["priority"] in PRIORITY_PATTERNS:
            for pattern in PRIORITY_PATTERNS[detected["priority"]]:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    matches += 2

        priority_confidence = min(0.9, 0.5 + (matches * 0.1))

    # Category confidence
    category_confidence = 0.3  # Default low confidence for "other"

    if detected["category"] != "other":
        matches = 0
        for keyword in CATEGORY_KEYWORDS.get(detected["category"], []):
            if keyword in text_lower:
                matches += 1

        category_confidence = min(0.95, 0.4 + (matches * 0.15))

    return {
        "priority": round(priority_confidence, 2),
        "category": round(category_confidence, 2)
    }


def extract_clean_description(description: str) -> str:
    """
    Remove priority indicators from description for cleaner task text.

    Args:
        description: Original task description

    Returns:
        Cleaned description
    """
    # Remove common priority prefixes
    cleaned = re.sub(r"^(urgent:|asap:|important:|critical:)\s*", "", description, flags=re.IGNORECASE)

    # Remove multiple exclamation marks (keep one if present)
    cleaned = re.sub(r"!{2,}", "!", cleaned)

    return cleaned.strip()


# Test cases for validation
if __name__ == "__main__":
    test_cases = [
        "URGENT: Finish project report by tomorrow!!!",
        "Buy groceries from the supermarket",
        "Meeting with client at 3pm",
        "Maybe read a book when I have time",
        "Doctor appointment for annual checkup",
        "Submit quarterly budget proposal deadline today",
        "Pick up milk and eggs from store",
        "Exercise at gym",
        "Call boss about project status",
        "Someday learn to play guitar"
    ]

    print("AI Smart-Input Analyzer Test Cases")
    print("=" * 70)

    for task in test_cases:
        result = analyze_task_text(task)
        confidence = get_analysis_confidence(task, result)
        clean = extract_clean_description(task)

        print(f"\nTask: {task}")
        print(f"  Priority: {result['priority']} (confidence: {confidence['priority']})")
        print(f"  Category: {result['category']} (confidence: {confidence['category']})")
        print(f"  Cleaned: {clean}")
