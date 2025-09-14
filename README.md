# Smart Attendance System (SIH Demo)


This project is a **QR + Web-based Attendance System** designed as a demo for SIH 2025.  
It allows students to mark their attendance securely using their **phones** after scanning a QR code.  

- The backend is powered by **Flask**.  
- The frontend QR generator uses **Tkinter**.  
- Attendance is tracked in `Present.txt` and `Absent.txt`.  
- Remote access is enabled using **ngrok** (so it works beyond local Wi-Fi). You need an ngok account to continue with this

## ✨ Features
- Unique **QR code** generated every time the system is started.  
- Students scan the QR and mark attendance from their phone.  
- Attendance immediately reflects on the **teacher’s desktop UI**.  
- **Proxy prevention**: once a student marks attendance, their phone session is closed.  
- Works over the **internet** via ngrok tunnel.

main.py → orchestrates the system.

qr_front.py → generates QR code with ngrok public URL.

web_app.py → Flask web app for marking attendance.

SIH_test.py → Teacher’s attendance dashboard.

attendance_backend.py → Backend utility for attendance files.

## Workflow
- Teacher runs main.py.
- A QR code is displayed → Students scan with their phone.
- Student selects their roll no. → Attendance is marked.
- Teacher’s UI updates with present/absent status in real-time.
