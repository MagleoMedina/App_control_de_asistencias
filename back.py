import libsql
import os
from dotenv import load_dotenv


load_dotenv()

url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")



conn = libsql.connect("salu.db", sync_url=url, auth_token=auth_token)
conn.sync()

conn.execute("CREATE TABLE IF NOT EXISTS machete (id INTEGER);")
conn.execute("INSERT INTO machete(id) VALUES (1);")
conn.commit()

conn.sync()

print(conn.execute("select * from machete").fetchall())