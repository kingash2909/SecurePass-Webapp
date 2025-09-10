// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Dashboard functionality
    const addPasswordBtn = document.getElementById('addPasswordBtn');
    const addPasswordModal = document.getElementById('addPasswordModal');
    const passwordDetailModal = document.getElementById('passwordDetailModal');
    const closeButtons = document.querySelectorAll('.close');
    const addPasswordForm = document.getElementById('addPasswordForm');
    const searchInput = document.getElementById('searchInput');
    const passwordCount = document.getElementById('passwordCount');
    
    // Recovery key functionality
    const generateRecoveryKeyBtn = document.getElementById('generateRecoveryKeyBtn');
    const recoveryKeyDisplay = document.getElementById('recoveryKeyDisplay');
    const recoveryKeyText = document.getElementById('recoveryKeyText');
    const copyRecoveryKeyBtn = document.getElementById('copyRecoveryKeyBtn');
    const downloadRecoveryKeyBtn = document.getElementById('downloadRecoveryKeyBtn');
    
    // Password strength elements
    const sitePasswordInput = document.getElementById('sitePassword');
    const strengthFill = document.getElementById('strengthFill');
    const strengthLabel = document.getElementById('strengthLabel');
    
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            createRipple(e, this);
        });
    });
    
    // Password visibility toggles for add password modal
    const toggleSitePassword = document.getElementById('toggleSitePassword');
    const toggleMasterPassword = document.getElementById('toggleMasterPassword');
    const masterPasswordInput = document.getElementById('masterPassword');
    
    if (toggleSitePassword && sitePasswordInput) {
        toggleSitePassword.addEventListener('click', function() {
            togglePasswordVisibility(sitePasswordInput, this);
        });
    }
    
    if (toggleMasterPassword && masterPasswordInput) {
        toggleMasterPassword.addEventListener('click', function() {
            togglePasswordVisibility(masterPasswordInput, this);
        });
    }
    
    // Password strength meter
    if (sitePasswordInput && strengthFill && strengthLabel) {
        sitePasswordInput.addEventListener('input', function() {
            updatePasswordStrength(this.value);
        });
    }
    
    // Open add password modal
    if (addPasswordBtn) {
        addPasswordBtn.addEventListener('click', function() {
            showLoading(false);
            addPasswordModal.style.display = 'block';
            // Add animation class
            const modalContent = addPasswordModal.querySelector('.modal-content');
            modalContent.style.animation = 'none';
            setTimeout(() => {
                modalContent.style.animation = 'slideInModal 0.3s ease-out';
            }, 10);
        });
    }
    
    // Close modals
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            modal.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                modal.style.display = 'none';
                modal.style.animation = '';
            }, 300);
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === addPasswordModal) {
            addPasswordModal.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                addPasswordModal.style.display = 'none';
                addPasswordModal.style.animation = '';
            }, 300);
        }
        if (event.target === passwordDetailModal) {
            passwordDetailModal.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                passwordDetailModal.style.display = 'none';
                passwordDetailModal.style.animation = '';
            }, 300);
        }
    });
    
    // Cancel add password
    const cancelAddBtn = document.getElementById('cancelAddBtn');
    if (cancelAddBtn) {
        cancelAddBtn.addEventListener('click', function() {
            addPasswordModal.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                addPasswordModal.style.display = 'none';
                addPasswordModal.style.animation = '';
                addPasswordForm.reset();
                // Reset password strength
                if (strengthFill && strengthLabel) {
                    strengthFill.style.width = '0%';
                    strengthFill.style.backgroundColor = '#333';
                    strengthLabel.textContent = 'Password Strength: None';
                }
            }, 300);
        });
    }
    
    // Generate password
    const generatePasswordBtn = document.getElementById('generatePasswordBtn');
    if (generatePasswordBtn) {
        generatePasswordBtn.addEventListener('click', function() {
            showLoading(true, 'Generating password...');
            fetch('/api/generate-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ length: 16 })
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                document.getElementById('sitePassword').value = data.password;
                updatePasswordStrength(data.password);
                // Add visual feedback
                generatePasswordBtn.textContent = 'Generated!';
                generatePasswordBtn.style.background = 'linear-gradient(135deg, #03dac6, #00b3a3)';
                setTimeout(() => {
                    generatePasswordBtn.textContent = 'Generate Secure Password';
                    generatePasswordBtn.style.background = '';
                }, 2000);
            })
            .catch(error => {
                showLoading(false);
                console.error('Error:', error);
                showAlert('Failed to generate password', 'error');
            });
        });
    }
    
    // Add password form submission
    if (addPasswordForm) {
        addPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                master_password: document.getElementById('masterPassword').value,
                site_name: document.getElementById('siteName').value,
                site_url: document.getElementById('siteUrl').value,
                site_username: document.getElementById('siteUsername').value,
                site_password: document.getElementById('sitePassword').value
            };
            
            // Validate form
            if (!formData.site_name || !formData.site_username || !formData.site_password || !formData.master_password) {
                showAlert('Please fill in all required fields', 'error');
                return;
            }
            
            showLoading(true, 'Adding password...');
            fetch('/api/passwords', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                if (data.message) {
                    addPasswordModal.style.animation = 'fadeOut 0.3s ease-out';
                    setTimeout(() => {
                        addPasswordModal.style.display = 'none';
                        addPasswordModal.style.animation = '';
                        addPasswordForm.reset();
                        // Reset password strength
                        if (strengthFill && strengthLabel) {
                            strengthFill.style.width = '0%';
                            strengthFill.style.backgroundColor = '#333';
                            strengthLabel.textContent = 'Password Strength: None';
                        }
                        loadPasswords();
                        showAlert('Password added successfully!', 'success');
                    }, 300);
                } else {
                    showAlert('Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showLoading(false);
                console.error('Error:', error);
                showAlert('Failed to add password', 'error');
            });
        });
    }
    
    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const passwordEntries = document.querySelectorAll('.password-entry');
            
            passwordEntries.forEach(entry => {
                const text = entry.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    entry.style.display = 'block';
                    // Add animation
                    entry.style.opacity = '0';
                    entry.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        entry.style.transition = 'all 0.3s ease';
                        entry.style.opacity = '1';
                        entry.style.transform = 'translateY(0)';
                    }, 10);
                } else {
                    entry.style.display = 'none';
                }
            });
            
            // Update password count
            updatePasswordCount();
        });
    }
    
    // Load passwords on dashboard
    if (document.getElementById('passwordList')) {
        loadPasswords();
    }
    
    // Add theme toggle
    addThemeToggle();
    
    // Generate recovery key
    if (generateRecoveryKeyBtn) {
        generateRecoveryKeyBtn.addEventListener('click', function() {
            showLoading(true, 'Generating recovery key...');
            fetch('/generate_recovery_key', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                if (data.recovery_key) {
                    recoveryKeyText.textContent = data.recovery_key;
                    recoveryKeyDisplay.style.display = 'block';
                    
                    // Scroll to recovery key display
                    recoveryKeyDisplay.scrollIntoView({ behavior: 'smooth' });
                    
                    // Add visual feedback
                    generateRecoveryKeyBtn.textContent = 'Generated!';
                    generateRecoveryKeyBtn.style.background = 'linear-gradient(135deg, #03dac6, #00b3a3)';
                    setTimeout(() => {
                        generateRecoveryKeyBtn.textContent = 'Generate Recovery Key';
                        generateRecoveryKeyBtn.style.background = '';
                    }, 2000);
                } else {
                    showAlert('Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showLoading(false);
                console.error('Error:', error);
                showAlert('Failed to generate recovery key', 'error');
            });
        });
    }
    
    // Copy recovery key
    if (copyRecoveryKeyBtn) {
        copyRecoveryKeyBtn.addEventListener('click', function() {
            const text = recoveryKeyText.textContent;
            navigator.clipboard.writeText(text).then(() => {
                const originalText = copyRecoveryKeyBtn.textContent;
                copyRecoveryKeyBtn.textContent = 'Copied!';
                copyRecoveryKeyBtn.style.background = 'linear-gradient(135deg, #03dac6, #00b3a3)';
                setTimeout(() => {
                    copyRecoveryKeyBtn.textContent = originalText;
                    copyRecoveryKeyBtn.style.background = '';
                }, 2000);
            });
        });
    }
    
    // Download recovery key
    if (downloadRecoveryKeyBtn) {
        downloadRecoveryKeyBtn.addEventListener('click', function() {
            const text = recoveryKeyText.textContent;
            const username = document.querySelector('.dashboard-title h2').textContent.replace('Welcome, ', '').replace('!', '');
            const filename = `securepass-recovery-key-${username}.txt`;
            
            const element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
            element.setAttribute('download', filename);
            
            element.style.display = 'none';
            document.body.appendChild(element);
            
            element.click();
            
            document.body.removeChild(element);
            
            // Visual feedback
            const originalText = downloadRecoveryKeyBtn.textContent;
            downloadRecoveryKeyBtn.textContent = 'Downloaded!';
            downloadRecoveryKeyBtn.style.background = 'linear-gradient(135deg, #03dac6, #00b3a3)';
            setTimeout(() => {
                downloadRecoveryKeyBtn.textContent = originalText;
                downloadRecoveryKeyBtn.style.background = '';
            }, 2000);
        });
    }
    
    // Copy username in password detail modal
    const copyUsernameBtn = document.getElementById('copyUsernameBtn');
    if (copyUsernameBtn) {
        copyUsernameBtn.addEventListener('click', function() {
            const username = document.getElementById('detailUsername').textContent;
            navigator.clipboard.writeText(username).then(() => {
                const originalText = copyUsernameBtn.textContent;
                copyUsernameBtn.textContent = 'Copied!';
                copyUsernameBtn.style.background = 'linear-gradient(135deg, #03dac6, #00b3a3)';
                setTimeout(() => {
                    copyUsernameBtn.textContent = originalText;
                    copyUsernameBtn.style.background = '';
                }, 2000);
            });
        });
    }
    
    // Visit site link
    const visitSiteLink = document.getElementById('visitSiteLink');
    if (visitSiteLink) {
        // This will be updated when showing password details
    }
});

// Toggle password visibility function
function togglePasswordVisibility(inputElement, toggleButton) {
    const type = inputElement.getAttribute('type') === 'password' ? 'text' : 'password';
    inputElement.setAttribute('type', type);
    
    // Toggle eye icon
    const eyeIcon = toggleButton.querySelector('i');
    if (type === 'password') {
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    } else {
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    }
}

// Update password strength meter
function updatePasswordStrength(password) {
    const strengthFill = document.getElementById('strengthFill');
    const strengthLabel = document.getElementById('strengthLabel');
    
    if (!strengthFill || !strengthLabel) return;
    
    if (!password) {
        strengthFill.style.width = '0%';
        strengthFill.style.backgroundColor = '#333';
        strengthLabel.textContent = 'Password Strength: None';
        return;
    }
    
    // Calculate password strength
    let strength = 0;
    let strengthText = '';
    let color = '';
    
    // Length check
    if (password.length >= 8) strength += 25;
    if (password.length >= 12) strength += 15;
    
    // Character variety
    if (/[a-z]/.test(password)) strength += 15;
    if (/[A-Z]/.test(password)) strength += 15;
    if (/[0-9]/.test(password)) strength += 15;
    if (/[^A-Za-z0-9]/.test(password)) strength += 15;
    
    // Determine strength text and color
    if (strength < 40) {
        strengthText = 'Weak';
        color = '#cf6679';
    } else if (strength < 70) {
        strengthText = 'Medium';
        color = '#ffb74d';
    } else if (strength < 90) {
        strengthText = 'Strong';
        color = '#81c784';
    } else {
        strengthText = 'Very Strong';
        color = '#4caf50';
    }
    
    strengthFill.style.width = strength + '%';
    strengthFill.style.backgroundColor = color;
    strengthLabel.textContent = `Password Strength: ${strengthText}`;
}

// Load passwords from API
function loadPasswords() {
    showLoading(true, 'Loading passwords...');
    fetch('/api/passwords')
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        const passwordList = document.getElementById('passwordList');
        const emptyState = document.getElementById('emptyState');
        const passwordCount = document.getElementById('passwordCount');
        
        if (data.passwords && data.passwords.length > 0) {
            passwordList.innerHTML = '';
            emptyState.style.display = 'none';
            
            data.passwords.forEach(password => {
                const entry = document.createElement('div');
                entry.className = 'password-entry';
                entry.innerHTML = `
                    <h3><i class="fas fa-key"></i> ${password.site_name}</h3>
                    <p><i class="fas fa-user"></i> ${password.site_username}</p>
                    <p><i class="fas fa-link"></i> ${password.site_url || 'No URL provided'}</p>
                `;
                entry.addEventListener('click', () => showPasswordDetail(password));
                
                // Add entrance animation
                entry.style.opacity = '0';
                entry.style.transform = 'translateY(20px)';
                passwordList.appendChild(entry);
                
                // Trigger animation
                setTimeout(() => {
                    entry.style.transition = 'all 0.3s ease';
                    entry.style.opacity = '1';
                    entry.style.transform = 'translateY(0)';
                }, 10);
            });
        } else {
            passwordList.innerHTML = '';
            emptyState.style.display = 'block';
        }
        
        // Update password count
        updatePasswordCount();
    })
    .catch(error => {
        showLoading(false);
        console.error('Error:', error);
        showAlert('Failed to load passwords', 'error');
    });
}

// Update password count
function updatePasswordCount() {
    const passwordEntries = document.querySelectorAll('.password-entry');
    const passwordCount = document.getElementById('passwordCount');
    if (passwordCount) {
        passwordCount.textContent = passwordEntries.length;
    }
}

// Show password detail
function showPasswordDetail(password) {
    document.getElementById('detailSiteName').textContent = password.site_name;
    document.getElementById('detailSiteUrl').textContent = password.site_url || 'No URL provided';
    document.getElementById('detailUsername').textContent = password.site_username;
    document.getElementById('detailPassword').textContent = '••••••••';
    document.getElementById('detailPassword').dataset.passwordId = password.id;
    
    // Reset decrypt input
    document.getElementById('decryptMasterPassword').value = '';
    
    // Set up event listeners
    document.getElementById('showPasswordBtn').onclick = togglePasswordVisibilityDetail;
    document.getElementById('copyPasswordBtn').onclick = copyPassword;
    document.getElementById('deletePasswordBtn').onclick = () => deletePassword(password.id);
    
    // Update visit site link
    const visitSiteLink = document.getElementById('visitSiteLink');
    if (visitSiteLink) {
        if (password.site_url) {
            visitSiteLink.href = password.site_url;
            visitSiteLink.style.display = 'inline-block';
        } else {
            visitSiteLink.style.display = 'none';
        }
    }
    
    // Show modal with animation
    const modal = document.getElementById('passwordDetailModal');
    modal.style.display = 'block';
    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.animation = 'none';
    setTimeout(() => {
        modalContent.style.animation = 'slideInModal 0.3s ease-out';
    }, 10);
}

// Toggle password visibility in detail modal
function togglePasswordVisibilityDetail() {
    const passwordSpan = document.getElementById('detailPassword');
    const showBtn = document.getElementById('showPasswordBtn');
    const masterPassword = document.getElementById('decryptMasterPassword').value;
    const passwordId = passwordSpan.dataset.passwordId;
    
    if (!masterPassword) {
        showAlert('Please enter your master password to decrypt', 'error');
        return;
    }
    
    if (passwordSpan.textContent === '••••••••') {
        showLoading(true, 'Decrypting password...');
        // Decrypt the password
        fetch(`/api/passwords/${passwordId}/decrypt`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ master_password: masterPassword })
        })
        .then(response => response.json())
        .then(data => {
            showLoading(false);
            if (data.password) {
                passwordSpan.textContent = data.password;
                passwordSpan.dataset.plaintext = data.password;
                showBtn.textContent = 'Hide';
                showBtn.style.background = 'linear-gradient(135deg, #cf6679, #bb4455)';
            } else {
                showAlert('Error: ' + data.error, 'error');
            }
        })
        .catch(error => {
            showLoading(false);
            console.error('Error:', error);
            showAlert('Failed to decrypt password', 'error');
        });
    } else {
        passwordSpan.textContent = '••••••••';
        passwordSpan.dataset.plaintext = '';
        showBtn.textContent = 'Show';
        showBtn.style.background = '';
    }
}

// Copy password to clipboard
function copyPassword() {
    const passwordSpan = document.getElementById('detailPassword');
    let password = passwordSpan.dataset.plaintext;
    
    if (!password) {
        showAlert('Please decrypt the password first', 'error');
        return;
    }
    
    navigator.clipboard.writeText(password).then(() => {
        const copyBtn = document.getElementById('copyPasswordBtn');
        const originalText = copyBtn.textContent;
        const originalBg = copyBtn.style.background;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.background = 'linear-gradient(135deg, #03dac6, #00b3a3)';
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = originalBg;
        }, 2000);
    });
}

// Delete password
function deletePassword(passwordId) {
    if (confirm('Are you sure you want to delete this password?')) {
        // In a real implementation, you would make an API call to delete the password
        showAlert('Password deletion would be implemented here', 'info');
        document.getElementById('passwordDetailModal').style.display = 'none';
        loadPasswords();
    }
}

// Create ripple effect
function createRipple(event, element) {
    const circle = document.createElement("span");
    circle.classList.add("ripple");
    circle.style.width = circle.style.height = Math.max(element.offsetWidth, element.offsetHeight) + "px";
    
    const rect = element.getBoundingClientRect();
    const x = event.clientX - rect.left - circle.offsetWidth / 2;
    const y = event.clientY - rect.top - circle.offsetHeight / 2;
    
    circle.style.left = x + "px";
    circle.style.top = y + "px";
    
    element.appendChild(circle);
    
    setTimeout(() => {
        circle.remove();
    }, 600);
}

// Show alert message
function showAlert(message, type) {
    // Remove existing alerts
    const existingAlert = document.querySelector('.custom-alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} custom-alert`;
    alert.textContent = message;
    
    // Add to body to ensure it's not constrained by container
    document.body.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Show loading overlay
function showLoading(show, text) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    
    if (show && loadingOverlay) {
        if (text) {
            loadingText.textContent = text;
        }
        loadingOverlay.style.display = 'flex';
    } else if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
}

// Add theme toggle functionality
function addThemeToggle() {
    // This would be implemented for light/dark theme switching
    // For now, we'll just add a placeholder for future implementation
    console.log('Theme toggle functionality ready for implementation');
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N to add new password
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        document.getElementById('addPasswordBtn')?.click();
    }
    
    // Esc to close modals
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal[style*="block"]');
        openModals.forEach(modal => {
            modal.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                modal.style.display = 'none';
                modal.style.animation = '';
            }, 300);
        });
    }
    
    // Ctrl/Cmd + F to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        document.getElementById('searchInput')?.focus();
    }
});

// Add first password button
document.addEventListener('click', function(e) {
    if (e.target.id === 'addFirstPasswordBtn') {
        document.getElementById('addPasswordBtn').click();
    }
});

// Add CSS for ripple effect and fadeOut animation
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    @keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }
    
    .no-passwords {
        text-align: center;
        color: #aaa;
        font-style: italic;
        padding: 2rem;
        grid-column: 1 / -1;
    }
    
    .custom-alert {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 300px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
`;
document.head.appendChild(style);