import sqlite3

def init_db():
    try:
        con = sqlite3.connect("ams.db")
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                f_name TEXT,
                l_name TEXT,
                contact TEXT,
                email TEXT UNIQUE,
                question TEXT,
                answer TEXT,
                password TEXT
            )
        """)
        con.commit()
        con.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

init_db()
