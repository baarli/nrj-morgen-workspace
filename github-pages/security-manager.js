// Security Manager for Mission Control
// Provides security hardening with validation and protection

class SecurityManager {
    constructor() {
        this.rateLimits = new Map();
        this.suspiciousActivity = [];
        this.securityHeaders = {
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; img-src 'self' data: https:; connect-src 'self' https://*.supabase.co wss://*.supabase.co;",
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
        };
    }

    // Initialize security
    init() {
        console.log('🔒 Initializing Security Manager...');
        
        this.applySecurityHeaders();
        this.setupInputValidation();
        this.setupRateLimiting();
        this.setupXSSProtection();
        this.setupCSRFProtection();
        this.monitorSuspiciousActivity();
    }

    // Apply security headers
    applySecurityHeaders() {
        // In a real application, these would be set server-side
        // For client-side, we can add meta tags
        const meta = document.createElement('meta');
        meta.httpEquiv = 'Content-Security-Policy';
        meta.content = this.securityHeaders['Content-Security-Policy'];
        document.head.appendChild(meta);

        // Add other security meta tags
        Object.entries(this.securityHeaders).forEach(([header, value]) => {
            if (header !== 'Content-Security-Policy') {
                const metaTag = document.createElement('meta');
                metaTag.httpEquiv = header;
                metaTag.content = value;
                document.head.appendChild(metaTag);
            }
        });
    }

    // Setup input validation
    setupInputValidation() {
        // Validate all form inputs
        document.addEventListener('input', (e) => {
            if (e.target.matches('input, textarea, select')) {
                this.validateInput(e.target);
            }
        });

        // Validate on form submit
        document.addEventListener('submit', (e) => {
            const form = e.target;
            if (!this.validateForm(form)) {
                e.preventDefault();
                this.showSecurityWarning('Form validation failed');
            }
        });
    }

    // Validate single input
    validateInput(input) {
        const value = input.value;
        const type = input.type;
        const pattern = input.pattern;
        const maxLength = input.maxLength;

        // Check for XSS attempts
        if (this.containsXSS(value)) {
            input.style.borderColor = '#ef4444';
            input.setCustomValidity('Potentially dangerous content detected');
            return false;
        }

        // Check pattern
        if (pattern && !new RegExp(pattern).test(value)) {
            input.style.borderColor = '#f59e0b';
            return false;
        }

        // Check length
        if (maxLength && value.length > maxLength) {
            input.style.borderColor = '#f59e0b';
            return false;
        }

        // Check email format
        if (type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                input.style.borderColor = '#f59e0b';
                return false;
            }
        }

        // Valid input
        input.style.borderColor = '#10b981';
        input.setCustomValidity('');
        return true;
    }

    // Validate entire form
    validateForm(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateInput(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    // Check for XSS patterns
    containsXSS(value) {
        const xssPatterns = [
            /<script[>\s]/i,
            /javascript:/i,
            /on\w+\s*=/i,
            /<iframe/i,
            /<object/i,
            /<embed/i,
            /eval\s*\(/i,
            /expression\s*\(/i
        ];

        return xssPatterns.some(pattern => pattern.test(value));
    }

    // Setup rate limiting
    setupRateLimiting() {
        // Rate limit API calls
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            const url = args[0];
            const key = `${url}_${Date.now()}`;

            if (this.isRateLimited(url)) {
                throw new Error('Rate limit exceeded');
            }

            this.recordRequest(url);
            return originalFetch.apply(window, args);
        };
    }

    // Check if URL is rate limited
    isRateLimited(url) {
        const now = Date.now();
        const windowMs = 60000; // 1 minute
        const maxRequests = 60; // 60 requests per minute

        if (!this.rateLimits.has(url)) {
            this.rateLimits.set(url, []);
        }

        const requests = this.rateLimits.get(url);
        const recentRequests = requests.filter(time => now - time < windowMs);

        this.rateLimits.set(url, recentRequests);

        return recentRequests.length >= maxRequests;
    }

    // Record request for rate limiting
    recordRequest(url) {
        if (!this.rateLimits.has(url)) {
            this.rateLimits.set(url, []);
        }
        this.rateLimits.get(url).push(Date.now());
    }

    // Setup XSS protection
    setupXSSProtection() {
        // Sanitize innerHTML assignments
        const originalInnerHTML = Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML');
        Object.defineProperty(Element.prototype, 'innerHTML', {
            set: function(value) {
                const sanitized = this.sanitizeHTML(value);
                originalInnerHTML.set.call(this, sanitized);
            }
        });
    }

    // Sanitize HTML
    sanitizeHTML(html) {
        const temp = document.createElement('div');
        temp.textContent = html;
        return temp.innerHTML;
    }

    // Setup CSRF protection
    setupCSRFProtection() {
        // Add CSRF token to all forms
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            if (!form.querySelector('input[name="csrf_token"]')) {
                const token = this.generateCSRFToken();
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'csrf_token';
                input.value = token;
                form.appendChild(input);
            }
        });
    }

    // Generate CSRF token
    generateCSRFToken() {
        return Array.from(crypto.getRandomValues(new Uint8Array(32)))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    // Monitor suspicious activity
    monitorSuspiciousActivity() {
        // Monitor for suspicious patterns
        document.addEventListener('click', (e) => {
            // Check for clickjacking attempts
            if (e.target.closest('iframe')) {
                this.logSuspiciousActivity('Click on iframe element');
            }
        });

        // Monitor console for errors
        const originalError = console.error;
        console.error = (...args) => {
            if (args.some(arg => 
                typeof arg === 'string' && 
                (arg.includes('XSS') || arg.includes('injection') || arg.includes('security'))
            )) {
                this.logSuspiciousActivity('Security-related console error');
            }
            originalError.apply(console, args);
        };
    }

    // Log suspicious activity
    logSuspiciousActivity(description) {
        const entry = {
            timestamp: new Date().toISOString(),
            description,
            url: window.location.href,
            userAgent: navigator.userAgent
        };

        this.suspiciousActivity.push(entry);

        // Keep only last 100 entries
        if (this.suspiciousActivity.length > 100) {
            this.suspiciousActivity.shift();
        }

        console.warn('🔒 Security:', description);
    }

    // Show security warning
    showSecurityWarning(message) {
        const warning = document.createElement('div');
        warning.className = 'security-warning';
        warning.innerHTML = `
            <i class="fas fa-shield-alt"></i>
            <span>${message}</span>
        `;
        warning.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #ef4444;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
        `;

        document.body.appendChild(warning);

        setTimeout(() => {
            warning.remove();
        }, 5000);
    }

    // Get security report
    getSecurityReport() {
        return {
            rateLimits: Object.fromEntries(this.rateLimits),
            suspiciousActivity: this.suspiciousActivity,
            timestamp: new Date().toISOString()
        };
    }
}

// Initialize when DOM is ready
let securityManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        securityManager = new SecurityManager();
        securityManager.init();
    });
} else {
    securityManager = new SecurityManager();
    securityManager.init();
}

// Export
window.SecurityManager = SecurityManager;
window.securityManager = securityManager;
