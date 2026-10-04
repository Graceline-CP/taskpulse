# My 10x Solution - Graceline CP

## Project: TaskPulse

### 1. Problem

Students often manage academic and personal tasks across different places,
making it difficult to track completed and pending work. Manually reviewing
tasks to understand daily productivity takes time and does not provide a
clear summary. TaskPulse solves this problem by providing a simple,
authenticated task management system with automatic productivity reporting.

### 2. 10x Solution

TaskPulse provides an authenticated API for managing tasks and generating
productivity reports. Instead of manually reviewing individual tasks, users
can view their progress through a report containing task totals, completed
tasks, pending tasks and completion percentage.

The solution aims to reduce daily productivity review from several minutes
of manual checking to a few seconds through automated reporting.

### 3. Target Users

Students and individuals who want a simple way to manage tasks and review
their productivity.

### 4. Concepts Implemented

#### 1. API Endpoints

FastAPI provides endpoints for authentication, task management and report
generation.

#### 2. Database

SQLite provides persistent storage for users, tasks and generated reports.

#### 3. Authentication

JWT-based authentication protects task and report endpoints.

#### 4. Background/Cron Jobs

APScheduler runs a scheduled productivity-report calculation job in the
background.

#### 5. Reporting — PDF

Playwright converts the productivity report into a downloadable PDF.

### 5. Swaps

No swaps were required. All five concepts were implemented directly from
the core concept list.

### 6. Non-goal

A mobile application and advanced graphical dashboard are outside the scope
of this capstone.

### 7. How It Works

1. A user registers an account.
2. The user logs in and receives an authentication token.
3. The token protects task and report endpoints.
4. Tasks are stored persistently in SQLite.
5. A productivity report calculates task statistics.
6. The scheduled background job runs the productivity-report calculation.
7. Playwright converts the report into a PDF.
8. The PDF can be downloaded through the API.

### 8. How to Run

1. Create and activate the Python virtual environment.
2. Install the required dependencies.
3. Run the seed script to add demo tasks.
4. Start the FastAPI server.
5. Open `/docs`.
6. Register and log in.
7. Authorize using the JWT token.
8. Create or view tasks.
9. Generate a report using the report endpoint.
10. Download the generated PDF.

### 9. Technology

- Python
- FastAPI
- SQLite
- JWT
- APScheduler
- Playwright
- HTML/CSS

### 10. Future Ideas

- Email delivery of daily reports
- Task priorities and categories
- Productivity trends
- Deployment to a free hosting platform