from datetime import datetime
from pathlib import Path
from fastapi.responses import FileResponse
from reports import generate_pdf
from scheduler import start_scheduler
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from scheduler import generate_daily_report
from fastapi.security import OAuth2PasswordRequestForm
from database import get_connection, init_db
from auth import (
    hash_password,
    verify_password,
    create_token,
    get_current_user
)


app = FastAPI(title="TaskPulse API")


@app.on_event("startup")
def startup():
    init_db()
    start_scheduler()

class RegisterRequest(BaseModel):
    username: str
    password: str


class TaskRequest(BaseModel):
    title: str
    description: str = ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/register", status_code=201)
def register(data: RegisterRequest):
    conn = get_connection()

    existing = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        (data.username,)
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    password_hash = hash_password(data.password)

    cursor = conn.execute(
        """
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
        """,
        (data.username, password_hash)
    )

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "id": user_id,
        "username": data.username
    }

@app.post("/reports/test")
def test_report(
    current_user=Depends(get_current_user)
):
    return generate_daily_report()

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (form_data.username,)
    ).fetchone()

    conn.close()

    if user is None or not verify_password(
        form_data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_token(user["id"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/tasks", status_code=201)
def create_task(
    data: TaskRequest,
    current_user=Depends(get_current_user)
):
    conn = get_connection()

    created_at = datetime.now().isoformat()

    cursor = conn.execute(
        """
        INSERT INTO tasks
        (user_id, title, description, completed, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            current_user["id"],
            data.title,
            data.description,
            0,
            created_at
        )
    )

    task_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "id": task_id,
        "title": data.title,
        "description": data.description,
        "completed": False,
        "created_at": created_at
    }


@app.get("/tasks")
def get_tasks(
    current_user=Depends(get_current_user)
):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM tasks
        WHERE user_id = ?
        ORDER BY id
        """,
        (current_user["id"],)
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.post("/reports", status_code=201)
def create_report(
    current_user=Depends(get_current_user)
):
    conn = get_connection()

    created_at = datetime.now().isoformat()

    cursor = conn.execute(
        """
        INSERT INTO reports (path, created_at)
        VALUES (?, ?)
        """,
        ("", created_at)
    )

    report_id = cursor.lastrowid

    output_path = generate_pdf(report_id)

    conn.execute(
        """
        UPDATE reports
        SET path = ?
        WHERE id = ?
        """,
        (str(output_path), report_id)
    )

    conn.commit()
    conn.close()

    return {
        "id": report_id,
        "file": f"/reports/{report_id}/file"
    }


@app.get("/reports/{report_id}")
def get_report(
    report_id: int,
    current_user=Depends(get_current_user)
):
    conn = get_connection()

    report = conn.execute(
        """
        SELECT *
        FROM reports
        WHERE id = ?
        """,
        (report_id,)
    ).fetchone()

    conn.close()

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return dict(report)


@app.get("/reports/{report_id}/file")
def download_report(
    report_id: int,
    current_user=Depends(get_current_user)
):
    conn = get_connection()

    report = conn.execute(
        """
        SELECT *
        FROM reports
        WHERE id = ?
        """,
        (report_id,)
    ).fetchone()

    conn.close()

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    path = Path(report["path"])

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )

    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename=f"taskpulse-report-{report_id}.pdf"
    )