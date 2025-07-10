# 🔖 EchoTag

**EchoTag** is a smart asset recovery and contact system that allows anyone who finds a tagged item (via QR code) to easily report it, leave a message, optionally share location, and initiate anonymous or identified contact — all while notifying the owner through Discord and email.

---

## 🗂️ Folder & File Structure

EchoTag/
├── backend/ # Flask backend (API + messaging logic)
│ ├── app.py # Main entry point for Flask app
│ ├── routes.py # Handles /api/report and core logic
│ ├── config.py # Loads secrets securely from .env
│ ├── .env # Environment variables (Discord, Gmail secrets) – NEVER COMMIT
│ ├── templates/
│ │ └── echotag_email.html # HTML email template sent to Jeremy on scan
│ └── db/
│ ├── models.py # SQLAlchemy models (Device registry, logs)
│ └── **init**.py # DB connection utility (connect_db function)
│
├── web/ # Frontend: HTML pages served or static-hosted
│ ├── found.html # Main scan page with auth/anon toggle + form
│ ├── respond.html # Reconnect view to check replies (future)
│ └── style.css # Shared styling for all web pages
│
├── qr/ # QR code generation scripts
│ ├── generate_qr.py # Script to create QR codes per device
│ └── output/ # PNG/SVG exports of generated QR codes
│
├── static/ # Local storage for uploaded images (from finder)
│ └── uploads/ # Where images are temporarily saved before CDN
│
├── bot/ # (Optional) Discord bot logic (if standalone or future logic is needed)
│ └── echotag_bot.py # Code for thread creation, response relays, etc.
│
├── logs/ # Scan logs, submission records (optional, for expansion)
│
└── README.md # This documentation file

⸻

⚙️ Key Features
• QR-based identification per tool/device
• Anonymous or authenticated user submissions
• Optional image and geolocation capture
• Real-time alerts via:
• Discord thread (one per find event)
• HTML email to Jeremy
• Reconnect link for finders to check responses later

⸻

🚀 Setup Instructions

1. Install Dependencies

pip install flask python-dotenv requests smtplib email-validator sqlalchemy

2. Set Environment Variables

Create a .env file in backend/:

DISCORD_CHANNEL_ID=your_channel_id
DISCORD_BOT_TOKEN=your_discord_bot_token
GMAIL_USER=youremail@gmail.com
GMAIL_PASS=your_gmail_app_password

🔐 Keep this file secret. Never commit it to version control.

⸻

3. Run Flask Locally

export FLASK_APP=app.py
flask run

⸻

4. Generate QR Codes

Customize and run:

python qr/generate_qr.py

This will create a QR code that links to https://j-scan.me/?id=DEVICE_ID.

⸻

🧠 How It Works (High-Level) 1. Finder scans a QR code 2. Lands on found.html and submits a form 3. routes.py handles the report:
• Posts a message to a new Discord thread inside #echotag
• Sends an HTML email to Jeremy with full details 4. The finder is given a Reconnect Link to follow up later 5. (Future) respond.html will allow check-in or two-way chat

⸻

🧪 To Do (Next Steps)
• Implement respond.html logic to view thread/message log
• Store submission metadata in DB
• Optional: webhook or polling relay for reply visibility
• QR layout template for engraving

⸻

👋 Contact

Questions, contributions, or recovery logic ideas? Reach out via @echotag on Discord (private server) or submit a pull request.

⸻

© 2025 EchoTag | Smart Recovery Systems – Minimal effort, maximum return.
