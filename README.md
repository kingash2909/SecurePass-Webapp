# SecurePass Web App Password Manager

A secure and user-friendly web-based password manager built with Flask and Python.

## Features

- **Secure Storage**: Passwords are encrypted before being stored using AES-128 encryption
- **Master Password Protection**: Single master password to access all your passwords with PBKDF2 hashing
- **Password Generation**: Generate strong, secure passwords with one click
- **Search Functionality**: Quickly find passwords by site name, URL, or username
- **Modern UI**: Clean, intuitive interface that's easy to use with dark theme
- **Password Visibility Toggle**: Show/hide passwords with eye icon toggle
- **UI Consistency**: Uniform styling across all form elements
- **Responsive Design**: Works on desktop and mobile devices
- **Password Recovery**: Secure password recovery using recovery keys
- **Email Integration**: Password reset functionality via email
- **Favicon**: Custom favicon for browser tabs and bookmarks

## Security Features

- All passwords are encrypted using AES-128 encryption
- Master password hashing with PBKDF2 and 100,000 iterations
- Secure password generation using cryptographic random number generation
- No data is sent to external servers
- No tracking or analytics
- Secure recovery key generation
- Password reset via email with time-limited tokens

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the webapp directory:
   ```bash
   cd SecurePass-Webapp
   ```

3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

5. (Optional) Generate a higher quality favicon:
   ```bash
   python generate_favicon.py
   ```

6. Configure email settings:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your email configuration (see [EMAIL_CONFIGURATION.md](EMAIL_CONFIGURATION.md) for details)

## Running the Application

### Development Mode

1. Make sure your virtual environment is activated
2. Run the application:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://127.0.0.1:5000`

### Production Mode

For production deployment, it's recommended to use a WSGI server like Gunicorn:

1. Install Gunicorn (already included in requirements.txt):
   ```bash
   pip install -r requirements.txt
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 wsgi:application
   ```

Alternatively, you can use the built-in Render deployment configuration which automatically handles this.

## Usage

1. Register for an account with a username, email, and master password
2. Login with your credentials
3. Generate a recovery key and store it in a secure location
4. Add passwords manually or generate secure passwords
5. Access your passwords whenever needed

## Deployment Options

### Render Deployment (Recommended)

This application includes a `render.yaml` file for easy deployment on Render:

1. Fork this repository to your GitHub account
2. Sign up for a Render account at https://render.com
3. Create a new Web Service and connect it to your forked repository
4. Render will automatically detect the `render.yaml` file and configure the service
5. Add your environment variables in the Render dashboard:
   - `SMTP_SERVER`: Your SMTP server address
   - `SMTP_PORT`: Your SMTP server port
   - `SENDER_EMAIL`: The email address to send from
   - `SENDER_PASSWORD`: App password for the sender email
   - `EMAIL_USE_TLS`: Whether to use TLS (True or False)
   - `SECRET_KEY`: (Optional) Flask secret key for sessions

### Other Deployment Options

- **Heroku**: Create a Procfile with `web: gunicorn app:app`
- **DigitalOcean App Platform**: Connect your repository and configure environment variables
- **AWS Elastic Beanstalk**: Upload the application as a ZIP file with requirements.txt
- **Traditional Server**: Use a WSGI server like Gunicorn with Nginx as a reverse proxy

## Environment Variables

The application uses the following environment variables for email configuration:

- `SMTP_SERVER`: SMTP server address (e.g., smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (e.g., 587)
- `SENDER_EMAIL`: Email address to send from
- `SENDER_PASSWORD`: App password for the sender email
- `EMAIL_USE_TLS`: Whether to use TLS encryption (True or False)

See [EMAIL_CONFIGURATION.md](EMAIL_CONFIGURATION.md) for detailed instructions on configuring email.

## API Endpoints

- `GET /`: Home page
- `GET /register`: User registration page
- `POST /register`: Register a new user
- `GET /login`: Login page
- `POST /login`: Authenticate user
- `GET /dashboard`: Password dashboard
- `GET /api/passwords`: Get all passwords for the current user
- `POST /api/passwords`: Add a new password
- `POST /api/passwords/<id>/decrypt`: Decrypt a password
- `POST /api/generate-password`: Generate a secure password
- `POST /generate_recovery_key`: Generate a recovery key

## Security Best Practices

1. **Use HTTPS**: Always deploy with HTTPS in production
2. **Strong Passwords**: Encourage users to use strong master passwords
3. **Regular Updates**: Keep all dependencies up to date
4. **Environment Variables**: Store secrets in environment variables, not in code
5. **Input Validation**: Validate and sanitize all user inputs
6. **Rate Limiting**: Implement rate limiting to prevent brute force attacks
7. **Backup**: Regularly backup your database
8. **Monitoring**: Monitor logs for suspicious activity

## Database

The application uses SQLite for data storage. In production, you might want to consider:

1. Using a more robust database like PostgreSQL
2. Implementing proper database connection pooling
3. Setting up regular database backups
4. Securing database files with appropriate permissions

## Contributing

Feel free to fork this project and submit pull requests with improvements.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.