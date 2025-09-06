#!/usr/bin/env python3
"""
Main entry point for the Wise Mise CLI and MCP Server
"""
import argparse
import json
from pathlib import Path
import sys

def main():
    """Main entry point for the CLI script."""
    parser = argparse.ArgumentParser(
        description="An intelligent CLI and MCP server for wise mise task management."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Server subcommand
    parser_server = subparsers.add_parser(
        "server", help="Run the Wise Mise MCP server."
    )
    parser_server.set_defaults(func=run_server)
    parser_server.add_argument('--http', action='store_true', help='Run with HTTP transport.')
    parser_server.add_argument('--host', type=str, default='0.0.0.0', help='Host for HTTP server.')
    parser_server.add_argument('--port', type=int, default=3000, help='Port for HTTP server.')


    # Analyze subcommand
    parser_analyze = subparsers.add_parser(
        "analyze", help="Analyze a project and get task recommendations."
    )
    parser_analyze.add_argument(
        "project_path",
        type=str,
        nargs="?",
        default=".",
        help="Path to the project directory to analyze (defaults to current directory).",
    )
    parser_analyze.set_defaults(func=run_analysis)

    args = parser.parse_args()
    args.func(args)

def run_server(args):
    """Runs the MCP server."""
    # To pass arguments like --http to the server main
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + [arg for arg in original_argv[1:] if arg not in ['server']]

    from wise_mise.server import main as server_main
    server_main()

    sys.argv = original_argv


def run_analysis(args):
    """Runs the project analysis."""
    from wise_mise.analyzer import TaskAnalyzer

    project_path = Path(args.project_path).resolve()
    if not project_path.exists():
        print(f"Error: Project path '{project_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        analyzer = TaskAnalyzer(project_path)
        structure = analyzer.analyze_project_structure()
        recommendations = analyzer.get_task_recommendations()
        existing_tasks = analyzer.extract_existing_tasks()

        output = {
            "project_path": str(project_path),
            "project_structure": {
                "package_managers": list(structure.package_managers),
                "languages": list(structure.languages),
                "frameworks": list(structure.frameworks),
                "has_tests": structure.has_tests,
                "has_docs": structure.has_docs,
                "has_ci": structure.has_ci,
                "has_database": structure.has_database,
                "source_dirs": structure.source_dirs,
            },
            "existing_tasks": [
                {
                    "name": task.full_name,
                    "domain": task.domain.value,
                    "description": task.description,
                    "complexity": task.complexity.value,
                }
                for task in existing_tasks
            ],
            "recommended_tasks": [
                {
                    "name": rec.task.full_name,
                    "domain": rec.task.domain.value,
                    "description": rec.task.description,
                    "complexity": rec.task.complexity.value,
                    "reasoning": rec.reasoning,
                    "priority": rec.priority,
                    "estimated_effort": rec.estimated_effort,
                    "dependencies_needed": rec.dependencies_needed,
                }
                for rec in recommendations
            ],
            "summary": {
                "total_existing": len(existing_tasks),
                "total_recommended": len(recommendations),
                "domains_covered": list(
                    set(rec.task.domain.value for rec in recommendations)
                ),
            },
        }
        print(json.dumps(output, indent=2))
    except Exception as e:
        print(f"An error occurred during analysis: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
