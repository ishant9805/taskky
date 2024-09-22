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

