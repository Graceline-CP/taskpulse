from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from database import get_connection


def generate_daily_report():
    conn = get_connection()

    total = conn.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    completed = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 1"
    ).fetchone()[0]

    pending = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 0"
    ).fetchone()[0]

    conn.close()

    completion_rate = (
        round((completed / total) * 100, 2)
        if total > 0
        else 0
    )

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_rate": completion_rate
    }

    print("\n===== DAILY PRODUCTIVITY REPORT =====")
    print(report)
    print("=====================================\n")

    return report


scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(
        generate_daily_report,
        "cron",
        hour=23,
        minute=59,
        id="daily_productivity_report",
        replace_existing=True
    )

    scheduler.start()
    print("Background scheduler started.")