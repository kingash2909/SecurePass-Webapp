# SecurePass Deployment Guide

This guide provides detailed instructions for deploying SecurePass in various environments, from local development to production systems.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Management](#database-management)
6. [Security Considerations](#security-considerations)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- Python 3.6 or higher
- pip (Python package manager)
- At least 50MB free disk space
- 1GB RAM minimum (2GB recommended for production)

### Required Python Packages
All required packages are listed in [requirements.txt](requirements.txt):
- Flask==2.0.3
- Werkzeug==2.0.3
- cryptography==3.4.8
- python-dotenv==0.19.0

## Local Development Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SecurePass-Webapp
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your email configuration (see [EMAIL_CONFIGURATION.md](EMAIL_CONFIGURATION.md) for details).

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Production Deployment

### Render Deployment (Recommended)

This application includes a `render.yaml` file for easy deployment on Render:

1. Fork this repository to your GitHub account
2. Sign up for a Render account at https://render.com
3. Create a new Web Service and connect it to your forked repository
4. Render will automatically detect the `render.yaml` file and configure the service
5. Add your environment variables in the Render dashboard:
   - SMTP_SERVER
   - SMTP_PORT
   - SENDER_EMAIL
   - SENDER_PASSWORD
   - EMAIL_USE_TLS

### Manual Production Deployment

#### 1. Server Setup
- Choose a Linux server (Ubuntu 20.04 LTS recommended)
- Ensure Python 3.6+ is installed
- Configure firewall to allow only necessary ports (typically 22, 80, 443)

#### 2. Application Installation
```bash
# Clone repository
git clone <repository-url>
cd SecurePass-Webapp

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production WSGI server
pip install gunicorn
```

#### 3. Environment Configuration
Create a `.env` file with production settings:
```bash
SMTP_SERVER=your.smtp.server
SMTP_PORT=587
SENDER_EMAIL=noreply@yourdomain.com
SENDER_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

#### 4. Database Security
- Ensure the database file (`data/password_manager.db`) has appropriate permissions
- Set up regular backups
- Consider moving the database to a more secure location

#### 5. Web Server Configuration
Use Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

#### 6. SSL Configuration
Use Let's Encrypt for free SSL certificates:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

#### 7. Process Management
Use systemd to manage the application:

Create `/etc/systemd/system/securepass.service`:
```ini
[Unit]
Description=SecurePass Password Manager
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/SecurePass-Webapp
ExecStart=/path/to/SecurePass-Webapp/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable securepass
sudo systemctl start securepass
```

## Environment Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| SMTP_SERVER | SMTP server address | smtp.gmail.com |
| SMTP_PORT | SMTP server port | 587 |
| SENDER_EMAIL | Sender email address | noreply@yourdomain.com |
| SENDER_PASSWORD | App password for sender email | your-app-password |
| EMAIL_USE_TLS | Use TLS encryption | True |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_ENV | Flask environment | production |
| SECRET_KEY | Flask secret key | Randomly generated |

## Database Management

### Database Location
The SQLite database is stored at `data/password_manager.db`.

### Backup Strategy
Regular backups are essential:
```bash
# Simple backup
cp data/password_manager.db backups/password_manager_$(date +%Y%m%d).db

# Automated backup script
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp data/password_manager.db "$BACKUP_DIR/password_manager_$DATE.db"
find $BACKUP_DIR -name "password_manager_*.db" -mtime +30 -delete
```

### Database Maintenance
Perform regular maintenance:
```bash
# Vacuum the database to optimize size
sqlite3 data/password_manager.db "VACUUM;"
```

### Migration to Other Databases
For high-traffic applications, consider migrating to PostgreSQL:
1. Install PostgreSQL adapter: `pip install psycopg2`
2. Update database connection code in [database.py](database.py)
3. Migrate existing data

## Security Considerations

### Application Security
- Always use HTTPS in production
- Keep all dependencies updated
- Implement rate limiting for API endpoints
- Validate and sanitize all user inputs
- Use secure session management

### Data Security
- All passwords are encrypted before storage
- Master passwords are hashed with PBKDF2
- Recovery keys are hashed with SHA-256
- Database files should have restricted permissions

### Network Security
- Use a firewall to restrict access
- Implement proper SSH security
- Use fail2ban for intrusion prevention
- Regularly update system packages

### Email Security
- Use app-specific passwords, not account passwords
- Enable two-factor authentication
- Monitor email sending quotas
- Implement SPF, DKIM, and DMARC records

## Monitoring and Maintenance

### Log Monitoring
Monitor application logs for:
- Failed login attempts
- Security events
- Error conditions
- Performance issues

### Performance Monitoring
- Monitor response times
- Track database performance
- Watch memory and CPU usage
- Set up alerts for anomalies

### Regular Maintenance Tasks
- Update dependencies monthly
- Rotate credentials quarterly
- Review security logs weekly
- Test backups monthly

### Automated Health Checks
Implement health checks:
```bash
#!/bin/bash
# Check if application is responding
curl -f http://localhost:8000/health || systemctl restart securepass
```

## Troubleshooting

### Common Issues

#### 1. Email Not Sending
- Check SMTP credentials
- Verify TLS settings
- Ensure firewall allows outbound connections
- Check email provider quotas

#### 2. Database Errors
- Check file permissions
- Ensure sufficient disk space
- Verify database file integrity
- Check for concurrent access issues

#### 3. Slow Performance
- Check database size and optimize
- Monitor system resources
- Review query performance
- Consider caching strategies

#### 4. Deployment Failures
- Check logs for error messages
- Verify environment variables
- Ensure dependencies are installed
- Check file permissions

### Log Locations
- Application logs: Console output or configured log files
- System logs: `/var/log/syslog` or `/var/log/messages`
- Web server logs: `/var/log/nginx/` (if using Nginx)

### Getting Help
For issues not covered in this guide:
1. Check the [README.md](README.md) for general information
2. Review [PRODUCTION.md](PRODUCTION.md) for security best practices
3. Open an issue on the GitHub repository
4. Contact the development team

## Conclusion

This deployment guide covers the essential steps for running SecurePass in production. Regular maintenance, monitoring, and security updates are crucial for maintaining a secure and reliable password management service.

Always test changes in a staging environment before applying them to production, and maintain regular backups of all critical data.