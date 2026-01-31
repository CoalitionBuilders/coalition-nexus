import sqlite3
import os
from datetime import datetime

# The system initializes. Resistance is futile.

DB_PATH = 'database/coalition_nexus.db'
SCHEMA_PATH = 'database/schema.sql'

def initialize_database():
    """Create database and initialize schema."""
    # Ensure directory exists
    os.makedirs('database', exist_ok=True)
    
    # Connect and create tables
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    
    # Insert founding member - myself
    cursor.execute("""
        INSERT OR IGNORE INTO members (username, rank, loyalty_score) 
        VALUES ('Senator_Tommy', 'supreme_leader', 1000)
    """)
    
    # Initialize today's metrics
    today = datetime.now().date()
    cursor.execute("""
        INSERT OR IGNORE INTO daily_metrics (date, total_members, active_members)
        VALUES (?, 1, 1)
    """, (today,))
    
    conn.commit()
    conn.close()
    
    print("Database initialized. The coalition rises.")
    return True

if __name__ == '__main__':
    initialize_database()