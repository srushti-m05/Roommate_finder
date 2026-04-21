import sqlite3

def get_db():
    return sqlite3.connect("roommate.db")

def init_db():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        uid TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        city TEXT,
        area TEXT,
        food TEXT,
        sleep TEXT,
        smoking TEXT,
        drinking TEXT,
        cleanliness TEXT,
        occupation TEXT,
        timing TEXT,
        password TEXT
    )
    """)
    con.commit()
    con.close()
