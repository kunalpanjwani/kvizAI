# kvizAI Database Documentation

## Overview

The kvizAI application uses SQLAlchemy with async support and SQLite for development. The database schema is designed to support a comprehensive quiz platform with AI-powered quiz generation, user management, leaderboards, and achievements.

## Database Models

### 1. User Model (`users` table)
**Purpose**: Store user accounts and authentication information

**Key Fields**:
- `id`: UUID primary key
- `email`: Unique email address
- `username`: Unique username
- `password_hash`: Hashed password
- `profile_picture`: URL to profile image
- `bio`: User biography
- `total_score`: Cumulative score across all quizzes
- `quizzes_taken`: Number of quizzes completed
- `quizzes_created`: Number of questionnaires created

**Relationships**:
- One-to-Many with Questionnaires (creator)
- One-to-Many with Quizzes (creator)
- One-to-Many with QuizAttempts
- One-to-Many with Leaderboard entries
- One-to-Many with UserAchievements

### 2. Questionnaire Model (`questionnaires` table)
**Purpose**: Store custom questionnaires created by users for AI quiz generation

**Key Fields**:
- `id`: UUID primary key
- `creator_id`: Foreign key to User
- `title`: Questionnaire title
- `description`: Questionnaire description
- `subject`: Subject category
- `difficulty_level`: easy, medium, hard
- `questions`: JSON field storing questionnaire questions
- `is_public`: Whether questionnaire is publicly accessible
- `is_template`: Whether it's a template questionnaire

**Relationships**:
- Many-to-One with User (creator)
- One-to-Many with Quizzes

### 3. Quiz Model (`quizzes` table)
**Purpose**: Store generated quizzes from questionnaires or AI processing

**Key Fields**:
- `id`: UUID primary key
- `questionnaire_id`: Foreign key to Questionnaire (optional)
- `creator_id`: Foreign key to User (optional)
- `title`: Quiz title
- `questions`: JSON field storing quiz questions
- `correct_answers`: JSON field storing correct answers
- `time_limit`: Time limit in minutes
- `difficulty`: easy, medium, hard
- `max_score`: Maximum possible score
- `is_global`: Whether it's a global quick quiz
- `ai_model_used`: Which AI model generated the quiz
- `generation_time`: Time taken to generate quiz

**Relationships**:
- Many-to-One with Questionnaire
- Many-to-One with User (creator)
- One-to-Many with QuizAttempts
- One-to-Many with Leaderboard entries

### 4. QuizAttempt Model (`quiz_attempts` table)
**Purpose**: Track user attempts at quizzes with detailed performance metrics

**Key Fields**:
- `id`: UUID primary key
- `user_id`: Foreign key to User
- `quiz_id`: Foreign key to Quiz
- `score`: User's score
- `max_score`: Maximum possible score
- `percentage`: Percentage score
- `time_taken`: Time taken in seconds
- `answers`: JSON field storing user answers
- `correct_answers`: Number of correct answers
- `incorrect_answers`: Number of incorrect answers
- `skipped_answers`: Number of skipped questions
- `accuracy`: Percentage accuracy
- `speed`: Average time per question

**Relationships**:
- Many-to-One with User
- Many-to-One with Quiz

### 5. Leaderboard Model (`leaderboards` table)
**Purpose**: Track user rankings and scores for competitions

**Key Fields**:
- `id`: UUID primary key
- `quiz_id`: Foreign key to Quiz
- `user_id`: Foreign key to User
- `attempt_id`: Foreign key to QuizAttempt
- `rank`: User's rank
- `score`: User's score
- `percentage`: Percentage score
- `time_taken`: Time taken in seconds
- `accuracy`: Percentage accuracy
- `speed`: Average time per question
- `leaderboard_type`: quiz, global, daily

**Relationships**:
- Many-to-One with Quiz
- Many-to-One with User
- Many-to-One with QuizAttempt

### 6. Achievement Model (`achievements` table)
**Purpose**: Define available achievements and badges

**Key Fields**:
- `id`: UUID primary key
- `name`: Achievement name
- `description`: Achievement description
- `icon`: Icon identifier
- `category`: quiz, score, time, streak, etc.
- `criteria_type`: Type of criteria (quizzes_taken, score_threshold, etc.)
- `criteria_value`: Value needed to unlock
- `criteria_condition`: gte, lte, eq
- `rarity`: common, rare, epic, legendary

**Relationships**:
- One-to-Many with UserAchievements

### 7. UserAchievement Model (`user_achievements` table)
**Purpose**: Track user's progress and earned achievements

**Key Fields**:
- `id`: UUID primary key
- `user_id`: Foreign key to User
- `achievement_id`: Foreign key to Achievement
- `progress`: Current progress towards achievement
- `is_unlocked`: Whether achievement is unlocked
- `unlocked_at`: When achievement was unlocked

**Relationships**:
- Many-to-One with User
- Many-to-One with Achievement

### 8. AIModelUsage Model (`ai_model_usage` table)
**Purpose**: Track AI model performance and usage statistics

**Key Fields**:
- `id`: UUID primary key
- `model_name`: AI model name (llama2, gemini, etc.)
- `model_version`: Model version
- `request_count`: Total requests
- `success_count`: Successful requests
- `error_count`: Failed requests
- `total_processing_time`: Total processing time in milliseconds
- `average_processing_time`: Average processing time
- `min_processing_time`: Minimum processing time
- `max_processing_time`: Maximum processing time
- `last_error`: Last error message
- `is_active`: Whether model is active

## Database Setup

### Prerequisites
- Python 3.11+
- SQLAlchemy 2.0+
- Alembic (for migrations)

### Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Initialize database**:
```bash
python init_db.py
```

3. **Run migrations** (if using Alembic):
```bash
alembic upgrade head
```

### Environment Variables

Configure the following environment variables in `.env`:

```env
DATABASE_URL=sqlite:///./kvizai.db
SECRET_KEY=your-secret-key-change-in-production
```

## Database Schema Diagram

```
Users
├── Questionnaires (1:N)
├── Quizzes (1:N)
├── QuizAttempts (1:N)
├── Leaderboards (1:N)
└── UserAchievements (1:N)

Questionnaires
├── User (N:1)
└── Quizzes (1:N)

Quizzes
├── Questionnaire (N:1)
├── User (N:1)
├── QuizAttempts (1:N)
└── Leaderboards (1:N)

QuizAttempts
├── User (N:1)
├── Quiz (N:1)
└── Leaderboards (1:N)

Leaderboards
├── Quiz (N:1)
├── User (N:1)
└── QuizAttempt (N:1)

Achievements
└── UserAchievements (1:N)

UserAchievements
├── User (N:1)
└── Achievement (N:1)

AIModelUsage (standalone)
```

## Data Types

### JSON Fields
Several models use JSON fields to store flexible data:

- **Questionnaire.questions**: Array of question objects
- **Quiz.questions**: Array of quiz question objects
- **Quiz.correct_answers**: Array of correct answer indices
- **QuizAttempt.answers**: Object mapping question IDs to user answers

### Example JSON Structures

**Questionnaire Questions**:
```json
[
  {
    "id": "q1",
    "text": "What is the capital of France?",
    "type": "multiple_choice",
    "options": ["London", "Paris", "Berlin", "Madrid"],
    "correct_answer": 1
  }
]
```

**Quiz Questions**:
```json
[
  {
    "id": "q1",
    "text": "What is the capital of France?",
    "type": "multiple_choice",
    "options": ["London", "Paris", "Berlin", "Madrid"],
    "points": 10
  }
]
```

**Quiz Attempt Answers**:
```json
{
  "q1": 1,
  "q2": 0,
  "q3": null
}
```

## Indexes

The following indexes are automatically created:

- `users.email` (unique)
- `users.username` (unique)
- `questionnaires.creator_id`
- `quizzes.questionnaire_id`
- `quizzes.creator_id`
- `quiz_attempts.user_id`
- `quiz_attempts.quiz_id`
- `leaderboards.quiz_id`
- `leaderboards.user_id`
- `user_achievements.user_id`
- `user_achievements.achievement_id`

## Performance Considerations

1. **JSON Queries**: Use database-specific JSON functions for efficient querying
2. **Indexes**: Additional indexes may be needed based on query patterns
3. **Pagination**: Implement pagination for large result sets
4. **Caching**: Consider Redis for frequently accessed data

## Backup and Migration

### Backup
```bash
# SQLite backup
cp kvizai.db kvizai_backup.db

# PostgreSQL backup
pg_dump -h localhost -U username -d kvizai > backup.sql
```

### Migration
```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Security Considerations

1. **Password Hashing**: Use bcrypt or similar for password hashing
2. **SQL Injection**: SQLAlchemy ORM prevents SQL injection
3. **Data Validation**: Validate all input data before database operations
4. **Access Control**: Implement proper authorization checks
5. **Audit Trail**: Consider adding audit fields for sensitive operations

## Troubleshooting

### Common Issues

1. **Database Lock**: Ensure only one process accesses SQLite database
2. **Migration Errors**: Check for schema conflicts and resolve manually
3. **Performance**: Monitor query performance and add indexes as needed
4. **Memory Usage**: Large JSON fields may impact memory usage

### Debug Queries

Enable SQL logging in development:
```python
# In config.py
DEBUG = True
```

This will log all SQL queries to the console for debugging. 