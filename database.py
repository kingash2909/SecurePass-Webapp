import sqlite3
import os
import json
from datetime import datetime

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'password_manager.db')

def init_db():
    """Initialize the database with required tables"""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create passwords table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            site_name TEXT NOT NULL,
            site_url TEXT,
            site_username TEXT NOT NULL,
            encrypted_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create reset_tokens table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expiry TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create recovery_keys table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recovery_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            key_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_passwords_user_id ON passwords (user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reset_tokens_token ON reset_tokens (token)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reset_tokens_user_id ON reset_tokens (user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_recovery_keys_user_id ON recovery_keys (user_id)')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get a database connection with row factory for dict-like access"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# User operations
def create_user(username, email, password_hash):
    """Create a new user"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone()
    finally:
        conn.close()

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return cursor.fetchone()
    finally:
        conn.close()

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def update_user_password(user_id, password_hash):
    """Update user's password hash"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET password_hash = ? WHERE id = ?',
            (password_hash, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

# Password operations
def add_password(user_id, site_name, site_url, site_username, encrypted_data):
    """Add a new password for a user"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO passwords (user_id, site_name, site_url, site_username, encrypted_data) VALUES (?, ?, ?, ?, ?)',
            (user_id, site_name, site_url, site_username, encrypted_data)
        )
        password_id = cursor.lastrowid
        conn.commit()
        return password_id
    finally:
        conn.close()

def get_passwords_by_user_id(user_id):
    """Get all passwords for a user"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM passwords WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        return cursor.fetchall()
    finally:
        conn.close()

def get_password_by_id(password_id):
    """Get a specific password by ID"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM passwords WHERE id = ?', (password_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def delete_password(password_id):
    """Delete a password by ID"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

# Reset token operations
def create_reset_token(user_id, token, expiry):
    """Create a new reset token"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reset_tokens (user_id, token, expiry) VALUES (?, ?, ?)',
            (user_id, token, expiry)
        )
        token_id = cursor.lastrowid
        conn.commit()
        return token_id
    finally:
        conn.close()

def get_reset_token(token):
    """Get reset token by token value"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT rt.*, u.username, u.email FROM reset_tokens rt JOIN users u ON rt.user_id = u.id WHERE rt.token = ?',
            (token,)
        )
        return cursor.fetchone()
    finally:
        conn.close()

def mark_token_as_used(token_id):
    """Mark a reset token as used"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE reset_tokens SET used = TRUE WHERE id = ?', (token_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def cleanup_expired_tokens():
    """Remove expired tokens"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reset_tokens WHERE expiry < datetime("now")')
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()

# Recovery key operations
def create_recovery_key(user_id, key_hash):
    """Create or update a recovery key for a user"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Try to update existing recovery key
        cursor.execute(
            'INSERT OR REPLACE INTO recovery_keys (user_id, key_hash) VALUES (?, ?)',
            (user_id, key_hash)
        )
        key_id = cursor.lastrowid
        conn.commit()
        return key_id
    finally:
        conn.close()

def get_recovery_key_by_user_id(user_id):
    """Get recovery key by user ID"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recovery_keys WHERE user_id = ?', (user_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def verify_recovery_key(user_id, key_hash):
    """Verify a recovery key for a user"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT 1 FROM recovery_keys WHERE user_id = ? AND key_hash = ?',
            (user_id, key_hash)
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()