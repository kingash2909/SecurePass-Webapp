"""
Python encryption helper for SecurePass Password Manager
This script provides additional encryption functionality that can be used alongside the Chrome extension.
"""

import hashlib
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordEncryption:
    def __init__(self):
        pass
    
    def generate_salt(self):
        """Generate a random salt for key derivation"""
        return secrets.token_bytes(16)
    
    def derive_key(self, master_password, salt):
        """Derive a key from the master password and salt using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key
    
    def encrypt_password(self, password, master_password):
        """Encrypt a password using the master password"""
        salt = self.generate_salt()
        key = self.derive_key(master_password, salt)
        f = Fernet(key)
        encrypted_password = f.encrypt(password.encode())
        
        # Return salt and encrypted password as base64 strings
        return {
            'salt': base64.b64encode(salt).decode(),
            'encrypted_password': base64.b64encode(encrypted_password).decode()
        }
    
    def decrypt_password(self, encrypted_data, master_password):
        """Decrypt a password using the master password"""
        salt = base64.b64decode(encrypted_data['salt'])
        encrypted_password = base64.b64decode(encrypted_data['encrypted_password'])
        
        key = self.derive_key(master_password, salt)
        f = Fernet(key)
        
        try:
            decrypted_password = f.decrypt(encrypted_password)
            return decrypted_password.decode()
        except Exception as e:
            raise ValueError("Decryption failed. Invalid master password or corrupted data.")
    
    def hash_master_password(self, master_password):
        """Hash the master password for verification"""
        salt = self.generate_salt()
        key = self.derive_key(master_password, salt)
        
        # Return salt and key as a single string separated by a delimiter
        return base64.b64encode(salt).decode() + ":" + base64.b64encode(key).decode()
    
    def verify_master_password(self, master_password, stored_hash):
        """Verify a master password against stored hash"""
        # Split the stored hash to get salt and hash
        salt_str, hash_str = stored_hash.split(":")
        salt = base64.b64decode(salt_str)
        key = self.derive_key(master_password, salt)
        
        return base64.b64encode(key).decode() == hash_str

# Example usage
if __name__ == "__main__":
    # Example of how to use the encryption helper
    encryptor = PasswordEncryption()
    
    # Example master password and password to encrypt
    master_password = "my_secure_master_password"
    password = "my_secret_password_123"
    
    # Encrypt the password
    encrypted = encryptor.encrypt_password(password, master_password)
    print("Encrypted password:", encrypted)
    
    # Decrypt the password
    decrypted = encryptor.decrypt_password(encrypted, master_password)
    print("Decrypted password:", decrypted)
    
    # Hash the master password
    master_hash = encryptor.hash_master_password(master_password)
    print("Master password hash:", master_hash)
    
    # Verify the master password
    is_valid = encryptor.verify_master_password(master_password, master_hash)
    print("Master password is valid:", is_valid)