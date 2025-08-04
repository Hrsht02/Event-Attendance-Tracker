# Event Attendance Tracker Dashboard

## 📌 Overview
Web dashboard for tracking event RSVPs and attendance with real-time visualizations.

## ✨ Features
- Add/remove attendees (CRUD operations)
- Interactive pie charts for RSVP/attendance
- Key metrics display:
  - Total invited
  - Attendance rate 
  - No-shows count

## 🛠️ Installation
```bash
# 1. Clone repo
git clone https://github.com/yourusername/event-attendance-tracker.git

# 2. Install dependencies
pip install flask pandas matplotlib

# 3. Run app
python app.py

## 📂 File Structure
.
├── app.py               # Main Flask app
├── event_data.csv       # Sample data
├── static/
│   └── style.css        # Styles
└── templates/
    └── index.html       # Dashboard HTML
