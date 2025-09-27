# Security Policy

## Supported Versions

This project maintains security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### 🚨 **DO NOT** create a public GitHub issue for security vulnerabilities

### ✅ **DO** report security vulnerabilities privately:

- **Email**: Send details to `security@genx-trading.com`
2. **Subject**: `[SECURITY] GenX_FX - [Brief Description]`
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Resolved Vulnerabilities

#### CWE-798: Use of Hard-coded Credentials (Resolved 2025-09-27)

*   **Description**: Hardcoded secrets, including API keys and database credentials, were identified in the `deploy_genx.sh` and `deploy_genx_fixed.sh` deployment scripts. This exposed sensitive information and posed a significant security risk.
*   **Resolution**: The hardcoded secrets were removed from the deployment scripts. The scripts now require a `.env` file to be present, which is loaded at runtime. Users are instructed to create this file manually from the `.env.example` template and populate it with their credentials. This ensures that secrets are not stored in the repository.
*   **Impact**: This change resolves the 7 secret scanning alerts identified in the GitHub security dashboard and prevents accidental exposure of credentials.

### 🔒 **What happens next:**

1. **Acknowledgment**: You'll receive an acknowledgment within 48 hours
2. **Investigation**: We'll investigate and assess the severity
3. **Fix Development**: If confirmed, we'll develop a fix
4. **Release**: We'll release a security patch
5. **Credit**: You'll be credited in the security advisory (unless you prefer anonymity)

### 📋 **Vulnerability Types We're Interested In:**

- Authentication bypasses
- Authorization flaws
- SQL injection
- Cross-site scripting (XSS)
- Remote code execution
- Information disclosure
- Denial of service
- Cryptographic weaknesses
- Docker container escape vulnerabilities
- AWS credential exposure

### 🛡️ **Security Measures in Place:**

- Automated dependency vulnerability scanning
- CodeQL static analysis
- Secret scanning for exposed credentials
- Container security scanning
- Regular security audits
- Branch protection rules
- Required security checks before merge

### 📅 **Security Update Schedule:**

- **Critical vulnerabilities**: Immediate response (within 24 hours)
- **High severity**: Within 72 hours
- **Medium severity**: Within 1 week
- **Low severity**: Within 1 month

### 🔐 **Security Best Practices for Contributors:**

1. Never commit secrets or credentials
2. Use environment variables for sensitive data
3. Validate all inputs
4. Follow secure coding practices
5. Keep dependencies updated
6. Use HTTPS for all external connections
7. Implement proper authentication and authorization

### 📞 **Contact Information:**

- **Security Email**: [your-email@domain.com]
- **GitHub Security**: Use GitHub's private vulnerability reporting feature
- **PGP Key**: [Include your PGP key if you have one]

---

**Thank you for helping keep this project secure!** 🛡️