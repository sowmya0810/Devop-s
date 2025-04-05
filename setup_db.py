import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('floretworld.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("Database and table created successfully.")
