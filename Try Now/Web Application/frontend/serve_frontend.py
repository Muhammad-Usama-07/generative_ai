"""
serve_frontend.py
Serves index.html and tryon.html over http://localhost:5500 instead of
opening them directly as file:// URLs.

Why this matters:
  Opening tryon.html by double-clicking it loads it as file:///Try%20Now/tryon.html.
  Browsers treat file:// pages as a unique, locked-down security origin —
  fetch() and FormData POSTs to http://localhost:8000 can be silently blocked
  or behave inconsistently depending on the browser. Serving over http://
  (even from a trivial local server) avoids this entirely.

Usage:
    python serve_frontend.py
    Then open: http://localhost:5500/tryon.html
"""

import http.server
import socketserver
import os

PORT = 5500
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Allow the page to fetch from the FastAPI backend on a different port
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving frontend from: {DIRECTORY}")
        print(f"Open in browser:       http://localhost:{PORT}/tryon.html")
        print(f"Or landing page:       http://localhost:{PORT}/index.html")
        print("Press Ctrl+C to stop.")
        httpd.serve_forever()