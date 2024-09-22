import datetime

from flask import Flask, request, redirect, flash, session
from flask import render_template
from flask import current_app as app

from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from .models import Users, Tasks
from .database import db

from helpers import apology, login_required

@app.route("/")
@login_required
def home():
    """Show users tasks"""
    user_id = session["user_id"]
    # Query the database for tasks related to this user
    user = Users.query.filter(Users.user_id == user_id).first()
    tasks = user.tasks
    
    print("User:", user_id)
    print(session["username"])

    print(tasks)

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
        # rows = db.execute("SELECT * FROM users WHERE username = ?", uname)
        user = Users(username=uname, email=email, hash=generate_password_hash(passwd))
        # Insert username, email, pass in db
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return apology("Username already exist", 400)
        # logging in the user
        print(user)
        user = Users.query.filter(Users.username == uname).one()
        session["user_id"] = user.user_id
        session["username"] = user.username
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        # rows = db.execute(
        #     "SELECT * FROM users WHERE username = ?", request.form.get("username")
        # )
        user = Users.query.filter(Users.username == username).one()
        if not user:
            return apology("invalid username", 403)
        # Ensure username exists and password is correct
        if not check_password_hash(user.hash, password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.user_id
        # print(rows)
        session["username"] = user.username

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/profile")
@login_required
def profile():
    """Profile customizations"""
    user_id = session["user_id"]
    # details = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    details = Users.query.filter_by(user_id = user_id).one()
    return render_template("profile.html", details=details)


@app.route("/logout")
def logout():
    """Log user out"""

    # Clear all cache
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/newTask", methods=["GET", "POST"])
@login_required
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

        # Convert due_date from 'YYYY-MM-DDTHH:MM' to python "datetime" object
        due_date = due.split('T')
        date = due_date[0].split("-")
        time = due_date[1].split(":") 
        due_date = datetime.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]), hour=int(time[0]), minute=int(time[1]))
        # print(due_date)
        # Get user id
        user_id = session["user_id"]

        user = Users.query.filter(Users.user_id==user_id).one()
        newtask = Tasks(task=taskname, task_description=taskdesc, due_date=due_date)
        user.tasks.append(newtask)
        try:
            db.session.commit()
        except:
            return apology("Sorry! Some error occurred")
        # Flash the message
        # db.session.commit()
        flash("Added a new task", category="primary")

        # Return to homepage
        return redirect("/")


@app.route("/update/<id>/<toUpd>", methods=["POST"])
@login_required
def update(id, toUpd):
    user = Users.query.filter_by(user_id=id).first()
    if toUpd == "email":
        email = request.form.get("email")
        # Update the user's email in the database
        user.email = email
        db.session.commit()
    if toUpd == "username":
        username = request.form.get("username")
        # Update the user's username in the database
        user2 = Users.query.filter_by(username=username).first()
        if user2:
            return apology("Username already exists.")
        else:
            user.username = username
            db.session.commit()
            session["username"] = username
    if toUpd == "password":
        oldPass = request.form.get("oldpass")
        newPass = request.form.get("newpass")
        cnfPass = request.form.get("cnfpass")
        hash = user.hash
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
                user.hash = new_hash
            else:
                flash(
                    "New password didn't matched with confirm password",
                    category="warning",
                )
        else:
            flash("Old password didn't match. Try again!", category="danger")

    return redirect("/")


@app.route("/edit_task/<int:task_id>", methods=["POST"])
@login_required
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
    # Convert due_date from 'YYYY-MM-DDTHH:MM' to python "datetime" object
    due_date = due.split('T')
    date = due_date[0].split("-")
    time = due_date[1].split(":") 
    due_date = datetime.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]), hour=int(time[0]), minute=int(time[1]))


    # Update the database
    task = Tasks.query.filter_by(task_id=task_id, user_id=session['user_id']).first()
    if task:
        task.task = taskname
        task.due_date = due_date
        task.task_description = taskdesc
        db.session.commit()
        flash(f"Updated task '{taskname}' successfully.", category="secondary")
        return redirect("/")
    else:
        return apology("Sorry! Some error occurred.")


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
