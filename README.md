## Overview
SOQS is a command-line Python quiz system that allows users to take timed quizzes, view leaderboards, and provides administrators with tools to manage quiz content. The system features:

- Timed quizzes with random question selection
- Performance feedback and score tracking
- Leaderboard with top scores
- Admin panel for question management
- File-based data storage (JSON)

## Requirements
- Python 3.x
- No additional libraries required

## Installation
1. Clone or download the repository
2. Navigate to the project directory in your terminal

## How to Run
Execute the main script:
```bash
python main.py
```

## System Features
### User Functions
1. **Take Quiz**:
   - Enter your name to start
   - Answer 10 random questions within 5 minutes
   - Get immediate feedback and final score

2. **View Leaderboard**:
   - Displays top 10 scores
   - Shows name, score, time, and timestamp

3. **Search Questions**:
   - Search quiz questions by keyword

### Admin Functions (Password: `PASSWORD`)
1. **Add Questions**:
   - Add new questions with options and correct answers
   - Automatic duplicate prevention

2. **Search/Edit Questions**:
   - Find questions by keyword
   - Edit existing questions or delete them

3. **Import Questions**:
   - Bulk import from text files (see `1.txt` for format example)
   - Place import files in `/data` directory

## File Structure
```
├── main.py             # Main application
├── quiz.py             # Quiz logic and functions
├── admin.py            # Admin management tools
├── utils.py            # Helper functions
├── data/               # Data storage
│   ├── question.json   # Quiz questions database
│   ├── leaderboard.json# Score records
│   └── 1.txt           # Sample import file
└── README.md           # This documentation
```

## Data Formats
### Question Import Format (`1.txt`)
```
1:Question text?
A. Option 1
B. Option 2
C. Option 3
D. Option 4
Correct Answer: A
Explanation: Detailed explanation
```

### JSON Structures
**question.json**:
```json
[
  {
    "question": "Sample question?",
    "options": ["A. Choice1", "B. Choice2", "C. Choice3", "D. Choice4"],
    "correct_answer": "A",
    "explanation": "Answer explanation"
  }
]
```

**leaderboard.json**:
```json
[
  {
    "name": "Player1",
    "score": 90,
    "time": "00:05:32.100",
    "timestamp": "2025-08-10 14:30:00"
  }
]
```

## Troubleshooting
- If files are missing, the system will automatically create required data files
- Ensure text import files follow the exact format shown in `1.txt`
- Admin password is case-sensitive: `PASSWORD`