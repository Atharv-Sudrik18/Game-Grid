from functools import wraps
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, session  # type: ignore
from db import get_db_connection


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# Guard: protects every admin route except the login page itself
def admin_login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.admin_login"))
        return f(*args, **kwargs)
    return wrapper


# Admin All Routes
# Admin Dashboard route
@admin_bp.route("/dashboard")
@admin_login_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM sign_up")
    total_users = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM admin_create_tournaments")
    total_tournaments = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM registrations")
    total_registrations = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM matches WHERE status = 'completed'")
    completed_matches = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM matches WHERE status != 'completed'")
    pending_results = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT team_name, registered_on
        FROM registrations
        ORDER BY registered_on DESC
        LIMIT 5
    """)
    recent_activities = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin/admin_dashboard.html",
        total_users=total_users,
        total_tournaments=total_tournaments,
        total_registrations=total_registrations,
        completed_matches=completed_matches,
        pending_results=pending_results,
        recent_activities=recent_activities,
    )


# Admin Profile
@admin_bp.route("/profile", methods=["GET", "POST"])
@admin_login_required
def admin_profile():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        new_password = request.form.get("new_password", "")

        # Check password confirmation
        if new_password and new_password != confirm_password:
            cursor.close()
            conn.close()
            return "Passwords do not match"

        # Get existing admin profile
        cursor.execute("SELECT * FROM admin_profile LIMIT 1")
        existing = cursor.fetchone()

        if existing:
            if not new_password:
                new_password = existing["new_password"]
                confirm_password = existing["confirm_password"]
            else:
                confirm_password = new_password

            cursor.execute("""
                UPDATE admin_profile
                SET fullname = %s,
                    username = %s,
                    email = %s,
                    mobile = %s,
                    new_password = %s,
                    confirm_password = %s
                LIMIT 1
            """, (
                fullname,
                username,
                email,
                mobile,
                new_password,
                confirm_password
            ))

        else:

            # Create profile if no record exists
            cursor.execute("""
                INSERT INTO admin_profile
                (fullname, username, email, mobile, new_password, confirm_password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                fullname,
                username,
                email,
                mobile,
                new_password,
                confirm_password
            ))

        conn.commit()

        # Update admin session
        session["admin_username"] = username

        cursor.close()
        conn.close()

        return redirect(url_for("admin.admin_profile"))

    # GET request
    cursor.execute("SELECT * FROM admin_profile LIMIT 1")
    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    # Default profile if table is empty
    if not admin:
        admin = {
            "fullname": "Administrator",
            "username": session.get("admin_username", "admin"),
            "email": "admin@gmail.com",
            "mobile": "9876543210",
            "new_password": "",
            "confirm_password": ""
        }

    return render_template("admin/admin_profile.html", admin=admin)


# Admin Manage Users route
@admin_bp.route("/manage_users")
@admin_login_required
def manage_users():
    search = request.args.get("search", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute("""
            SELECT fullname, username, email, mobile
            FROM sign_up
            WHERE fullname LIKE %s OR username LIKE %s OR email LIKE %s
            ORDER BY username
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT fullname, username, email, mobile FROM sign_up ORDER BY username")

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/manage_users.html", users=users, search=search)


# Admin Edit User route
@admin_bp.route("/edit_user/<username>", methods=["GET", "POST"])
@admin_login_required
def edit_user(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        mobile = request.form["mobile"]

        cursor.execute("""
            UPDATE sign_up SET fullname = %s, email = %s, mobile = %s
            WHERE username = %s
        """, (fullname, email, mobile, username))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for("admin.manage_users"))

    cursor.execute("SELECT fullname, username, email, mobile FROM sign_up WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return "User not found", 404

    return render_template("admin/edit_user.html", user=user)


# Admin Delete User route
@admin_bp.route("/delete_user/<username>")
@admin_login_required
def delete_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sign_up WHERE username = %s", (username,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("admin.manage_users"))


# Admin View Registrations route
@admin_bp.route("/registrations")
@admin_login_required
def view_registrations():
    search = request.args.get("search", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute("""
            SELECT r.*, t.tournament_name
            FROM registrations r
            JOIN admin_create_tournaments t ON r.tournament_id = t.id
            WHERE r.team_name LIKE %s OR r.captain_name LIKE %s OR r.username LIKE %s
            ORDER BY r.registered_on DESC
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("""
            SELECT r.*, t.tournament_name
            FROM registrations r
            JOIN admin_create_tournaments t ON r.tournament_id = t.id
            ORDER BY r.registered_on DESC
        """)

    registrations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/view_registrations.html", registrations=registrations, search=search)


# Admin Delete Registration route
@admin_bp.route("/delete_registration/<int:reg_id>")
@admin_login_required
def delete_registration(reg_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM registrations WHERE id = %s", (reg_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin.view_registrations'))


# Admin Manage Tournaments route
@admin_bp.route("/manage_tournaments")
@admin_login_required
def manage_tournaments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM admin_create_tournaments ORDER BY id DESC")
    tournaments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/manage_tournaments.html", tournaments=tournaments)


# Admin Create Tournament route
@admin_bp.route("/create_tournament", methods=["GET", "POST"])
@admin_login_required
def create_tournament():
    if request.method == 'POST':
        tournament_name = request.form['tournament_name']
        game = request.form['game']
        tournament_type = request.form['tournament_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        venue = request.form['venue']
        maximum_teams = request.form['maximum_teams']
        reg_last_date = request.form['reg_last_date']
        status = request.form['status']

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO admin_create_tournaments
        ( tournament_name, game, tournament_type,
        start_date, end_date, venue,
        maximum_teams, reg_last_date, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            tournament_name,
            game,
            tournament_type,
            start_date,
            end_date,
            venue,
            maximum_teams,
            reg_last_date,
            status
        )

        cursor.execute(sql, values)
        conn.commit()

        tournament_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return redirect(url_for('admin.add_matches', tournament_id=tournament_id))

    return render_template("admin/create_tournament.html")


# Admin Edit Tournament route
@admin_bp.route("/edit_tournament/<int:id>", methods=["GET", "POST"])
@admin_login_required
def edit_tournament(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        game = request.form["game"]
        type_ = request.form["type"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        venue = request.form["venue"]
        max_teams = request.form["max_teams"]
        last_date = request.form["last_date"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE admin_create_tournaments SET
            tournament_name = %s, game = %s, tournament_type = %s,
            start_date = %s, end_date = %s, venue = %s,
            maximum_teams = %s, reg_last_date = %s, status = %s
            WHERE id = %s
        """, (name, game, type_, start_date, end_date, venue, max_teams, last_date, status, id))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('admin.manage_tournaments'))

    cursor.execute("""
        SELECT id, tournament_name AS name, game, tournament_type AS type,
               start_date, end_date, venue,
               maximum_teams AS max_teams, reg_last_date AS last_date, status
        FROM admin_create_tournaments WHERE id = %s
    """, (id,))
    tournament = cursor.fetchone()

    cursor.close()
    conn.close()

    if not tournament:
        return "Tournament not found", 404

    return render_template("admin/edit_tournament.html", tournament=tournament)


# Admin Delete Tournament route
@admin_bp.route("/delete_tournament/<int:id>")
@admin_login_required
def delete_tournament(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clean up dependent rows first to respect the FK on registrations
    cursor.execute("DELETE FROM matches WHERE tournament_id = %s", (id,))
    cursor.execute("DELETE FROM registrations WHERE tournament_id = %s", (id,))
    cursor.execute("DELETE FROM admin_create_tournaments WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin.manage_tournaments'))


# Admin Add Matches route
@admin_bp.route("/add_matches/<int:tournament_id>", methods=["GET", "POST"])
@admin_login_required
def add_matches(tournament_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        match_no = request.form["match_no"]
        team_a = request.form["team_a"]
        team_b = request.form["team_b"]
        match_date = request.form["match_date"]
        match_time = request.form["match_time"]
        venue = request.form["venue"]
        round_ = request.form["round"]
        status = request.form["status"]

        sql = """
        INSERT INTO matches
        (tournament_id, match_no, team_a, team_b, match_date, match_time, venue, round, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (tournament_id, match_no, team_a, team_b, match_date, match_time, venue, round_, status)

        cursor.execute(sql, values)
        conn.commit()

    cursor.execute("SELECT * FROM admin_create_tournaments WHERE id = %s", (tournament_id,))
    tournament = cursor.fetchone()

    cursor.execute("SELECT * FROM matches WHERE tournament_id = %s ORDER BY match_no", (tournament_id,))
    matches = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/add_matches.html", tournament=tournament, matches=matches, tournament_id=tournament_id)


# Admin Edit Match route
@admin_bp.route("/edit_match/<int:match_id>", methods=["GET", "POST"])
@admin_login_required
def edit_match(match_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        match_no = request.form["match_no"]
        team_a = request.form["team_a"]
        team_b = request.form["team_b"]
        match_date = request.form["match_date"]
        match_time = request.form["match_time"]
        venue = request.form["venue"]
        round_ = request.form["round"]
        status = request.form["status"]

        sql = """
        UPDATE matches SET
        match_no = %s, team_a = %s, team_b = %s, match_date = %s,
        match_time = %s, venue = %s, round = %s, status = %s
        WHERE id = %s
        """
        cursor.execute(sql, (match_no, team_a, team_b, match_date, match_time, venue, round_, status, match_id))
        conn.commit()

        cursor.execute("SELECT tournament_id FROM matches WHERE id = %s", (match_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        return redirect(url_for('admin.add_matches', tournament_id=row['tournament_id']))

    cursor.execute("SELECT * FROM matches WHERE id = %s", (match_id,))
    match = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("admin/edit_match.html", match=match)


# Admin Delete Match route
@admin_bp.route("/delete_match/<int:match_id>")
@admin_login_required
def delete_match(match_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT tournament_id FROM matches WHERE id = %s", (match_id,))
    row = cursor.fetchone()

    cursor.execute("DELETE FROM matches WHERE id = %s", (match_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin.add_matches', tournament_id=row['tournament_id']))


# Admin Update Match Result route
@admin_bp.route("/update_result/<int:match_id>", methods=["GET", "POST"])
@admin_login_required
def update_result(match_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        winner = request.form["winner"]
        score_team_a = request.form["score_team_a"]
        score_team_b = request.form["score_team_b"]
        player_of_match = request.form["player_of_match"]
        remarks = request.form["remarks"]

        sql = """
        UPDATE matches SET
        winner = %s, score_team_a = %s, score_team_b = %s,
        player_of_match = %s, remarks = %s, status = 'completed'
        WHERE id = %s
        """
        cursor.execute(sql, (winner, score_team_a, score_team_b, player_of_match, remarks, match_id))
        conn.commit()

    cursor.execute("SELECT * FROM matches WHERE id = %s", (match_id,))
    match = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("admin/update_result.html", match=match)


# Admin Results route
@admin_bp.route("/manage_results", methods=["GET", "POST"])
@admin_login_required
def manage_results():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        tournament_id = request.form["tournament_id"]
        winner = request.form["winner"]
        runner_up = request.form["runner_up"]
        score = request.form["score"]
        result_date = request.form["result_date"]

        cursor.execute("SELECT tournament_name FROM admin_create_tournaments WHERE id = %s", (tournament_id,))
        row = cursor.fetchone()
        tournament_name = row["tournament_name"] if row else ""

        cursor.execute("""
            INSERT INTO admin_published_results (tournament, winner, runnerup, score, date)
            VALUES (%s, %s, %s, %s, %s)
        """, (tournament_name, winner, runner_up, score, result_date))
        conn.commit()

    cursor.execute("SELECT id, tournament_name AS name FROM admin_create_tournaments ORDER BY id DESC")
    tournaments = cursor.fetchall()

    cursor.execute("""
        SELECT id, tournament, winner, runnerup AS runner_up, score, date AS result_date
        FROM admin_published_results
        ORDER BY id DESC
    """)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/manage_results.html", tournaments=tournaments, results=results)


# Admin Notifications route
@admin_bp.route("/manage_notifications", methods=["GET", "POST"])
@admin_login_required
def manage_notifications():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        title = request.form["title"]
        message = request.form["message"]
        publish_date = request.form["publish_date"]

        sql = """
        INSERT INTO admin_published_notifications(title, publish_date, message)
        VALUES(%s, %s, %s)
        """

        cursor.execute(sql, (title, publish_date, message))
        conn.commit()

    # Always fetch notifications
    cursor.execute("""
        SELECT * FROM admin_published_notifications
        ORDER BY id DESC
    """)

    notifications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/manage_notifications.html", notifications=notifications)


# Admin Reports route
@admin_bp.route("/reports")
@admin_login_required
def reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS c FROM sign_up")
    total_users = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM admin_create_tournaments")
    total_tournaments = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM registrations")
    total_registrations = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM admin_published_results")
    total_results = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM admin_published_notifications")
    total_notifications = cursor.fetchone()["c"]

    cursor.close()
    conn.close()

    return render_template(
        "admin/reports.html",
        total_users=total_users,
        total_tournaments=total_tournaments,
        total_registrations=total_registrations,
        total_results=total_results,
        total_notifications=total_notifications,
        current_date=date.today().strftime("%Y-%m-%d"),
    )


# Admin Login route
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_profile LIMIT 1")
        admin_row = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin_row:
            # An admin profile exists in the database - check against it
            valid = (username == admin_row["username"] and password == admin_row["new_password"])
        else:
            # No profile saved yet (fresh database) - allow the one-time default login
            valid = (username == "admin" and password == "password")

        if valid:
            session["admin_logged_in"] = True
            session["admin_username"] = username
            return redirect(url_for("admin.admin_dashboard"))
        else:
            return render_template("admin/admin_login.html", error="Invalid username or password. Please try again.")

    return render_template("admin/admin_login.html")



# Admin Logout route
@admin_bp.route("/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    return redirect(url_for("admin.admin_login"))



