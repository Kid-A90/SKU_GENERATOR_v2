import sqlite3

# Connect to a new or existing sku.db file
conn = sqlite3.connect("sku.db")
cursor = conn.cursor()

# Drop the old table if it exists
cursor.execute("DROP TABLE IF EXISTS skus;")

# Create a new table for SKUs
cursor.execute("""
    CREATE TABLE skus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        base_number TEXT,
        suffix TEXT,
        used INTEGER DEFAULT 0
    );
""")

# Populate the table with a smaller range of SKUs
base_numbers = ["9000", "9001", "9002"]  # Base numbers you want to include
suffixes = [f"{chr(i)}{chr(j)}" for i in range(65, 68) for j in range(65, 91)]  # AA to CZ

for base in base_numbers:
    for suffix in suffixes:
        cursor.execute("INSERT INTO skus (base_number, suffix) VALUES (?, ?)", (base, suffix))

# Commit changes and close the connection
conn.commit()
conn.close()

print("New sku.db has been created successfully!")
