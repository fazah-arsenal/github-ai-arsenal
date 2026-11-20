# Contributing to FAZAH AI Arsenal (`github-ai-arsenal`)

Thank you for your interest in contributing to **FAZAH AI Arsenal**! We welcome pull requests for new curated tools, Awesome-list sources, MCP integrations, security rules, and bug fixes.

## 🚀 Quick Ways to Contribute

1. **Add an Elite Tool**: Edit `references/catalog.json` to add high-impact open-source GitHub tools with accurate `use_when` descriptions and `install` commands.
2. **Add a New Domain / Awesome List**: Add curated Awesome list repositories to `scripts/build_mega_index.py` and run `python scripts/build_mega_index.py`.
3. **Add a Turnkey Project Stack**: Add a cohesive architecture blueprint to `references/stacks.json`.
4. **Enhance Security Scanning**: Add supply-chain detection patterns to `DANGEROUS_PATTERNS` in `scripts/gh_arsenal.py`.

## 🧪 Development & Testing Rules

- **Zero External Dependencies**: All core CLI (`scripts/gh_arsenal.py`), MCP server (`scripts/mcp_server.py`), and Local Web UI (`scripts/web_ui.py`) code MUST use **Python 3.9+ standard library only**.
- **Run Tests Before Submitting**:
  ```bash
  python -m unittest discover -s tests -v
  ```
- **Sync Versions**: When bumping versions, always run:
  ```bash
  python scripts/bump_version.py <new_version>
  ```

## 📞 Contact Maintainer
- **Maintainer**: FAZAH
- **Telegram**: [@testtttttttt11222](https://t.me/testtttttttt11222)
- **Email**: `mhamadabdalla150150@gmail.com`
