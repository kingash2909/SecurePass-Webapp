import os
import json
import secrets
import hashlib
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
import sqlite3

# Load environment variables from .env file
load_dotenv()

# Import the encryption helper
from encryption_helper import PasswordEncryption

# Import database module
from database import init_db, get_user_by_username, get_user_by_email, create_user, update_user_password
from database import add_password, get_passwords_by_user_id, get_password_by_id, delete_password
from database import create_reset_token, get_reset_token, mark_token_as_used
from database import create_recovery_key, get_recovery_key_by_user_id, verify_recovery_key

# Initialize database
init_db()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for sessions

# Email configuration - Production ready settings
EMAIL_CONFIG = {
    'smtp_server': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.environ.get('SMTP_PORT', 587)),
    'sender_email': os.environ.get('SENDER_EMAIL', 'noreply@securepass.com'),
    'sender_password': os.environ.get('SENDER_PASSWORD', ''),
    'use_tls': os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
}

print(f"Email configuration loaded:")
print(f"  SMTP Server: {EMAIL_CONFIG['smtp_server']}")
print(f"  SMTP Port: {EMAIL_CONFIG['smtp_port']}")
print(f"  Sender Email: {EMAIL_CONFIG['sender_email']}")
print(f"  Use TLS: {EMAIL_CONFIG['use_tls']}")

# Initialize encryption helper
encryptor = PasswordEncryption()

def send_password_reset_email(username, recipient_email, reset_link):
    """
    Send password reset email to user
    
    Args:
        username (str): The username of the recipient
        recipient_email (str): The email address of the recipient
        reset_link (str): The password reset link to include in the email
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "SecurePass Password Reset"
        message["From"] = EMAIL_CONFIG['sender_email']
        message["To"] = recipient_email
        
        # Create the plain-text version
        text = f"""\
        Hi {username},
        
        You have requested to reset your password for your SecurePass account.
        
        Please click the link below to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you did not request this password reset, please ignore this email 
        and consider enabling two-factor authentication for additional security.
        
        Best regards,
        SecurePass Security Team"""
        
        # Create HTML version
        html = f"""\
        <!DOCTYPE html>
        <html>
        <head>
            <title>SecurePass Password Reset</title>
        </head>
        <body>
            <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                    <h1 style="color: white; margin: 0;">SecurePass</h1>
                </div>
                <div style="padding: 30px; background: #f9f9f9;">
                    <h2>Hello {username},</h2>
                    <p>You have requested to reset your password for your SecurePass account.</p>
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" 
                           style="background: #667eea; color: white; padding: 12px 24px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Reset Password
                        </a>
                    </p>
                    <p><small>This link will expire in 1 hour.</small></p>
                    <p>If you did not request this password reset, please ignore this email.</p>
                </div>
                <div style="padding: 20px; text-align: center; background: #f1f1f1; font-size: 12px;">
                    <p>© 2023 SecurePass Password Manager. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(part1)
        message.attach(part2)
        
        # Create secure connection and send email
        if EMAIL_CONFIG['use_tls']:
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.sendmail(EMAIL_CONFIG['sender_email'], recipient_email, message.as_string())
            server.quit()
        else:
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.sendmail(EMAIL_CONFIG['sender_email'], recipient_email, message.as_string())
            server.quit()
        
        print(f"Password reset email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {e}")
        return False

# Routes
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        master_password = request.form['master_password']
        confirm_password = request.form['confirm_password']
        
        # Validate email format
        if not email or '@' not in email:
            return render_template('register.html', error='Please enter a valid email address')
        
        # Check if username already exists
        if get_user_by_username(username):
            return render_template('register.html', error='Username already exists')
        
        # Check if email already exists
        if get_user_by_email(email):
            return render_template('register.html', error='Email address already registered')
        
        # Validate password length
        if len(master_password) < 8:
            return render_template('register.html', error='Password must be at least 8 characters')
        
        # Check if passwords match
        if master_password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        # Hash the master password
        master_hash = encryptor.hash_master_password(master_password)
        
        try:
            # Create user in database
            user_id = create_user(username, email, master_hash)
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            # Handle specific database constraint violations
            if "username" in str(e).lower():
                return render_template('register.html', error='Username already exists')
            elif "email" in str(e).lower():
                return render_template('register.html', error='Email address already registered')
            else:
                return render_template('register.html', error='Registration failed. Username or email may already exist.')
        except Exception as e:
            # Log the actual error for debugging (in production, you might want to log this to a file)
            print(f"Registration error: {str(e)}")
            return render_template('register.html', error='Registration failed. Please try again.')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        master_password = request.form['master_password']
        
        # Get user from database
        user = get_user_by_username(username)
        
        if not user:
            return render_template('login.html', error='Invalid username or password')
        
        # Verify master password
        try:
            is_valid = encryptor.verify_master_password(master_password, user['password_hash'])
            if is_valid:
                session['username'] = username
                session['user_id'] = user['id']
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid username or password')
        except Exception as e:
            return render_template('login.html', error='Login failed')
    
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        
        if not username:
            return render_template('forgot_password.html', error='Username is required')
        
        # Check if username exists
        user = get_user_by_username(username)
        
        if not user:
            # Security: Don't reveal if username exists
            return render_template('forgot_password.html', 
                                 message='If account exists, reset instructions sent to email')
        
        # Generate secure reset token (valid for 1 hour)
        token = secrets.token_urlsafe(32)
        expiry = datetime.now() + timedelta(hours=1)
        
        # Store token in database
        try:
            token_id = create_reset_token(user['id'], token, expiry)
        except Exception as e:
            return render_template('forgot_password.html', 
                                 error='Failed to process reset request. Please try again later.')
        
        # Generate reset link
        reset_link = url_for('reset_password', token=token, _external=True)
        
        # Send email
        email_sent = send_password_reset_email(username, user['email'], reset_link)
        
        if not email_sent:
            return render_template('forgot_password.html', 
                                 error='Failed to send reset email. Please try again later.')
        
        # In production, only show success message without token/link
        return render_template('forgot_password.html', 
                             message='If account exists, reset instructions sent to email')
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Get token from database
    token_data = get_reset_token(token)
    
    # Validate token
    if not token_data:
        return render_template('reset_password.html', error='Invalid or expired reset token')
    
    # Check if token is expired
    expiry = datetime.fromisoformat(token_data['expiry'])
    if datetime.now() > expiry:
        return render_template('reset_password.html', error='Reset token has expired')
    
    # Check if token has been used
    if token_data['used']:
        return render_template('reset_password.html', error='Reset token has already been used')
    
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not new_password or not confirm_password:
            return render_template('reset_password.html', 
                                 error='All fields are required',
                                 token=token)
        
        if len(new_password) < 8:
            return render_template('reset_password.html', 
                                 error='Password must be at least 8 characters long',
                                 token=token)
        
        if new_password != confirm_password:
            return render_template('reset_password.html', 
                                 error='Passwords do not match',
                                 token=token)
        
        # Hash the new master password
        master_hash = encryptor.hash_master_password(new_password)
        
        # Update user's password
        try:
            update_user_password(token_data['user_id'], master_hash)
            
            # Mark token as used
            mark_token_as_used(token_data['id'])
            
            return render_template('reset_password.html', 
                                 success='Password reset successfully.')
        except Exception as e:
            return render_template('reset_password.html', 
                                 error='Failed to reset password. Please try again.',
                                 token=token)
    
    return render_template('reset_password.html', token=token)

@app.route('/generate_recovery_key', methods=['POST'])
def generate_recovery_key():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get user from database
    user = get_user_by_username(session['username'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Generate a secure recovery key
    recovery_key = secrets.token_urlsafe(32)
    recovery_hash = hashlib.sha256(recovery_key.encode()).hexdigest()
    
    # Store the hash of the recovery key
    try:
        create_recovery_key(user['id'], recovery_hash)
        
        return jsonify({
            'recovery_key': recovery_key,
            'message': 'Save this recovery key in a secure location. It can only be viewed once.'
        })
    except Exception as e:
        return jsonify({'error': 'Failed to generate recovery key'}), 500

@app.route('/use_recovery_key', methods=['GET', 'POST'])
def use_recovery_key():
    if request.method == 'POST':
        username = request.form.get('username')
        recovery_key = request.form.get('recovery_key')
        
        if not username or not recovery_key:
            return render_template('use_recovery_key.html', error='Username and recovery key are required')
        
        # Get user from database
        user = get_user_by_username(username)
        if not user:
            return render_template('use_recovery_key.html', error='No account found for this username')
        
        # Verify recovery key
        recovery_hash = hashlib.sha256(recovery_key.encode()).hexdigest()
        if not verify_recovery_key(user['id'], recovery_hash):
            return render_template('use_recovery_key.html', error='Invalid recovery key')
        
        # Recovery key is valid, allow user to set new password
        session['recovery_authenticated'] = True
        session['recovery_username'] = username
        session['recovery_user_id'] = user['id']
        return redirect(url_for('recovery_reset_password'))
    
    return render_template('use_recovery_key.html')

@app.route('/recovery_reset_password', methods=['GET', 'POST'])
def recovery_reset_password():
    if not session.get('recovery_authenticated'):
        return redirect(url_for('login'))
    
    username = session.get('recovery_username')
    user_id = session.get('recovery_user_id')
    
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not new_password or not confirm_password:
            return render_template('recovery_reset_password.html', 
                                 error='All fields are required')
        
        if len(new_password) < 8:
            return render_template('recovery_reset_password.html', 
                                 error='Password must be at least 8 characters long')
        
        if new_password != confirm_password:
            return render_template('recovery_reset_password.html', 
                                 error='Passwords do not match')
        
        # Hash the new master password
        master_hash = encryptor.hash_master_password(new_password)
        
        # Update user's password
        try:
            update_user_password(user_id, master_hash)
            
            # Clear recovery session
            session.pop('recovery_authenticated', None)
            session.pop('recovery_username', None)
            session.pop('recovery_user_id', None)
            
            return render_template('recovery_reset_password.html', 
                                 success='Password reset successfully.')
        except Exception as e:
            return render_template('recovery_reset_password.html', 
                                 error='Failed to reset password. Please try again.')
    
    return render_template('recovery_reset_password.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

# API endpoints
@app.route('/api/passwords', methods=['GET'])
def get_passwords():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get user from database
    user = get_user_by_username(session['username'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get passwords from database
    user_passwords = get_passwords_by_user_id(user['id'])
    
    # Convert to list of dictionaries
    passwords_list = []
    for password in user_passwords:
        passwords_list.append({
            'id': password['id'],
            'site_name': password['site_name'],
            'site_url': password['site_url'],
            'site_username': password['site_username'],
            'created_at': password['created_at']
        })
    
    return jsonify({'passwords': passwords_list})

@app.route('/api/passwords', methods=['POST'])
def add_password_api():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    master_password = data.get('master_password')
    site_name = data.get('site_name')
    site_url = data.get('site_url')
    site_username = data.get('site_username')
    site_password = data.get('site_password')
    
    if not all([master_password, site_name, site_username, site_password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Get user from database
    user = get_user_by_username(session['username'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Verify master password
    try:
        is_valid = encryptor.verify_master_password(master_password, user['password_hash'])
        if not is_valid:
            return jsonify({'error': 'Invalid master password'}), 401
    except Exception as e:
        return jsonify({'error': 'Verification failed'}), 500
    
    # Encrypt the password
    try:
        encrypted_data = encryptor.encrypt_password(site_password, master_password)
        
        # Store the encrypted password in database
        password_id = add_password(user['id'], site_name, site_url, site_username, encrypted_data)
        
        return jsonify({'message': 'Password added successfully'})
    except Exception as e:
        return jsonify({'error': 'Encryption failed'}), 500

@app.route('/api/passwords/<int:password_id>/decrypt', methods=['POST'])
def decrypt_password(password_id):
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    master_password = data.get('master_password')
    
    if not master_password:
        return jsonify({'error': 'Master password required'}), 400
    
    # Get user from database
    user = get_user_by_username(session['username'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Verify master password
    try:
        is_valid = encryptor.verify_master_password(master_password, user['password_hash'])
        if not is_valid:
            return jsonify({'error': 'Invalid master password'}), 401
    except Exception as e:
        return jsonify({'error': 'Verification failed'}), 500
    
    # Get the password entry from database
    password_entry = get_password_by_id(password_id)
    
    if not password_entry:
        return jsonify({'error': 'Password not found'}), 404
    
    # Check if password belongs to the user
    if password_entry['user_id'] != user['id']:
        return jsonify({'error': 'Password not found'}), 404
    
    # Decrypt the password
    try:
        decrypted_password = encryptor.decrypt_password(password_entry['encrypted_data'], master_password)
        return jsonify({'password': decrypted_password})
    except Exception as e:
        return jsonify({'error': 'Decryption failed'}), 500

@app.route('/api/generate-password', methods=['POST'])
def generate_password():
    data = request.get_json()
    length = data.get('length', 16)
    
    # Generate a secure password
    generated_password = generate_secure_password(length)
    return jsonify({'password': generated_password})

def generate_secure_password(length):
    import secrets
    import string
    
    charset = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(charset) for _ in range(length))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
