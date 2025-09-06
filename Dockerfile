# Use Python 3.11 slim base image for better performance and security
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for compilation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml uv.lock ./
COPY README.md ./

# Install UV for fast Python package management
RUN pip install uv

# Install dependencies using UV
RUN uv pip install --system --no-cache-dir -e .

# Copy source code
COPY wise_mise/ ./wise_mise/

# Create a non-root user for security
RUN groupadd -r mcp && useradd -r -g mcp -d /app -s /bin/bash mcp && \
    chown -R mcp:mcp /app

# Switch to non-root user
USER mcp

# Expose port for HTTP MCP server
EXPOSE 3000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check to ensure MCP server is running  
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -s http://localhost:3000/mcp > /dev/null || exit 1

# Default command to start the MCP server in HTTP mode
CMD ["python", "-m", "wise_mise.server", "--transport", "http", "--port", "3000", "--host", "0.0.0.0"]