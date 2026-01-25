"""
Simple AI Analyzer - Phase 5 Update
Checks for 'urgently' keyword and returns high priority.
"""
from typing import Dict

def analyze_task_text(description: str) -> Dict[str, str]:
    """
    Analyze task description for priority.

    Args:
        description: Task description text

    Returns:
        Dictionary with 'priority' and 'category' keys
    """
    if not description or not description.strip():
        return {"priority": "medium", "category": "other"}

    text_lower = description.lower()

    if "urgently" in text_lower:
        return {"priority": "high", "category": "other"}
    else:
        return {"priority": "medium", "category": "other"}

# Keep other functions minimal or remove if not needed, but API might use them
def get_analysis_confidence(description: str, detected: Dict[str, str]) -> Dict[str, float]:
    return {"priority": 1.0 if detected["priority"] == "high" else 0.5, "category": 0.5}

def extract_clean_description(description: str) -> str:
    return description.strip()

if __name__ == "__main__":
    print("Simple analyzer ready. Test with 'urgently...' for high priority.")