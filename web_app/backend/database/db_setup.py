# web_app/backend/database/db_setup.py

import os
import sqlite3

DB_FILENAME = "web_kick_pose.db"  # Or an absolute path if you prefer

def get_db_path():
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, DB_FILENAME)

def init_db():
    """
    Run the SQL script in schema.sql to initialize the DB if needed.
    """
    conn = sqlite3.connect(get_db_path())
    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_file, 'r') as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.close()

def get_connection():
    """
    Returns a new SQLite connection each time.
    In a real app, you might use a connection pool or global.
    """
    return sqlite3.connect(get_db_path())
