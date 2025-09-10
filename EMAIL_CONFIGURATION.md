# Email Configuration for SecurePass Password Manager

## Overview

This document explains how to configure email functionality for the SecurePass Password Manager in a production environment.

## Environment Variables

The application uses environment variables for email configuration. You can set these variables in your operating system or in a `.env` file.

### Required Environment Variables

1. **SMTP_SERVER** - SMTP server address (e.g., `smtp.gmail.com`)
2. **SMTP_PORT** - SMTP server port (e.g., `587` for TLS)
3. **SENDER_EMAIL** - Email address to send from
4. **SENDER_PASSWORD** - Password or app-specific password for the sender email
5. **EMAIL_USE_TLS** - Whether to use TLS encryption (`True` or `False`)

### Example Configuration

#### For Gmail
```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your-app@gmail.com
export SENDER_PASSWORD=your-app-password
export EMAIL_USE_TLS=True
```

#### For Outlook/Hotmail
```bash
export SMTP_SERVER=smtp-mail.outlook.com
export SMTP_PORT=587
export SENDER_EMAIL=your-app@outlook.com
export SENDER_PASSWORD=your-app-password
export EMAIL_USE_TLS=True
```

#### For Yahoo
```bash
export SMTP_SERVER=smtp.mail.yahoo.com
export SMTP_PORT=587
export SENDER_EMAIL=your-app@yahoo.com
export SENDER_PASSWORD=your-app-password
export EMAIL_USE_TLS=True
```

## Using a .env File

Create a `.env` file in the webapp directory with the following content:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=noreply@securepass.com
SENDER_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

Then load the environment variables before running the application:

```bash
# On Linux/macOS
source .env
python app.py

# On Windows
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587
set SENDER_EMAIL=noreply@securepass.com
set SENDER_PASSWORD=your-app-password
set EMAIL_USE_TLS=True
python app.py
```

## Email Provider Specific Instructions

### Gmail Configuration

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this app password as your SENDER_PASSWORD

### Outlook/Hotmail Configuration

1. Enable 2-Factor Authentication on your Microsoft account
2. Generate an App Password:
   - Go to Microsoft Account settings
   - Security → More security options → Create a new app password
   - Use this app password as your SENDER_PASSWORD

### Yahoo Configuration

1. Enable 2-Factor Authentication on your Yahoo account
2. Generate an App Password:
   - Go to Yahoo Account settings
   - Security → Account security → App passwords
   - Generate a new app password
   - Use this app password as your SENDER_PASSWORD

## Testing Email Configuration

You can test your email configuration by running the test_email.py script:

```bash
python test_email.py
```

This script will show you what the email would look like without actually sending it.

## Security Considerations

1. **Never hardcode credentials** in the source code
2. **Use app-specific passwords** instead of your main account password
3. **Store credentials securely** using environment variables or a secrets manager
4. **Use TLS encryption** whenever possible
5. **Regularly rotate credentials** for security

## Troubleshooting

### Common Issues

1. **Authentication Failed**: Check that you're using an app-specific password, not your main account password
2. **Connection Refused**: Verify SMTP server address and port
3. **TLS Error**: Try setting EMAIL_USE_TLS=False if your provider doesn't support TLS

### Error Messages

- **"Username and Password not accepted"**: Incorrect credentials or need to use app-specific password
- **"Connection timed out"**: Incorrect SMTP server or port
- **"STARTTLS failed"**: Try disabling TLS or check server configuration

## Customization

You can customize the email templates by modifying the `send_password_reset_email` function in `app.py`:

1. **Plain Text Version**: Modify the `text` variable
2. **HTML Version**: Modify the `html` variable
3. **Subject Line**: Modify the `message["Subject"]` line

## Database Integration

In a production environment, you would need to:

1. Store user email addresses in your database
2. Modify the `forgot_password` route to retrieve the user's email from the database
3. Replace the placeholder `user_email = f"{username}@example.com"` with actual email retrieval

Example modification:
```python
# Instead of this placeholder:
user_email = f"{username}@example.com"

# Use this in production:
user_email = get_user_email_from_database(username)
```

Where `get_user_email_from_database` is a function that retrieves the user's email from your database.