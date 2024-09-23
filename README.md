# Taskky: A Task Management Web Application

#### Video Demo: https://youtu.be/asmK4zMQ50g
#### Live Website: ishant9805.pythonanywhere.com/
#### Description:
Taskky is a web application designed for users to manage their daily tasks effectively. Built with Flask, this application allows users to register, login, add tasks, edit them, and mark them as completed.

## Features:
- **User Authentication**: Secure registration and login functionality.
- **Task Management**: Users can add new tasks, edit existing ones, and delete them as needed.
- **Profile Management**: Users can update their profiles, including email and other personal details.

## File Structure:
- `application`: This directory contains the taskky application.
  - `__init__.py`: Empty file to register application as module
  - `config.py`: Contains config for local development
  - `controllers.py`: Handles routing
  - `database.py`: Connects to database
  - `helpers.py`: Contains utility functions that assist with various tasks throughout the application. Copied from finance project of CS50 week 9.
  - `models.py`: Contains database models(Users, Tasks)
- `db_directory/database.sqlite3`: This directory contains SQLite database file where user and task data are stored.
- `static/`: Directory for static files.
  - `main.js`: JavaScript file that contains front-end logic for interactive elements.
  - `styles.css`: CSS file for custom styling beyond what's provided by Bootstrap.
- `templates/`: Directory for Flask templates.
  - `layout.html`: Base template that includes common elements and structure.
  - `login.html`: Template for user login.
  - `register.html`: Template for user registration.
  - `profile.html`: Template for displaying and updating user profiles.
  - `home.html`: Main dashboard template for displaying tasks.
  - `apology.html`: Template for displaying error messages. Copied from finance project of CS50 week 9.
- `.gitignore`: To ignore unnecessary file for git tracking.
- `main.py`: The main file that runs the Flask application and sets config.
- `requirements.txt`: Python libraries that is required to run the app. 
- `schema.sql`: SQL schema that defines the structure of the database used by the application.

## How to Run:
1. Ensure Python is installed.
2. Install required python libraries by using command `pip install -r requirements.txt`.
3. Run the flask app with `python main.py` inside prject directory.

## Design Choices:
- **Flask**: Chosen for its simplicity and Pythonic conventions, making it ideal for small to medium web applications.
- **Flask-SQLAlchemy**: Used it for connecting flask app with database.
- **SQLite**: A lightweight database that doesn't require a separate server, perfect for development and smaller-scale applications.
- **Bootstrap**: An awesome css library which was easy to use and design the website.

## Conclusion:
Taskky is a simplistic yet powerful tool for managing daily tasks, showcasing the power of Flask and SQLite for web application development.

---

Taskky is developed by Ishant from India🇮🇳. For any inquiries or contributions, please contact ishant9805@gmail.com.
