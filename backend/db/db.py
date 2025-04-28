from dotenv import load_dotenv
import psycopg2
import os

# טען את הקובץ ממיקום ידני
load_dotenv(dotenv_path=".env")

def get_db():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432)
    )
