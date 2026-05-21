import sqlite3

DB = "neurojustice.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        question TEXT,
        answer TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_case(date, cat, q, a):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO history(date,category,question,answer)
    VALUES (?,?,?,?)
    """, (date, cat, q, a))

    conn.commit()
    conn.close()

def get_all_cases():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    SELECT date, category, question, answer
    FROM history
    ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_cases():
    conn = sqlite3.connect("neurojustice.db")
    cur = conn.cursor()

    cur.execute("SELECT date, category, question, answer FROM history ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return rows


def delete_all():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM history")

    conn.commit()
    conn.close()