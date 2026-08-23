# Game Grid — Sports Tournament Management System

A web app to manage sports tournaments — built with Python (Flask) and MySQL.

Admins can create tournaments, schedule matches, and update results.
Users can browse tournaments, register their team, and check results.

## Features

- Admin: create/edit/delete tournaments, manage matches and results, manage users, publish notifications
- User: register for tournaments, view matches and results, AI chat assistant
- Login/signup with password reset for both admin and user

## Tech Stack

Flask, MySQL, Jinja2, HTML/CSS, Google Gemini API

## Setup

1. Install dependencies
```
pip install flask mysql-connector-python python-dotenv google-genai
```

2. Import the database
```
mysql -u root -p game_grid < Database/game_grid-final.sql
```
Update your MySQL credentials in `db.py`.

3. Add a `.env` file in the project root
```
GEMINI_API_KEY=your_api_key_here
```

4. Run the app
```
python app.py
```
Open http://127.0.0.1:5000

## Default Admin Login

```
Username: admin
Password: password
```
Change this from the Admin Profile page after first login.

## Author

1.Atharv Sudrik
2.Aditya Kulkarni
3.Kiran Nimbalkar

— Diploma Industrial Training Project (Computer Engineering)
