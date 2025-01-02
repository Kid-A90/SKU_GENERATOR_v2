import sqlite3

conn = sqlite3.connect("sku.db")
c = conn.cursor()

# Check total SKUs
c.execute("SELECT COUNT(*) FROM skus")
print("Total SKUs:", c.fetchone()[0])

# Check the first few SKUs
c.execute("SELECT * FROM skus LIMIT 10")
print("Sample SKUs:", c.fetchall())

conn.close()
