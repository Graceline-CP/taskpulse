from datetime import datetime, timedelta

from database import get_connection, init_db


init_db()

conn = get_connection()

# Clear old demo data
conn.execute("DELETE FROM tasks")

tasks = [
    ("Complete Python assignment", "Finish the backend assignment", 1),
    ("Study Java", "Prepare for the upcoming practical", 1),
    ("Work on TaskPulse", "Complete the capstone project", 0),
    ("Read research paper", "Read one AI research paper", 0),
    ("Practice SQL", "Practice aggregation queries", 1),
]

for title, description, completed in tasks:
    conn.execute(
        """
        INSERT INTO tasks
        (user_id, title, description, completed, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            1,
            title,
            description,
            completed,
            (datetime.now() - timedelta(days=1)).isoformat()
        )
    )

conn.commit()
conn.close()

print("Demo tasks seeded successfully.")