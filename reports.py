import sqlite3
from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright

from database import get_connection


REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def generate_pdf(report_id):
    conn = get_connection()

    tasks = conn.execute(
        """
        SELECT id, title, description, completed, created_at
        FROM tasks
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    tasks = [dict(task) for task in tasks]

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task["completed"]
    )

    pending_tasks = total_tasks - completed_tasks

    completion_rate = (
        round((completed_tasks / total_tasks) * 100, 2)
        if total_tasks > 0
        else 0
    )

    generated_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    rows = ""

    for task in tasks:
        status = (
            "Completed"
            if task["completed"]
            else "Pending"
        )

        rows += f"""
        <tr>
            <td>{task["id"]}</td>
            <td>{task["title"]}</td>
            <td>{task["description"]}</td>
            <td>{status}</td>
            <td>{task["created_at"]}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <title>TaskPulse Productivity Report</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                color: #222;
            }}

            h1 {{
                margin-bottom: 5px;
            }}

            .date {{
                color: #666;
                margin-bottom: 30px;
            }}

            .summary {{
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
            }}

            .card {{
                border: 1px solid #ddd;
                padding: 15px;
                width: 150px;
            }}

            .number {{
                font-size: 24px;
                font-weight: bold;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}

            th {{
                background: #f2f2f2;
            }}

            thead {{
                display: table-header-group;
            }}

            tr {{
                break-inside: avoid;
                page-break-inside: avoid;
            }}

        </style>

    </head>

    <body>

        <h1>TaskPulse Productivity Report</h1>

        <div class="date">
            Generated: {generated_at}
        </div>

        <div class="summary">

            <div class="card">
                <div>Total Tasks</div>
                <div class="number">{total_tasks}</div>
            </div>

            <div class="card">
                <div>Completed</div>
                <div class="number">{completed_tasks}</div>
            </div>

            <div class="card">
                <div>Pending</div>
                <div class="number">{pending_tasks}</div>
            </div>

            <div class="card">
                <div>Completion</div>
                <div class="number">{completion_rate}%</div>
            </div>

        </div>

        <h2>Task Details</h2>

        <table>

            <thead>

                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Status</th>
                    <th>Created</th>
                </tr>

            </thead>

            <tbody>

                {rows}

            </tbody>

        </table>

    </body>

    </html>
    """

    output_path = REPORTS_DIR / f"{report_id}.pdf"

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            executable_path=CHROME_PATH
        )

        page = browser.new_page()

        page.set_content(html)

        page.pdf(
            path=str(output_path),
            format="A4",
            print_background=True
        )

        browser.close()

    return output_path