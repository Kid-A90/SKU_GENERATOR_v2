import sqlite3

# Create a new SQLite database or connect to an existing one
conn = sqlite3.connect("sku.db")
c = conn.cursor()

# Create the `skus` table
c.execute("""
    CREATE TABLE IF NOT EXISTS skus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        base_number TEXT,
        suffix TEXT,
        used INTEGER DEFAULT 0
    )
""")

# Generate SKUs for base numbers 9000-9003 and suffixes AA-ZZ
base_numbers = [f"{i:04d}" for i in range(9000, 9003)]
suffixes = [f"{chr(a)}{chr(b)}" for a in range(65, 91) for b in range(65, 91)]  # AA to ZZ

# Insert all SKUs into the database
for base in base_numbers:
    for suffix in suffixes:
        c.execute("INSERT INTO skus (base_number, suffix, used) VALUES (?, ?, 0)", (base, suffix))

conn.commit()
conn.close()

print("Database initialized successfully with SKUs from 9000-AA to 9003-ZZ.")

