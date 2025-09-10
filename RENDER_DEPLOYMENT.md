# Render Deployment Guide for SecurePass

This guide provides detailed instructions for deploying SecurePass on Render, a cloud platform that simplifies web application hosting.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. An email account with SMTP access (Gmail, Outlook, etc.)

## Deployment Steps

### 1. Fork the Repository

1. Go to the SecurePass repository on GitHub
2. Click the "Fork" button in the top right corner
3. Choose your account as the destination for the fork

### 2. Configure Render

1. Sign up or log in to your Render account
2. Click "New" and select "Web Service"
3. Connect Render to your GitHub account
4. Select the forked SecurePass repository
5. Configure the following settings:
   - **Name**: Choose a name for your service (e.g., "securepass")
   - **Region**: Choose the region closest to your users
   - **Branch**: Select "main" or "master"
   - **Root Directory**: Leave empty (the app is in the root directory)
   - **Environment**: Select "Python 3"
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:8000 wsgi:application`

### 3. Configure Environment Variables

In the Render dashboard, add the following environment variables:

1. `SMTP_SERVER`: Your SMTP server address (e.g., smtp.gmail.com)
2. `SMTP_PORT`: Your SMTP server port (e.g., 587)
3. `SENDER_EMAIL`: The email address to send from
4. `SENDER_PASSWORD`: App password for the sender email (NOT your regular password)
5. `EMAIL_USE_TLS`: Whether to use TLS (True or False)
6. `SECRET_KEY`: (Optional) Flask secret key for sessions (Render will auto-generate one if not provided)

### 4. Configure Email

Follow the instructions in [EMAIL_CONFIGURATION.md](EMAIL_CONFIGURATION.md) to properly configure your email settings:

- For Gmail, you'll need to enable 2-Factor Authentication and generate an App Password
- For Outlook/Hotmail, generate an App Password in your Microsoft account settings
- For Yahoo, generate an App Password in your Yahoo account settings

### 5. Deploy the Application

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies using `requirements.txt`
   - Start the application using Gunicorn
3. Wait for the deployment to complete (this may take a few minutes)
4. Once deployed, Render will provide a URL for your application

## Monitoring and Management

### Health Checks

The application includes a health check endpoint at `/health` that returns:

```json
{
  "status": "healthy",
  "timestamp": "2023-01-01T12:00:00.000000",
  "service": "SecurePass Password Manager"
}
```

Render will automatically monitor this endpoint to ensure your application is running.

### Logs

You can view application logs directly in the Render dashboard:
1. Go to your service in the Render dashboard
2. Click on the "Logs" tab
3. View real-time logs or search through historical logs

### Scaling

Render automatically handles scaling for you. If you need more resources:
1. Go to your service in the Render dashboard
2. Click on "Settings"
3. Adjust the instance type and number of instances

## Custom Domain (Optional)

To use a custom domain:

1. Purchase a domain from a registrar (or use an existing one)
2. In the Render dashboard:
   - Go to your service
   - Click on "Settings"
   - Scroll to "Custom Domains"
   - Add your domain
3. Configure DNS records as instructed by Render:
   - Add an A record pointing to Render's IP address
   - Add a CNAME record for www (if needed)

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SMTP_SERVER` | SMTP server address | smtp.gmail.com |
| `SMTP_PORT` | SMTP server port | 587 |
| `SENDER_EMAIL` | Sender email address | noreply@yourdomain.com |
| `SENDER_PASSWORD` | App password for sender email | your-app-password |
| `EMAIL_USE_TLS` | Use TLS encryption | True |
| `SECRET_KEY` | Flask secret key (optional) | your-secret-key |

## Troubleshooting

### Common Issues

1. **Email Not Sending**:
   - Verify SMTP credentials
   - Check if you're using an App Password (not your regular password)
   - Ensure TLS settings are correct
   - Check email provider quotas

2. **Application Not Starting**:
   - Check logs for error messages
   - Verify all environment variables are set
   - Ensure requirements.txt includes all dependencies

3. **Database Issues**:
   - Check file permissions on the database file
   - Ensure sufficient disk space
   - Verify database file integrity

### Getting Help

If you encounter issues not covered in this guide:
1. Check the application logs in the Render dashboard
2. Review the documentation files in the repository
3. Open an issue on the GitHub repository

## Security Considerations

1. **Use HTTPS**: Render automatically provides HTTPS for your application
2. **Environment Variables**: Store secrets in Render's environment variables, not in code
3. **Regular Updates**: Keep your fork updated with the latest security patches
4. **Access Control**: Use Render's access controls to limit who can manage your service

## Conclusion

Your SecurePass application should now be successfully deployed on Render and accessible via the URL provided in your Render dashboard. The application is configured to automatically restart if it crashes and includes health monitoring to ensure it stays running.

For ongoing maintenance:
- Regularly update your fork with security patches
- Monitor logs for any unusual activity
- Keep your email credentials secure and rotate them periodically