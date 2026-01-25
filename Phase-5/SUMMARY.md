# Phase 5: AI Smart-Input Analyzer

## Overview
Phase 5 enhances the todo application with intelligent task analysis capabilities. The AI Smart-Input Analyzer automatically detects task priority and category from natural language descriptions, reducing manual input and improving task organization.

## Key Features

### 1. Priority Detection
- **High Priority**: Automatically detects urgent tasks using keywords like "urgent", "ASAP", "critical", "deadline", "today"
- **Low Priority**: Identifies non-urgent tasks with keywords like "maybe", "sometime", "optional", "when possible"
- **Medium Priority**: Default when no strong indicators are present

### 2. Category Classification
- **Work**: Tasks related to meetings, projects, emails, clients, business activities
- **Personal**: Health, family, study, hobbies, personal appointments (includes "study" keyword)
- **Shopping**: Purchases, groceries, ordering, shopping trips
- **Other**: Default category when no specific keywords are detected

### 3. Contextual Pattern Matching
- Uses regex patterns to detect contextual clues like due dates ("due today", "before Friday")
- Recognizes urgency indicators like multiple exclamation marks (!!!)
- Understands time constraints ("finish by tomorrow")

## Technical Implementation

### Files
- `ai_analyzer.py`: Core AI analysis module with keyword dictionaries and detection algorithms
- `api.py`: Flask API endpoints for task analysis
- `index.html`: Web interface for testing the analyzer

### How It Works
1. **Text Processing**: Converts input to lowercase for consistent matching
2. **Keyword Scoring**: Scores tasks based on keyword frequency in both priority and category dictionaries
3. **Pattern Matching**: Applies regex patterns to detect contextual information
4. **Decision Logic**: Returns the highest-scoring priority and category

## How to Test

To demonstrate the AI Smart-Input Analyzer features in your demo, type these three sentences:

1. **Study Feature**: "Study for math exam this weekend" - This will be automatically categorized as "Personal" due to the "study" keyword

2. **Shopping Feature**: "Buy groceries for dinner party" - This will be categorized as "Shopping" and detected as a shopping-related task

3. **Urgent Feature**: "Urgent: Submit quarterly report by 5 PM today!!!" - This will be flagged as "High" priority and categorized as "Work" based on urgency indicators and work-related keywords

## Integration Points
- Can be integrated with Phase 4's task management API
- Works as a standalone analysis service
- Provides RESTful API endpoints for easy integration

## Benefits
- Reduces manual task categorization effort
- Improves task prioritization accuracy
- Enhances user experience with intelligent defaults
- Adaptable to different domains with customizable keyword dictionaries