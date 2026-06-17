import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

try:
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print("Connected to:", cur.fetchone()[0])
except Exception as e:
    print("Connection failed:", e)
