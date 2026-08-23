🏆 Game Grid — Sports Tournament Management System

Game Grid is a web-based platform for organizing, managing, and following sports tournaments. It provides a full Admin Panel to create and run tournaments, and a User Panel where players can browse tournaments, register their team, and track match results — plus an AI chat assistant for user support.

Built as a diploma industrial training project using Python (Flask) and MySQL.

✨ Features
Admin Panel
Secure admin login
Dashboard with live stats (total users, tournaments, registrations, completed matches, pending results)
Create, edit, and delete tournaments
Add, edit, and delete matches for each tournament (match no, teams, date, time, venue, round, status)
Update match results (winner, scores, player of the match, remarks)
View and manage all registered teams per tournament
Manage users (search, edit, delete)
Publish and manage notifications
Publish and manage tournament results
Reports overview
Admin profile management
User Panel
User signup, login, and forgot/reset password
Dashboard showing the user's own registered tournaments
Browse all tournaments and view match schedules
Register a team for a tournament (team name, captain name, captain mobile, player list)
View match results
View published notifications
AI Assistant chatbox (powered by Google Gemini) for quick help
User profile management
Public Pages
Home / About / Contact
Public tournaments listing (upcoming and completed)
🛠️ Tech Stack
Layer	Technology
Backend	Python, Flask (Blueprints)
Database	MySQL (mysql-connector-python)
Frontend	HTML, Jinja2 templates, CSS
AI Assistant	Google Gemini API (google-genai)
Config	python-dotenv for environment variables
📁 Project Structure
GAME_GRID_FINAL/
├── app.py                 # Flask app entry point, registers blueprints
├── main.py                # Public routes: home, login, signup, tournaments, password reset
├── admin.py                # Admin blueprint: dashboard, tournaments, matches, users, results
├── user.py                 # User blueprint: dashboard, registration, results, chatbox
├── db.py                   # MySQL connection helper
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment start command
├── Database/
│   └── *.sql                # Database schema/dump
├── static/
│   ├── css/                 # admin_style.css, user_style.css, style.css
│   └── images/               # logos, banners, media
└── templates/
    ├── admin/                # Admin panel pages
    ├── user/                 # User panel pages
    └── *.html                 # Public pages (index, login, signup, etc.)
⚙️ Setup & Installation
1. Clone / extract the project
bash
cd GAME_GRID_FINAL
2. Create a virtual environment (recommended)
bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
3. Install dependencies
bash
pip install flask mysql-connector-python python-dotenv google-genai

(Or use your project's requirements.txt if it only lists these core packages.)

4. Set up the database
Create a MySQL database (e.g. game_grid)
Import the schema from Database/game_grid-final.sql using phpMyAdmin or:
bash
mysql -u root -p game_grid < Database/game_grid-final.sql
Update db.py with your MySQL host, username, password, and database name.
5. Configure environment variables

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

Never commit .env to version control — add it to .gitignore.

6. Run the application
bash
python app.py

Visit http://127.0.0.1:5000 in your browser.

🔑 Default Admin Login

If no admin profile exists yet in the database, use the default:

Username: admin
Password: password

Update this immediately from the Admin Profile page after first login.

🗄️ Core Database Tables
Table	Purpose
sign_up	Registered users
admin_profile	Admin account details
admin_create_tournaments	Tournament records
matches	Match schedule and results per tournament
registrations	Team registrations per tournament
admin_published_notifications	Notifications shown to users
admin_published_results	Published tournament results
contact	Contact form submissions
📌 Notes
The Gemini API key must be kept secret — always load it via environment variables, never hardcode it in source files.
This project was built and tested locally with XAMPP/MySQL and Flask's development server; for production use, run behind a proper WSGI server (e.g. Gunicorn) and disable debug mode.
👤 Author

Developed by 
1.Atharv Sudrik
2.Aditya Kulkarni
3.Kiran Nimbalkar
as part of the Diploma Industrial Training Program (Computer Engineering).
