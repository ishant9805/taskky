import datetime

from .database import db
from sqlalchemy.sql import func

class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    hash = db.Column(db.String, nullable=False)
    tasks = db.relationship("Tasks", backref='user', lazy=True)

class Tasks(db.Model):
    __tablename__ = "tasks"
    task_id =  db.Column(db.Integer, autoincrement=True, primary_key=True)
    task = db.Column(db.String, nullable=False)
    task_description = db.Column(db.String)
    completed = db.Column(db.Boolean, default=0)
    due_date = db.Column(db.DateTime)
    task_created = db.Column(db.DateTime, default=func.now())

    # Foreign key linking to Users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __str__(self) -> str:
        return f"[Task ID: {self.task_id}, Task: {self.task}, User: {self.user_id}" 

# class Userstask(db.Model):
#     __tablename__ = "userstask"
#     user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
#     task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"), primary_key=True)

