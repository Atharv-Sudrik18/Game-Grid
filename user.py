from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify  # type: ignore[import]
from db import get_db_connection
from google import genai
from datetime import date
from dotenv import load_dotenv  # type: ignore[import]
import os


user_bp = Blueprint("user", __name__, url_prefix="/user")
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


# User All Routes
# User Dashboard route
@user_bp.route("/dashboard")
def user_dashboard():
    if "username" not in session:
        return redirect(url_for("main.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.id, r.team_name, r.captain_name, r.registered_on, t.tournament_name, t.game, t.start_date, t.venue
        FROM registrations r
        JOIN admin_create_tournaments t ON r.tournament_id = t.id
        WHERE r.username = %s
        ORDER BY r.registered_on DESC
    """, (session["username"],))

    my_registrations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("user/user_dashboard.html", my_registrations=my_registrations)



# User Profile route
@user_bp.route("/profile")
def user_profile():

    if "username" not in session:
        return redirect(url_for("main.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT fullname, username, email, mobile
        FROM sign_up
        WHERE username=%s
    """, (session["username"],))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("user/user_profile.html",user=user)


# User Update Profile route
@user_bp.route("/update_profile", methods=["POST"])
def update_profile():

    if "username" not in session:
        return redirect(url_for("main.login"))

    fullname = request.form["fullname"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    if password.strip() == "":
        cursor.execute("""
            UPDATE sign_up
            SET fullname=%s,
                email=%s,
                mobile=%s
            WHERE username=%s
        """, (fullname, email, mobile, session["username"]))

    else:
        cursor.execute("""
            UPDATE sign_up
            SET fullname=%s,
                email=%s,
                mobile=%s,
                password=%s,
                confirm_password=%s
            WHERE username=%s
        """, (fullname, email, mobile, password, password, session["username"]))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Profile updated successfully!", "success")

    return redirect(url_for("user.user_profile"))

# User Tournaments route
@user_bp.route("/tournaments")
def user_tournaments():
    tournaments = []

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin_create_tournaments")
    tournaments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("user/user_tournaments.html",tournaments=tournaments)


# User View Matches for a Tournament route
@user_bp.route("/tournaments/<int:tournament_id>/matches")
def user_view_matches(tournament_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM admin_create_tournaments WHERE id = %s", (tournament_id,))
    tournament = cursor.fetchone()

    cursor.execute("SELECT * FROM matches WHERE tournament_id = %s ORDER BY match_no", (tournament_id,))
    matches = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("user/user_matches.html", tournament=tournament, matches=matches)

# User Registration route
@user_bp.route("/registration", methods=["GET", "POST"])
def user_registration():
    if request.method == "POST" and "username" not in session:
        return redirect(url_for("main.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        tournament_id = request.form["tournament_id"]
        team_name = request.form["team_name"]
        captain_name = request.form["captain_name"]
        captain_mobile = request.form["captain_mobile"]
        player_names = request.form.getlist("player_names[]")
        player_names = [p for p in player_names if p.strip()]

        error = None

        if len(player_names) > 15:
            error = "You can add a maximum of 15 players."

        if not error:
            cursor.execute("SELECT * FROM admin_create_tournaments WHERE id = %s", (tournament_id,))
            tournament = cursor.fetchone()

            if not tournament:
                error = "Selected tournament could not be found."
            elif tournament["reg_last_date"] and tournament["reg_last_date"] < date.today():
                error = "Registration for this tournament has closed."
            else:
                cursor.execute(
                    "SELECT COUNT(*) AS c FROM registrations WHERE tournament_id = %s",
                    (tournament_id,)
                )
                current_count = cursor.fetchone()["c"]

                if tournament["maximum_teams"] and current_count >= tournament["maximum_teams"]:
                    error = "This tournament has reached its maximum number of teams."
                else:
                    cursor.execute(
                        "SELECT id FROM registrations WHERE tournament_id = %s AND username = %s",
                        (tournament_id, session.get("username"))
                    )
                    if cursor.fetchone():
                        error = "You have already registered for this tournament."

        if error:
            cursor.execute("SELECT * FROM admin_create_tournaments ORDER BY start_date")
            tournaments = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template("user/user_registration.html", tournaments=tournaments,
                                    error=error)

        player_names_str = ", ".join(player_names)

        sql = """
        INSERT INTO registrations
        (tournament_id, username, team_name, captain_name, captain_mobile, player_names)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            tournament_id,
            session.get("username"),
            team_name,
            captain_name,
            captain_mobile,
            player_names_str
        ))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Registration successful.", "success")
        return redirect(url_for("user.user_dashboard"))

    cursor.execute("SELECT * FROM admin_create_tournaments ORDER BY start_date")
    tournaments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("user/user_registration.html", tournaments=tournaments)


# User Edit Registration route
@user_bp.route("/registration/edit/<int:reg_id>", methods=["GET", "POST"])
def edit_registration(reg_id):
    if "username" not in session:
        return redirect(url_for("main.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.*, t.tournament_name
        FROM registrations r
        JOIN admin_create_tournaments t ON r.tournament_id = t.id
        WHERE r.id = %s
    """, (reg_id,))
    registration = cursor.fetchone()

    if not registration or registration["username"] != session["username"]:
        cursor.close()
        conn.close()
        return "You are not allowed to edit this registration", 403

    if request.method == "POST":
        team_name = request.form["team_name"]
        captain_name = request.form["captain_name"]
        captain_mobile = request.form["captain_mobile"]
        player_names = request.form.getlist("player_names[]")
        player_names = [p for p in player_names if p.strip()]

        if len(player_names) > 15:
            cursor.close()
            conn.close()
            player_list = [p.strip() for p in registration["player_names"].split(",") if p.strip()]
            return render_template("user/edit_registration.html", registration=registration,
                                    player_list=player_list, error="You can add a maximum of 15 players.")

        player_names_str = ", ".join(player_names)

        cursor.execute("""
            UPDATE registrations SET
            team_name = %s, captain_name = %s, captain_mobile = %s, player_names = %s
            WHERE id = %s
        """, (team_name, captain_name, captain_mobile, player_names_str, reg_id))
        conn.commit()

        cursor.close()
        conn.close()
        flash("Registration updated successfully.", "success")
        return redirect(url_for("user.user_dashboard"))

    cursor.close()
    conn.close()

    player_list = [p.strip() for p in registration["player_names"].split(",") if p.strip()]

    return render_template("user/edit_registration.html", registration=registration, player_list=player_list)


# User Delete Registration route
@user_bp.route("/registration/delete/<int:reg_id>")
def delete_registration(reg_id):
    if "username" not in session:
        return redirect(url_for("main.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT username FROM registrations WHERE id = %s", (reg_id,))
    registration = cursor.fetchone()

    if not registration or registration["username"] != session["username"]:
        cursor.close()
        conn.close()
        return "You are not allowed to delete this registration", 403

    cursor.execute("DELETE FROM registrations WHERE id = %s", (reg_id,))
    conn.commit()

    cursor.close()
    conn.close()
    flash("Registration cancelled.", "delete")
    return redirect(url_for("user.user_dashboard"))


# User Results route
@user_bp.route("/results")
def user_results():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.*, t.tournament_name
        FROM matches m
        JOIN admin_create_tournaments t ON m.tournament_id = t.id
        WHERE m.status = 'completed'
        ORDER BY m.match_date DESC
    """)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("user/user_results.html", results=results)


# User Notifications route
@user_bp.route("/notifications")
def user_notifications():
    notifications = []

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM admin_published_notifications
        WHERE publish_date <= CURDATE()
        ORDER BY publish_date DESC, id DESC
    """)
    notifications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("user/user_notifications.html", notifications=notifications)


# User Logout Confirmation route
@user_bp.route("/logout_page")
def logout_page():
    return render_template("user/user_logout.html")


# Logout route
@user_bp.route("/logout")
def user_logout():
    session.clear()      # Remove all session data
    return redirect(url_for("main.login"))


@user_bp.route("/chatbox")
def chatbox():
    if "username" not in session:
        return redirect(url_for("main.login"))

    return render_template("user/chatbox.html")


@user_bp.route("/chat", methods=["POST"])
def chat():
    
    if "username" not in session:
        return jsonify({"reply": "Please login first."}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({"reply": "No data received."})

        message = data.get("message")
        if not message:
            return jsonify({"reply": "Message cannot be empty."})

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({
            "reply": f"Error: {str(e)}"
        })