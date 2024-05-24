import sqlite3
from hashlib import sha256

# Database setup
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')
conn.commit()

def hash_password(password):
    return sha256(password.encode()).hexdigest()