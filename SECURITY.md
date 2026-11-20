# Security Policy

## Supported Versions

| Version | Supported |
| :--- | :---: |
| `6.5.x` (Latest) | ✅ Yes |
| `6.0.x` | ✅ Yes |
| `< 6.0` | ❌ Upgrade via `fazah up` |

## Built-In Safety Protections

FAZAH AI Arsenal is designed with security-first defaults for autonomous AI agents:
- **Zero External Python Dependencies**: Eliminates third-party PyPI supply-chain attack surface.
- **Zip-Slip Path Traversal Guard**: `pull` strictly validates every extracted archive path.
- **Pre-Install Auditing (`fazah a` & `fazah scan`)**: Evaluates Trust Score (0–100) and scans `setup.py`, `package.json`, `install.sh`, and `Dockerfile` for malicious patterns (`curl | sh`, obfuscated base64, webhooks, suspicious lifecycle hooks).
- **Isolated Sandbox (`fazah try`)**: Tests unfamiliar Python repositories inside a clean temporary `venv`.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly instead of opening a public issue:
- **Email**: `mhamadabdalla150150@gmail.com`
- **Telegram**: [@testtttttttt11222](https://t.me/testtttttttt11222)

We aim to acknowledge all security reports within 24–48 hours.
