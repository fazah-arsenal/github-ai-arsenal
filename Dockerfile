FROM python:3.12-slim

WORKDIR /app
COPY scripts/ ./scripts/
COPY references/ ./references/
COPY SKILL.md README.md LICENSE VERSION pyproject.toml ./

ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python3", "scripts/mcp_server.py"]
