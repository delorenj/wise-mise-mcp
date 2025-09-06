#!/usr/bin/env python3
"""
Main executable entry point for the Mise Task Tools MCP Server
"""

import sys
import asyncio
from pathlib import Path

# Add the package to Python path for development
sys.path.insert(0, str(Path(__file__).parent))

from wise_mise.server import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down Mise Task Tools MCP Server...")
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)
