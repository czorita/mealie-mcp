# Mealie MCP Server
# FastMCP-based Model Context Protocol server for Mealie integration

FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Run as a non-root user
RUN useradd --create-home --uid 1000 mcpuser
USER mcpuser

# The server communicates over HTTP so it can be reached from a separate
# machine on the network. Configurable via MCP_HOST (default 0.0.0.0) and
# MCP_PORT (default 8000); the actual external exposure is controlled by
# how the port is published at the Docker/compose level, not by this value.
# Environment variables MEALIE_URL and MEALIE_API_TOKEN must be provided at
# runtime - MEALIE_API_TOKEN also serves as the MCP endpoint's bearer token.
EXPOSE 8000

ENTRYPOINT ["python", "-m", "src.server"]
