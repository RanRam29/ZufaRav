import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT", 5432)
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  rank TEXT,
  role TEXT,
  id_number TEXT,
  phone_number TEXT,
  full_name TEXT,
  email TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS events (
  id SERIAL PRIMARY KEY,
  title TEXT,
  location TEXT,
  reporter TEXT,
  lat REAL,
  lng REAL,
  address TEXT,
  confirmed BOOLEAN DEFAULT false,
  confirmed_by TEXT,
  confirmed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS events_archive (
  id INTEGER PRIMARY KEY,
  title TEXT,
  location TEXT,
  reporter TEXT,
  lat REAL,
  lng REAL,
  address TEXT,
  confirmed BOOLEAN,
  confirmed_by TEXT,
  confirmed_at TIMESTAMP,
  created_at TIMESTAMP,
  deleted_by TEXT,
  deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tracking (
  id SERIAL PRIMARY KEY,
  username TEXT,
  lat REAL,
  lng REAL,
  timestamp TIMESTAMP DEFAULT now()
);
""")

conn.commit()
cursor.close()
conn.close()

print("✅ כל הטבלאות נוצרו בהצלחה במסד הנתונים החדש!")
