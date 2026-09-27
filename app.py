import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import psycopg

BIND_HOST = os.environ.get("BIND_HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8080"))
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "events")
DB_USER = os.environ.get("DB_USER", "events")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "local-throwaway-password")

try:
    conn = psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True,
    )
except Exception as exc:
    print(f"could not connect to {DB_HOST}: {exc}")
    sys.exit(1)

print(f"connected to {DB_HOST}")
conn.execute(
    "CREATE TABLE IF NOT EXISTS events (id SERIAL PRIMARY KEY, note TEXT NOT NULL)"
)



class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/events":
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode()
            try:
                data = json.loads(body)
                if not isinstance(data, dict) or "note" not in data:
                    raise ValueError()
                note = data["note"]
                if not isinstance(note, str) or len(note) == 0 or len(note) > 200:
                    raise ValueError()
            
            except ValueError:
                self.send_response(400)
                self.end_headers()
                return
            row = conn.execute(
                "INSERT INTO events (note) VALUES (%s) RETURNING id, note", (note,)
            ).fetchone()
            response = json.dumps({"id": row[0], "note": row[1]}).encode()
            self.send_response(201)

        else:
            response = b"not found\n"
            self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        if self.path == "/events":
            rows = conn.execute("SELECT id, note FROM events ORDER BY id").fetchall()
            events = [{"id": row[0], "note": row[1]} for row in rows]
            response = json.dumps(events).encode()
            self.send_response(200)
        else:
            response = b"not found\n"
            self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    print(f"listening on {BIND_HOST}:{PORT}")
    server = HTTPServer((BIND_HOST, PORT), Handler)
    server.serve_forever()
