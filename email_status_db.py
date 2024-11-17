import sqlite3
from datetime import datetime

# Database file
DB_FILE = "email_status.db"

# Function to initialize the database and table
def initialize_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # Create the email_logs table if it does not already exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            delivery_status TEXT NOT NULL,
            opened TEXT DEFAULT 'No',
            timestamp TEXT NOT NULL
        )
        """)
        conn.commit()

# Function to log email status
def log_email_status(recipient_email, subject, delivery_status, opened="No"):
    # Ensure the database is initialized before logging
    initialize_db()
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # Insert the email log into the table
        cursor.execute("""
        INSERT INTO email_logs (recipient_email, subject, delivery_status, opened, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (recipient_email, subject, delivery_status, opened, timestamp))
        conn.commit()

# Function to update the opened status of an email
def update_opened_status(recipient_email, subject):
    # Ensure the database is initialized before updating
    initialize_db()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # Update the opened status to 'Yes' for the matching email
        cursor.execute("""
        UPDATE email_logs
        SET opened = 'Yes'
        WHERE recipient_email = ? AND subject = ?
        """, (recipient_email, subject))
        conn.commit()

# Function to fetch the log details
def get_log_details():
    # Ensure the database is initialized before fetching logs
    initialize_db()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # Retrieve all rows from the email_logs table
        cursor.execute("SELECT * FROM email_logs")
        rows = cursor.fetchall()
        # Convert the rows into a list of dictionaries for easy access
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
