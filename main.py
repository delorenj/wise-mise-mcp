#!/usr/bin/env python3
"""
Main entry point for Wise Mise MCP Server.

This module provides the CLI interface for the Wise Mise MCP server.
"""

import argparse
import asyncio
import logging
import os
import sys
from importlib.metadata import version, PackageNotFoundError

from wise_mise.server import app

# Get version from package metadata
try:
    __version__ = version("wise-mise")
except PackageNotFoundError:
    __version__ = "dev"

__description__ = "Intelligent mise task management with domain expertise"


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport method (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    logging.info(f"Wise Mise Server v{__version__} starting up")
    logging.info(f"Using transport: {args.transport}")

    if args.transport == "sse":
        import uvicorn

        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level="debug" if args.verbose else "info",
        )
    else:
        await app.run_stdio()


if __name__ == "__main__":
    asyncio.run(main())
