# TaskPulse

TaskPulse is a backend productivity and task management system built as a
capstone project. It allows authenticated users to manage tasks and generate
productivity reports as downloadable PDF files.

## Problem

Students often manage academic and personal tasks across different places.
This makes it difficult to track completed and pending work and understand
daily productivity.

TaskPulse provides one simple system for managing tasks and reviewing
productivity through automatically calculated reports.

## 10x Solution

TaskPulse reduces the time required to review daily task progress by
calculating productivity statistics and presenting them in a downloadable
PDF report.

Instead of manually checking individual tasks, users can see:

- Total tasks
- Completed tasks
- Pending tasks
- Completion percentage
- Individual task details

## Concepts Implemented

| Concept | Implementation | Location |
|---|---|---|
| API Endpoints | FastAPI REST endpoints | `main.py` |
| Database | Persistent SQLite database | `database.py` |
| Authentication | JWT authentication with protected routes | `auth.py`, `main.py` |
| Background/Cron Jobs | Scheduled productivity calculation | `scheduler.py` |
| Reporting - PDF | HTML to PDF report generation | `reports.py` |

No swaps were required. All five concepts were implemented directly from
the core concept list.

## Features

1. User registration and login
2. JWT-protected task management
3. Persistent task storage
4. Scheduled productivity reporting
5. Downloadable PDF productivity reports

## Project Structure

```text
taskpulse/
│
├── main.py
├── database.py
├── auth.py
├── scheduler.py
├── reports.py
├── seed.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── report.html
│
└── reports/

The database file and generated PDF reports are created locally and are
excluded from Git.
Technologies
- Python
- FastAPI
- SQLite
- JWT
- APScheduler
- Playwright
- HTML/CSS
- Uvicorn
Requirements
- Python 3.10+
- Google Chrome
- Internet connection for installing Python packages
Installation
Clone the repository:
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd taskpulse

Create a virtual environment:
py -m venv .venv

Activate it on Windows PowerShell:
.\.venv\Scripts\Activate.ps1

Install dependencies:
pip install -r requirements.txt

Seed Demo Data
Run:
py seed.py

Expected output:
Demo tasks seeded successfully.

Run the Application
Start the FastAPI server:
py -m uvicorn main:app

Open the API documentation:
http://127.0.0.1:8000/docs

API Endpoints
Health
GET /health

Authentication
POST /register
POST /login

Tasks
POST /tasks
GET /tasks

Task endpoints require authentication.
Reports
POST /reports
GET /reports/{report_id}
GET /reports/{report_id}/file

Background Report Test
POST /reports/test

This endpoint manually triggers the productivity report calculation for
testing.
5-Minute Demo
1. Start the FastAPI server.
2. Open http://127.0.0.1:8000/docs.
3. Register a new user.
4. Log in using the Swagger authentication flow.
5. Click Authorize.
6. Create a task using POST /tasks.
7. View tasks using GET /tasks.
8. Generate a report using POST /reports.
9. Open GET /reports/{report_id}/file.
10. Download and view the generated PDF.
The PDF displays the total number of tasks, completed tasks, pending tasks,
completion percentage and task details.
Background Job
APScheduler runs the productivity report calculation once per day at
11:59 PM.
The scheduler can also be tested manually using:
POST /reports/test

PDF Report
The PDF is generated using Playwright and contains:
- Report generation timestamp
- Total tasks
- Completed tasks
- Pending tasks
- Completion percentage
- Task details table
Example demo result:
Total Tasks:       5
Completed:         3
Pending:           2
Completion Rate:   60%

Security
Authentication tokens are required for protected task and report endpoints.
Passwords are stored as hashes rather than plain text.
Environment files, databases, virtual environments and generated reports
are excluded using .gitignore.
Future Ideas
- Email delivery of daily reports
- Task priorities and categories
- Productivity trends
- Deployment to a free hosting platform
Capstone
Your 10x Solution — Backend Track
Built as a capstone project demonstrating five program concepts:
1. API endpoints
2. Database
3. Authentication
4. Background/Cron jobs
5. PDF reporting