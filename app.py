import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Used some code from finance project

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///taskky.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def home():
    """Show users tasks"""
    user_id = session["user_id"]
    # Query the database for tasks related to this user
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", user_id)
    print("Tasks:", tasks)

    return render_template("home.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    session.clear()

    # Handling POST request
    if request.method == "POST":
        # Take inputs and handle
        uname = request.form.get("username")
        email = request.form.get("email")
        passwd = request.form.get("password")
        cnfpass = request.form.get("confirmation")
        if not uname and not email:
            return apology("provide username and email", 400)
        elif not passwd:
            return apology("provide password", 400)
        elif not cnfpass:
            return apology("provide confirmation password", 400)
        elif cnfpass != passwd:
            return apology("passwords don't match", 400)

        # Check database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", uname)
        if len(rows) != 0:
            return apology("Username already exist", 400)

        # Insert username, email, pass in db
        db.execute(
            "INSERT INTO users (username, email, hash) VALUES(?, ?, ?)",
            uname,
            email,
            generate_password_hash(passwd),
        )

        rows = db.execute("SELECT * FROM users WHERE username = ?", uname)
        # logging in the user
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        print(rows)
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/profile")
@login_required
def profile():
    """Profile customizations"""
    user_id = session["user_id"]
    details = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    return render_template("profile.html", details=details)


@app.route("/logout")
def logout():
    """Log user out"""

    # Clear all cache
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/newTask", methods=["GET", "POST"])
def newTask():
    if request.method == "POST":
        taskname = request.form.get("taskname")
        taskdesc = request.form.get("taskdesc")
        due = request.form.get("due")

        if not taskname:
            flash(f"You must provide task.", category="warning")
            return redirect("/")
        if not taskdesc:
            flash(f"You must provide task description.", category="warning")
            return redirect("/")
        if not due:
            flash(f"You must provide task due date.", category="warning")
            return redirect("/")

        # Convert due_date from 'YYYY-MM-DDTHH:MM' to 'YYYY-MM-DD HH:MM:SS'
        due_date = due.replace("T", " ") + ":00"

        # Get user id
        user_id = session["user_id"]

        # Insert data into database
        db.execute(
            "INSERT INTO tasks (user_id, task, task_description, due_date) VALUES (?, ?, ?, ?)",
            user_id,
            taskname,
            taskdesc,
            due_date,
        )

        # Flash the message
        flash("Added a new task", category="primary")

        # Return to homepage
        return redirect("/")


@app.route("/update/<id>/<toUpd>", methods=["POST"])
def update(id, toUpd):
    if toUpd == "email":
        email = request.form.get("email")
        # Update the user's email in the database
        db.execute("UPDATE users SET email = ? WHERE id = ?", email, id)
    if toUpd == "username":
        username = request.form.get("username")
        # Update the user's username in the database
        db.execute("UPDATE users SET username = ? WHERE id = ?", username, id)
        session["username"] = username
    if toUpd == "password":
        oldPass = request.form.get("oldpass")
        newPass = request.form.get("newpass")
        cnfPass = request.form.get("cnfpass")
        hash = db.execute("SELECT * FROM users WHERE id = ?", id)[0]["hash"]
        if not oldPass:
            flash("Provide Old password", "warning")
        if not newPass:
            flash("Provide New password", "warning")
        if not cnfPass:
            flash("Confirm New password", "warning")
        if check_password_hash(hash, oldPass):
            if cnfPass == newPass:
                new_hash = generate_password_hash(cnfPass)
                # Update the user's password in the database
                db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, id)
            else:
                flash(
                    "New password didn't matched with confirm password",
                    category="warning",
                )
        else:
            flash("Old password didn't match. Try again!", category="danger")

    return redirect("/")


@app.route("/edit_task/<int:task_id>", methods=["POST"])
def editTask(task_id):
    taskname = request.form.get("taskname")
    taskdesc = request.form.get("taskdesc")
    due = request.form.get("due")

    if not taskname:
        flash(f"You must provide task.", category="warning")
        return redirect("/")
    if not taskdesc:
        flash(f"You must provide task description.", category="warning")
        return redirect("/")
    if not due:
        flash(f"You must provide task due date.", category="warning")
        return redirect("/")
    # Convert due_date from 'YYYY-MM-DDTHH:MM' to 'YYYY-MM-DD HH:MM:SS'
    due_date = due.replace("T", " ") + ":00"

    # Update the database
    db.execute(
        "UPDATE tasks SET task = ?, task_description = ?, due_date = ? WHERE id = ?",
        taskname,
        taskdesc,
        due_date,
        task_id,
    )
    flash(f"Updated task '{taskname}' successfully.", category="secondary")
    return redirect("/")


@app.route("/delete_task/<int:task_id>", methods=["POST"])
def deleteTask(task_id):
    rows = db.execute("SELECT * FROM tasks WHERE id = ?", task_id)
    taskname = rows[0]["task"]
    db.execute("DELETE FROM tasks WHERE id = ?", task_id)
    flash(f"Deleted task '{taskname}' successfully.", category="danger")
    return redirect("/")


@app.route("/done/<int:status>/<int:task_id>", methods=["POST"])
def done(status, task_id):
    if status == 0:
        rows = db.execute("SELECT * FROM tasks WHERE id = ?", task_id)
        taskname = rows[0]["task"]
        db.execute("UPDATE tasks SET completed = ? WHERE id = ?", 1, task_id)
        flash(f"Congratulations🎉! on completing task {taskname}.", category="success")
    else:
        rows = db.execute("SELECT * FROM tasks WHERE id = ?", task_id)
        taskname = rows[0]["task"]
        db.execute("UPDATE tasks SET completed = ? WHERE id = ?", 0, task_id)
        flash(f"You marked the task {taskname} as incompleted.", category="warning")
    return redirect("/")
