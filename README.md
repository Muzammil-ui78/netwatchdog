# NetWatchdog
A Real-Time Network Intrusion Detection System (NIDS)

## What it does
NetWatchdog monitors all network traffic in real-time and automatically detects malicious activity, logs threats to MongoDB, displays them on a live dashboard, and sends instant Discord alerts.

## Attacks Detected
- Port Scan
- SYN Flood
- Brute Force
- ICMP Flood
- UDP Flood
- DNS Amplification
- Null Scan
- XMAS Scan

## Tech Stack
- Backend: Python, Scapy, Flask, Flask-SocketIO
- Database: MongoDB
- Frontend: React, Vite, Tailwind CSS
- Alerts: Discord Webhook

## Run Backend
cd backend
pip install scapy flask flask-socketio flask-cors pymongo requests
python app.py

## Run Frontend
cd frontend
npm install
npm run dev

## Dashboard
Open http://localhost:5173 to view the live threat dashboard.
