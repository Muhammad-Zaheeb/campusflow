# 🎓 CampusFlow Backend

A production-ready backend for **CampusFlow**, a student productivity and task management application built with **FastAPI**, **PostgreSQL**, and **JWT Authentication**.

---

## 🚀 Features

* 🔐 User Registration & Login
* 🔑 JWT Authentication
* 🛡️ Protected API Routes
* 👤 User-specific Task Management
* ✅ Create, Update, Delete Tasks
* ✔ Mark Tasks as Completed
* 📅 Due Dates
* 🔥 Overdue Task Detection
* ⭐ Task Priority (High, Medium, Low)
* 🗄 PostgreSQL Database
* ⚡ SQLAlchemy ORM
* 🌐 RESTful API
* ☁️ Deployed on Render

---

## 🛠 Tech Stack

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL (Neon)
* JWT Authentication
* Passlib (Password Hashing)
* Uvicorn
* Git & GitHub
* Render

---

## 📁 Project Structure

```
app/
│
├── auth/
├── core/
├── database/
├── models/
├── routers/
├── schemas/
└── main.py
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn app.main:app --reload
```

---

## 🌍 API Documentation

Once running locally:

```
http://localhost:8000/docs
```

---

## 🌐 Live Backend

Deployed on Render.

---

## 🔮 Future Improvements

* Password Reset
* Email Verification via Production Email Service
* Docker Support
* API Rate Limiting
* Refresh Tokens
* Unit & Integration Tests

---

## 👨‍💻 Author

**Muhammad Zaheeb**

Built as a portfolio project to demonstrate full-stack development using FastAPI, PostgreSQL, JWT Authentication, and modern REST API design.
