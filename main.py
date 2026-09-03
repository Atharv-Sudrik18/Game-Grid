from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash  # type: ignore[import]
from db import get_db_connection


main_bp = Blueprint("main", __name__)

# Main Routes
@main_bp.route("/")
def index():
    return render_template("index.html")

# About route
@main_bp.route("/about")
def about():
    return render_template("about.html")

# Contact form route
@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO contact(name, email, subject, message)
        VALUES (%s, %s, %s, %s)
        """
        values = (name, email, subject, message)

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        flash("Message sent successfully!", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html")


# Tournaments route
@main_bp.route("/tournaments")
def tournaments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Upcoming tournaments
    cursor.execute("""
        SELECT tournament_name, game, start_date, status
        FROM admin_create_tournaments
        WHERE LOWER(status) = 'upcoming'
        ORDER BY start_date ASC
    """)
    upcoming_tournaments = cursor.fetchall()

    # Completed tournaments
    cursor.execute("""
        SELECT 
            tournament_name,
            game,
            winner,
            YEAR(end_date) AS year
        FROM admin_create_tournaments
        WHERE LOWER(status) = 'completed'
        ORDER BY end_date DESC
    """)
    completed_tournaments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "tournaments.html",
        upcoming_tournaments=upcoming_tournaments,
        completed_tournaments=completed_tournaments
    )


# Login route
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM sign_up WHERE username=%s AND password=%s"
        values = (username, password)

        cursor.execute(sql, values)
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("user.user_dashboard"))
        else:
            return render_template(
                "login.html",
                error="Invalid username or password. Please try again."
            )

    return render_template("login.html")


# User Signup route
@main_bp.route("/user_signup", methods=["GET", "POST"])
def user_signup():
    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match"

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO sign_up(fullname, username, email, mobile, password, confirm_password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (fullname, username, email, mobile, password, confirm_password)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("main.login"))
    return render_template("user_signup.html")


# Forgot Password - Step 1: verify identity
@main_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM sign_up WHERE username = %s AND email = %s",
            (username, email)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["reset_username"] = username
            return redirect(url_for("main.reset_password"))
        else:
            return render_template(
                "forgot_password.html",
                error="No account found with that username and email."
            )

    return render_template("forgot_password.html")


# Forgot Password - Step 2: set new password
@main_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if "reset_username" not in session:
        return redirect(url_for("main.forgot_password"))

    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return render_template(
                "reset_password.html",
                error="Passwords do not match."
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE sign_up SET password = %s, confirm_password = %s WHERE username = %s",
            (new_password, confirm_password, session["reset_username"])
        )
        conn.commit()
        cursor.close()
        conn.close()

        session.pop("reset_username", None)
        return redirect(url_for("main.login"))

    return render_template("reset_password.html")
