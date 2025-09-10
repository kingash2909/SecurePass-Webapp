"""
WSGI entry point for SecurePass application.
This file is used by Gunicorn to serve the application.
"""

from app import app

if __name__ == "__main__":
    # For local development
    app.run()
else:
    # For production with Gunicorn
    application = app