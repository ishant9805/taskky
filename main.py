import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_session import Session
app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
      
        app.config["SESSION_PERMANENT"] = False
        app.config["SESSION_TYPE"] = "filesystem"
    db.init_app(app)
    Session(app)
    app.app_context().push()
    return app

app = create_app()
@app.after_request
def after_request(response):
    """Ensure responses aren't cached
    This function is executed after every request is processed by the Flask app.
    It modifies the response headers to prevent the browser from caching the response.
    
    - Cache-Control: 'no-cache, no-store, must-revalidate' ensures that the browser will always 
      fetch a fresh copy of the page and not store it in cache.
    - Expires: '0' forces the browser to treat the page as expired, so it always fetches a new version.
    - Pragma: 'no-cache' is an older HTTP header for backward compatibility, 
      ensuring older browsers don't cache the page.
    
    This is useful for pages that need to reflect real-time data or should not be cached 
    for security reasons (e.g., user data or sensitive information).
    
    Returns the modified response.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
# Import all the controllers so they are loaded
from application.controllers import *

if __name__ == '__main__':
  # Create db
  db.create_all() 
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)
