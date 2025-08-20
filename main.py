#!/usr/bin/env python3

"""
Wise Mise MCP Server - Production Entry Point

A sophisticated MCP server for intelligent mise task management and organization.
Provides comprehensive tools for analyzing, creating, and optimizing mise tasks
with domain-specific expertise and intelligent recommendations.

Features:
- Intelligent task creation with domain expertise
- Project structure analysis and recommendations  
- Task dependency tracing and validation
- Architecture compliance checking
- Automated task pruning and optimization
- Production-ready logging and error handling
- Health monitoring and diagnostics

Usage:
    python main.py                    # Start MCP server (stdio mode)
    python main.py --config config.json  # Use custom configuration
    python main.py --health           # Run health check
    python main.py --version          # Show version info
"""

import sys
import os
import logging
import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add the package to Python path for development
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from wise_mise_mcp.server import app
from wise_mise_mcp.models import TaskDomain, TaskComplexity

# Version information
__version__ = "0.1.0"
__author__ = "Jarad DeLorenzo"
__description__ = "Intelligent MCP server for wise mise task management"


class ServerConfig:
    """Server configuration management"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".config" / "wise-mise-mcp" / "config.json"
        self.config: Dict[str, Any] = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with sensible defaults"""
        defaults = {
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": None,  # None means stderr only
                "max_size_mb": 10,
                "backup_count": 3
            },
            "server": {
                "name": "Wise Mise MCP Server",
                "description": "Intelligent mise task management with domain expertise",
                "version": __version__,
                "author": __author__
            },
            "features": {
                "health_check": True,
                "metrics": True,
                "verbose_errors": False,  # Set to True for development
                "auto_documentation": True
            },
            "task_defaults": {
                "complexity_threshold": {
                    "simple_max_commands": 1,
                    "moderate_max_commands": 5
                },
                "domain_priorities": {
                    "build": 9,
                    "test": 8,
                    "lint": 7,
                    "ci": 8,
                    "deploy": 6,
                    "dev": 5,
                    "db": 7,
                    "docs": 4,
                    "clean": 3,
                    "setup": 8
                }
            }
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    # Merge user config with defaults
                    return self._deep_merge(defaults, user_config)
            except Exception as e:
                logging.warning(f"Failed to load config from {self.config_path}: {e}")
        
        return defaults
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)


def setup_logging(config: ServerConfig) -> None:
    """Setup production-ready logging"""
    log_config = config.config["logging"]
    
    # Configure logging level
    level = getattr(logging, log_config["level"].upper(), logging.INFO)
    
    # Setup formatter
    formatter = logging.Formatter(
        fmt=log_config["format"],
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Clear any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    
    # Add file handler if configured
    if log_config.get("file"):
        try:
            from logging.handlers import RotatingFileHandler
            log_file = Path(log_config["file"])
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=log_config["max_size_mb"] * 1024 * 1024,
                backupCount=log_config["backup_count"]
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            logger.addHandler(file_handler)
            
            logging.info(f"File logging enabled: {log_file}")
        except Exception as e:
            logging.warning(f"Failed to setup file logging: {e}")
    
    # Log startup info
    logging.info(f"Wise Mise MCP Server v{__version__} starting up")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Working directory: {os.getcwd()}")


def health_check() -> Dict[str, Any]:
    """Perform comprehensive health check"""
    health = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": __version__,
        "python_version": sys.version,
        "checks": {}
    }
    
    try:
        # Check FastMCP import
        from fastmcp import FastMCP
        health["checks"]["fastmcp"] = {"status": "ok", "version": getattr(FastMCP, '__version__', 'unknown')}
    except ImportError as e:
        health["checks"]["fastmcp"] = {"status": "error", "error": str(e)}
        health["status"] = "degraded"
    
    try:
        # Check networkx import
        import networkx as nx
        health["checks"]["networkx"] = {"status": "ok", "version": nx.__version__}
    except ImportError as e:
        health["checks"]["networkx"] = {"status": "error", "error": str(e)}
        health["status"] = "degraded"
    
    try:
        # Check pydantic import
        import pydantic
        health["checks"]["pydantic"] = {"status": "ok", "version": pydantic.VERSION}
    except ImportError as e:
        health["checks"]["pydantic"] = {"status": "error", "error": str(e)}
        health["status"] = "degraded"
    
    try:
        # Check TOML support
        import tomli, tomli_w
        health["checks"]["toml_support"] = {"status": "ok", "tomli": tomli.__version__, "tomli_w": tomli_w.__version__}
    except ImportError as e:
        health["checks"]["toml_support"] = {"status": "error", "error": str(e)}
        health["status"] = "degraded"
    
    try:
        # Test project structure analysis
        from wise_mise_mcp.models import ProjectStructure
        test_path = Path(".")
        structure = ProjectStructure.analyze(test_path)
        health["checks"]["project_analysis"] = {
            "status": "ok",
            "test_project": {
                "path": str(test_path.absolute()),
                "package_managers": list(structure.package_managers),
                "languages": list(structure.languages)
            }
        }
    except Exception as e:
        health["checks"]["project_analysis"] = {"status": "error", "error": str(e)}
        health["status"] = "degraded"
    
    # Check domains and experts
    try:
        domains = [domain.value for domain in TaskDomain]
        complexities = [complexity.value for complexity in TaskComplexity]
        health["checks"]["task_system"] = {
            "status": "ok",
            "domains": domains,
            "complexities": complexities,
            "domain_count": len(domains)
        }
    except Exception as e:
        health["checks"]["task_system"] = {"status": "error", "error": str(e)}
        health["status"] = "degraded"
    
    # Overall health assessment
    error_checks = [check for check in health["checks"].values() if check["status"] == "error"]
    if error_checks:
        health["status"] = "unhealthy"
    
    health["summary"] = {
        "total_checks": len(health["checks"]),
        "passed": len([c for c in health["checks"].values() if c["status"] == "ok"]),
        "failed": len(error_checks)
    }
    
    return health


def show_version() -> None:
    """Display detailed version information"""
    print(f"Wise Mise MCP Server v{__version__}")
    print(f"Author: {__author__}")
    print(f"Description: {__description__}")
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")
    
    # Show dependencies
    deps = [
        ("fastmcp", "FastMCP framework"),
        ("networkx", "Graph analysis"),  
        ("pydantic", "Data validation"),
        ("tomli", "TOML parsing"),
        ("tomli_w", "TOML writing")
    ]
    
    print("\nDependencies:")
    for dep_name, description in deps:
        try:
            module = __import__(dep_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"  {dep_name:12} {version:10} - {description}")
        except ImportError:
            print(f"  {dep_name:12} {'MISSING':10} - {description}")
    
    print(f"\nFeatures:")
    print(f"  • Intelligent task creation with domain expertise")
    print(f"  • Project structure analysis and recommendations")
    print(f"  • Task dependency tracing and validation")
    print(f"  • Architecture compliance checking")
    print(f"  • Automated task pruning and optimization")
    print(f"  • Production-ready logging and monitoring")
    
    # Show supported domains
    try:
        domains = [domain.value for domain in TaskDomain]
        print(f"\nSupported Task Domains ({len(domains)}):")
        for i, domain in enumerate(sorted(domains), 1):
            print(f"  {i:2}. {domain}")
    except:
        print("\nUnable to load task domain information")


def create_example_project() -> None:
    """Create an example project structure for demonstration"""
    example_dir = Path("./example-project")
    
    if example_dir.exists():
        print(f"Example project already exists at {example_dir}")
        return
    
    print(f"Creating example project at {example_dir}...")
    
    # Create directory structure
    (example_dir / "src").mkdir(parents=True, exist_ok=True)
    (example_dir / "tests").mkdir(parents=True, exist_ok=True)
    (example_dir / "docs").mkdir(parents=True, exist_ok=True)
    
    # Create example files
    files = {
        "package.json": {
            "name": "example-project",
            "version": "1.0.0",
            "scripts": {
                "build": "webpack",
                "test": "jest",
                "dev": "webpack serve",
                "lint": "eslint src/"
            },
            "dependencies": {
                "react": "^18.0.0"
            },
            "devDependencies": {
                "webpack": "^5.0.0",
                "jest": "^29.0.0",
                "eslint": "^8.0.0"
            }
        },
        "src/index.js": "console.log('Hello, World!');",
        "tests/index.test.js": "test('example', () => { expect(1 + 1).toBe(2); });",
        "README.md": "# Example Project\n\nAn example project for demonstrating Wise Mise MCP Server capabilities.",
        ".mise.toml": """
# Example mise configuration
[tools]
node = "20"

[tasks.hello]
run = "echo 'Hello from mise!'"
description = "Simple greeting task"
"""
    }
    
    for file_path, content in files.items():
        full_path = example_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.endswith('.json'):
            with open(full_path, 'w') as f:
                json.dump(content, f, indent=2)
        else:
            with open(full_path, 'w') as f:
                f.write(content)
    
    print(f"✅ Example project created at {example_dir}")
    print(f"""
Try these commands:
    cd {example_dir}
    mise task ls  # List existing tasks
    
    # Or use the MCP server to analyze it:
    # Call analyze_project_for_tasks with project_path: "{example_dir.absolute()}"
    """)


def main() -> int:
    """Main entry point with comprehensive argument handling"""
    parser = argparse.ArgumentParser(
        description=f"{__description__} v{__version__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python main.py                     # Start MCP server
  python main.py --health            # Run health check
  python main.py --version           # Show version info
  python main.py --create-example    # Create example project
  python main.py --config myconfig.json  # Use custom config
        """
    )
    
    parser.add_argument(
        '--version', '-v', 
        action='store_true',
        help='Show version information and exit'
    )
    
    parser.add_argument(
        '--health',
        action='store_true', 
        help='Run health check and exit'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=Path,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--create-example',
        action='store_true',
        help='Create an example project for testing'
    )
    
    parser.add_argument(
        '--log-level', 
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Override log level'
    )
    
    args = parser.parse_args()
    
    # Handle version request
    if args.version:
        show_version()
        return 0
    
    # Handle example project creation
    if args.create_example:
        create_example_project()
        return 0
    
    # Load configuration
    try:
        config = ServerConfig(args.config)
        
        # Override log level if provided
        if args.log_level:
            config.config["logging"]["level"] = args.log_level
            
        setup_logging(config)
        
    except Exception as e:
        print(f"Failed to initialize configuration: {e}", file=sys.stderr)
        return 1
    
    # Handle health check
    if args.health:
        print("Running health check...")
        health = health_check()
        print(json.dumps(health, indent=2))
        return 0 if health["status"] in ["healthy", "degraded"] else 1
    
    # Start the MCP server
    try:
        logging.info("Starting Wise Mise MCP Server...")
        logging.info(f"Server config: {config.config['server']}")
        
        # Log available features
        logging.info("Available MCP tools:")
        tools = [
            "analyze_project_for_tasks - Project analysis and task recommendations",
            "trace_task_chain - Task dependency tracing and visualization", 
            "create_task - Intelligent task creation with domain expertise",
            "validate_task_architecture - Architecture compliance checking",
            "prune_tasks - Automated task pruning and optimization",
            "remove_task - Safe task removal with cleanup",
            "get_task_recommendations - Strategic improvement recommendations",
            "get_mise_architecture_rules - Architecture rules and best practices"
        ]
        for tool in tools:
            logging.info(f"  • {tool}")
        
        logging.info("Available MCP prompts:")
        prompts = [
            "mise_task_expert_guidance - Expert guidance on task architecture",
            "task_chain_analyst - Task dependency analysis and insights"
        ]
        for prompt in prompts:
            logging.info(f"  • {prompt}")
        
        # Run initial health check
        health = health_check()
        if health["status"] == "unhealthy":
            logging.error("Server health check failed - some critical components unavailable")
            for check_name, check_result in health["checks"].items():
                if check_result["status"] == "error":
                    logging.error(f"  {check_name}: {check_result.get('error', 'Unknown error')}")
            return 1
        elif health["status"] == "degraded":
            logging.warning("Server started in degraded mode - some optional features unavailable")
        else:
            logging.info("✅ All health checks passed - server ready")
        
        # Start the FastMCP server (stdio mode)
        logging.info("Server starting in stdio mode...")
        app.run()
        
    except KeyboardInterrupt:
        logging.info("Server shutdown requested by user")
        return 0
    except Exception as e:
        logging.error(f"Server startup failed: {e}")
        if config.config["features"]["verbose_errors"]:
            logging.exception("Full error details:")
        return 1
    finally:
        logging.info("Wise Mise MCP Server shutdown complete")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())