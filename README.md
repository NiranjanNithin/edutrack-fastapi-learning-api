# EduTrack – Micro-Learning Progress & Analytics API

EduTrack is a backend REST API built using **FastAPI** and **SQLite** to track user learning progress, 
manage course enrollments, and provide analytics for a micro-learning platform.

---

## 📌 Features

✅ User management  
✅ Course management  
✅ Enrollment system with validation  
✅ Lesson completion tracking  
✅ Automated achievement system  
✅ User dashboard with progress tracking  
✅ Leaderboard (SQL optimized aggregation)

---

## 🏗️ Tech Stack

- **Backend:** FastAPI (Python 3.10+)
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic

---
## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/NiranjanNithin/edutrack-fastapi-learning-api
cd edutrack-fastapi-learning-api

### 2️⃣ Install Dependencies
pip install -r requirements.txt

### 3️⃣ Run Application
uvicorn app.main:app --reload

🌐 API Documentation
After starting server:
👉 http://127.0.0.1:8000/docs

📊 Core APIs
✅ User

POST /users → Create user
GET /users/{id} → Get user

✅ Course

GET /courses → List all courses (seeded)
POST /courses → Create course

✅ Enrollment

POST /enrollments → Enroll user
POST /enrollments/{id}/complete-lesson → Complete lesson

✅ Dashboard

GET /users/{id}/dashboard → User progress

✅ Analytics

GET /analytics/leaderboard → Top 5 users


🧠 Business Logic
✅ Enrollment Rules

Prevent duplicate active enrollments

✅ Completion Logic

Auto-complete course when lessons finished
Update status → completed
Add completed_at timestamp


🏆 Achievement System
🎯 Fast Starter

Awarded when user completes their first course

🎯 Deep Diver

Awarded when user completes a course with ≥ 10 lessons


📊 Leaderboard Logic

Uses optimized SQL aggregation:

SQLSUM(completed_lessons_count)GROUP BY userORDER BY DESCLIMIT 5Show more lines
✅ No Python sorting (performance optimized)

🌱 Seed Data
On application startup:

Python Basics (5 lessons)
Intro to FastAPI (3 lessons)
SQL 101 (10 lessons)


⚠️ Error Handling

400 → Duplicate enrollment / invalid request
404 → Resource not found
Validation errors handled via Pydantic
