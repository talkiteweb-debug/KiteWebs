"""Twilio WhatsApp inbound-message webhook.

Deploys to Vercel as a Python serverless function at /api/whatsapp.
Configure Twilio's "Inbound Message" webhook to point here:
    https://kitewebs.com/api/whatsapp

For each reply, logs the message and returns an empty TwiML response so Twilio
doesn't auto-reply. v2: classify the reply (interested/cold/unsubscribe), notify
Tal via email or push, and update the outreach queue status.
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


class handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        data = parse_qs(raw)

        from_phone = data.get("From", [""])[0]
        body = data.get("Body", [""])[0]
        profile_name = data.get("ProfileName", [""])[0]

        # TODO v2: persist to a store + classify + notify
        print(f"[inbound] {profile_name} {from_phone}: {body[:200]}")

        self.send_response(200)
        self.send_header("Content-Type", "text/xml")
        self.end_headers()
        self.wfile.write(b"<Response></Response>")

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"KiteWebs inbound webhook is live. POST only.")
