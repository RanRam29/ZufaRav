import os
import psycopg2
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# Run this script with the same env as your backend
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT", 5432)
)
cursor = conn.cursor()

print("\n✅ Connected to database")
print("🌐 Connected to DB:", os.getenv("POSTGRES_DB"))
print("👤 User:", os.getenv("POSTGRES_USER"))
print("🔗 Host:", os.getenv("POSTGRES_HOST"))

# ✅ Show actual DB connection context
cursor.execute("SELECT current_database(), inet_server_addr(), inet_client_addr(), current_user;")
db_info = cursor.fetchone()
print("\n🧠 DB Context:")
print(" - current_database:", db_info[0])
print(" - inet_server_addr:", db_info[1])
print(" - inet_client_addr:", db_info[2])
print(" - current_user:", db_info[3])

# List all tables across all schemas
cursor.execute("""
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
ORDER BY table_schema, table_name;
""")
tables = cursor.fetchall()
print("\n📦 All tables in DB:")
for schema, name in tables:
    print(f" - {schema}.{name}")

# Specifically check if users table exists in public
if any(name == "users" and schema == "public" for schema, name in tables):
    print("\n✅ 'users' table found in public schema. Columns:")
    cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' AND table_schema = 'public'")
    for row in cursor.fetchall():
        print(" -", row[0], row[1])
else:
    print("\n❌ 'users' table NOT found in public schema")

cursor.close()
conn.close()
print("\nDone.")