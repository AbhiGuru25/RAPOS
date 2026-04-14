// Keyboard Accessibility & Form Validation Utilities

// Keyboard Navigation Helper
class KeyboardAccessibility {
    static init() {
        // Allow Enter key to submit forms
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                    const button = form.querySelector('button[type="submit"], input[type="submit"]');
                    if (button) button.click();
                }
            });
        });

        // Allow Escape key to close modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && document.getElementById('modal')) {
                const modal = document.getElementById('modal');
                if (modal.classList.contains('active')) {
                    modal.classList.remove('active');
                }
            }
        });

        // Tab through form inputs
        document.querySelectorAll('input, select, textarea, button, a[href]').forEach((el, index) => {
            el.setAttribute('tabindex', index + 1);
        });
    }
}

// Form Validation Helper
class FormValidator {
    static validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    static validatePassword(password) {
        return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/.test(password);
    }

    static validateUsername(username) {
        return username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username);
    }

    static showFieldError(field, message) {
        field.style.borderColor = '#d32f2f';
        let errorEl = field.nextElementSibling;
        if (!errorEl || !errorEl.classList.contains('field-error')) {
            errorEl = document.createElement('div');
            errorEl.className = 'field-error';
            errorEl.style.color = '#d32f2f';
            errorEl.style.fontSize = '12px';
            errorEl.style.marginTop = '4px';
            field.parentNode.insertBefore(errorEl, field.nextSibling);
        }
        errorEl.textContent = message;
    }

    static clearFieldError(field) {
        field.style.borderColor = '';
        const errorEl = field.nextElementSibling;
        if (errorEl && errorEl.classList.contains('field-error')) {
            errorEl.remove();
        }
    }

    static validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        const name = field.name;

        if (!value && field.required) {
            this.showFieldError(field, `${name} is required`);
            return false;
        }

        if (type === 'email' && value && !this.validateEmail(value)) {
            this.showFieldError(field, 'Please enter a valid email');
            return false;
        }

        if (name === 'password' && value && !this.validatePassword(value)) {
            this.showFieldError(field, 'Password must be 8+ chars with uppercase, lowercase, number, and symbol');
            return false;
        }

        if (name === 'username' && value && !this.validateUsername(value)) {
            this.showFieldError(field, 'Username must be 3+ characters (letters, numbers, underscore only)');
            return false;
        }

        this.clearFieldError(field);
        return true;
    }

    static setupRealTimeValidation(form) {
        form.querySelectorAll('input, select, textarea').forEach(field => {
            field.addEventListener('blur', () => {
                this.validateField(field);
            });
            field.addEventListener('input', () => {
                if (field.style.borderColor) {
                    this.validateField(field);
                }
            });
        });
    }
}

// Real-time Password Strength Indicator
class PasswordStrength {
    static init() {
        document.querySelectorAll('input[name="password"], input[id="password"]').forEach(field => {
            field.addEventListener('input', () => {
                this.updateStrength(field);
            });
        });
    }

    static updateStrength(field) {
        const password = field.value;
        let strength = 0;
        let feedback = '';

        if (!password) {
            strength = 0;
            feedback = '';
        } else {
            if (password.length >= 8) strength++;
            if (/[a-z]/.test(password)) strength++;
            if (/[A-Z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[!@#$%^&*]/.test(password)) strength++;

            const levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
            feedback = levels[strength] || '';
        }

        let el = document.getElementById('passwordStrength');
        if (!el) {
            el = document.createElement('div');
            el.id = 'passwordStrength';
            el.style.fontSize = '12px';
            el.style.marginTop = '6px';
            el.style.fontWeight = '600';
            field.parentNode.insertBefore(el, field.nextSibling);
        }

        const colors = ['#d32f2f', '#ff9800', '#fbc02d', '#7cb342', '#43a047'];
        el.style.color = colors[strength - 1] || '#999';
        el.textContent = feedback;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    KeyboardAccessibility.init();
    PasswordStrength.init();
    document.querySelectorAll('form').forEach(form => {
        FormValidator.setupRealTimeValidation(form);
    });
});
