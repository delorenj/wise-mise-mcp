"""
FastMCP server for intelligent mise task management
"""

import sys
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
from typing import Any, Dict, Optional

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from .models import TaskDomain, TaskComplexity
from .analyzer import TaskAnalyzer
from .manager import TaskManager

# Get version from package metadata
try:
    __version__ = version("wise-mise-mcp")
except PackageNotFoundError:
    __version__ = "dev"


# Request/Response models
class AnalyzeProjectRequest(BaseModel):
    project_path: str = Field(description="Path to the project directory")


class TraceTaskChainRequest(BaseModel):
    project_path: str = Field(description="Path to the project directory")
    task_name: str = Field(description="Name of the task to trace")


class CreateTaskRequest(BaseModel):
    project_path: str = Field(description="Path to the project directory")
    task_description: str = Field(description="Description of what the task should do")
    suggested_name: Optional[str] = Field(None, description="Suggested task name")
    force_complexity: Optional[str] = Field(
        None, description="Force complexity level (simple/moderate/complex)"
    )
    domain_hint: Optional[str] = Field(
        None, description="Hint about which domain this task belongs to"
    )


class ValidateArchitectureRequest(BaseModel):
    project_path: str = Field(description="Path to the project directory")


class PruneTasksRequest(BaseModel):
    project_path: str = Field(description="Path to the project directory")
    dry_run: bool = Field(True, description="Whether to only report what would be pruned")


class RemoveTaskRequest(BaseModel):
    project_path: str = Field(description="Path to the project directory")
    task_name: str = Field(description="Name of the task to remove")


# Initialize FastMCP
app = FastMCP("Wise Mise MCP")


@app.tool()
async def analyze_project_for_tasks(
    project_path: str = Field(description="Path to the project directory")
) -> Dict[str, Any]:
    """
    Analyze a project structure and extract strategic task recommendations.

    This tool examines the project's package managers, languages, frameworks, and
    structure to recommend useful tasks organized by domain. It identifies what
    build systems, testing frameworks, and development tools are in use to suggest
    practical, actionable tasks.
    """
    try:
        project_path_obj = Path(project_path)
        
        # Security validation: reject potentially dangerous paths
        dangerous_paths = ['/etc', '/proc', '/sys', '/dev', '/bin', '/sbin', '/usr/bin', '/usr/sbin']
        resolved_path = project_path_obj.resolve()
        
        # Check if path is in dangerous system directories
        for dangerous in dangerous_paths:
            if str(resolved_path).startswith(dangerous):
                return {"error": f"Access denied: {project_path} is not allowed for security reasons"}
        
        # Check for path traversal attempts
        if '..' in str(project_path_obj) or str(resolved_path) != str(project_path_obj.absolute()):
            return {"error": f"Access denied: Path traversal detected in {project_path}"}
        
        if not project_path_obj.exists():
            return {"error": f"Project path {project_path} does not exist"}

        analyzer = TaskAnalyzer(project_path_obj)

        # Analyze project structure
        structure = analyzer.analyze_project_structure()

        # Get task recommendations
        recommendations = analyzer.get_task_recommendations()

        # Get existing tasks for context
        existing_tasks = analyzer.extract_existing_tasks()

        return {
            "project_path": str(project_path_obj),
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

    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


@app.tool()
async def trace_task_chain(
    project_path: str = Field(description="Path to the project directory"),
    task_name: str = Field(description="Name of the task to trace")
) -> Dict[str, Any]:
    """
    Trace the dependency chain for a specific task.

    This tool analyzes task dependencies to show the complete execution flow
    for a given task. It helps understand what tasks will run and in what order,
    making it easier to optimize build processes and debug issues.
    """
    try:
        project_path_obj = Path(project_path)
        if not project_path_obj.exists():
            return {"error": f"Project path {project_path} does not exist"}

        analyzer = TaskAnalyzer(project_path_obj)
        
        # Use the analyzer's trace_task_chain method
        result = analyzer.trace_task_chain(task_name)
        
        # If there's an error, return it
        if "error" in result:
            existing_tasks = analyzer.extract_existing_tasks()
            result["available_tasks"] = [task.full_name for task in existing_tasks]
            return result
        
        # Transform to expected format
        return {
            "project_path": str(project_path_obj),
            "task_name": result.get("task_name", task_name),  # Keep original field name for compatibility
            "target_task": result.get("task_name", task_name),
            "execution_order": result.get("execution_order", []),  # Keep original field for compatibility
            "execution_chain": [
                {
                    "name": task_name,
                    "domain": details.get("domain", "unknown"),
                    "description": details.get("description", ""),
                    "command": details.get("run", ""),
                    "complexity": details.get("complexity", "simple"),
                }
                for task_name, details in result.get("task_details", {}).items()
                if task_name in result.get("execution_order", [])
            ],
            "parallelizable_groups": result.get("parallelizable_groups", []),  # Keep original for compatibility
            "dependencies": result.get("dependencies", []),
            "dependents": result.get("dependents", []),
            "task_details": result.get("task_details", {}),
            "total_steps": len(result.get("execution_order", [])),
            "estimated_complexity": "simple",  # Simple default
        }

    except Exception as e:
        return {"error": f"Trace failed: {str(e)}"}


@app.tool()
async def create_task(
    project_path: str = Field(description="Path to the project directory"),
    task_description: str = Field(description="Description of what the task should do"),
    suggested_name: Optional[str] = Field(None, description="Suggested task name"),
    force_complexity: Optional[str] = Field(
        None, description="Force complexity level (simple/moderate/complex)"
    ),
    domain_hint: Optional[str] = Field(
        None, description="Hint about which domain this task belongs to"
    )
) -> Dict[str, Any]:
    """
    Create a new task with intelligent placement and configuration.

    This tool analyzes the task description and project context to suggest
    the best domain, complexity level, and implementation for a new task.
    It follows mise best practices for task organization and naming.
    """
    try:
        project_path_obj = Path(project_path)
        if not project_path_obj.exists():
            return {"error": f"Project path {project_path} does not exist"}

        manager = TaskManager(project_path_obj)

        # Parse complexity if provided
        complexity = None
        if force_complexity and isinstance(force_complexity, str):
            try:
                complexity = TaskComplexity(force_complexity.lower())
            except ValueError:
                return {
                    "error": f"Invalid complexity '{force_complexity}'. "
                    f"Must be one of: {[c.value for c in TaskComplexity]}"
                }

        # Parse domain hint if provided
        domain = None
        if domain_hint and isinstance(domain_hint, str):
            try:
                domain = TaskDomain(domain_hint.lower())
            except ValueError:
                return {
                    "error": f"Invalid domain '{domain_hint}'. "
                    f"Must be one of: {[d.value for d in TaskDomain]}"
                }

        # Create the task
        result = manager.create_task_intelligently(
            task_description=task_description,
            suggested_name=suggested_name,
            force_complexity=complexity,
        )

        return {
            "project_path": str(project_path_obj),
            "result": result,
        }

    except Exception as e:
        return {"error": f"Task creation failed: {str(e)}"}


@app.tool()
async def validate_task_architecture(
    project_path: str = Field(description="Path to the project directory")
) -> Dict[str, Any]:
    """
    Validate the current task architecture against best practices.

    This tool analyzes the existing task structure to identify issues like
    circular dependencies, missing dependencies, redundant tasks, and
    opportunities for better organization.
    """
    try:
        project_path_obj = Path(project_path)
        if not project_path_obj.exists():
            return {"error": f"Project path {project_path} does not exist"}

        analyzer = TaskAnalyzer(project_path_obj)
        existing_tasks = analyzer.extract_existing_tasks()

        if not existing_tasks:
            return {
                "project_path": str(project_path_obj),
                "validation_result": "no_tasks",
                "message": "No tasks found to validate",
            }

        # Validate architecture using the analyzer's method
        validation_result = analyzer.validate_task_architecture()

        return {
            "project_path": str(project_path_obj),
            "validation_result": "success" if not validation_result.get("issues") else "issues_found",
            **validation_result  # Include all fields from analyzer (total_tasks, domains_used, etc.)
        }

    except Exception as e:
        return {"error": f"Validation failed: {str(e)}"}


@app.tool()
async def prune_tasks(
    project_path: str = Field(description="Path to the project directory"),
    dry_run: bool = Field(True, description="Whether to only report what would be pruned")
) -> Dict[str, Any]:
    """
    Remove redundant or outdated tasks from the project.

    This tool identifies tasks that are no longer needed, have become redundant,
    or are not following current best practices. It can either report what would
    be pruned (dry run) or actually remove the tasks.
    """
    try:
        project_path_obj = Path(project_path)
        if not project_path_obj.exists():
            return {"error": f"Project path {project_path} does not exist"}

        analyzer = TaskAnalyzer(project_path_obj)
        redundant_tasks = analyzer.find_redundant_tasks()

        if dry_run:
            return {
                "project_path": str(project_path_obj),
                "dry_run": True,
                "tasks_to_prune": [
                    {
                        "name": task.get("task", "unknown"),
                        "reason": task.get("reason", "unknown"),
                        "domain": "unknown",
                    }
                    for task in redundant_tasks
                ],
                "total_to_prune": len(redundant_tasks),
            }
        else:
            # Actually prune the tasks
            manager = TaskManager(project_path_obj)
            removed_tasks = []
            for task_info in redundant_tasks:
                task_name = task_info.get("task", "")
                if task_name:
                    result = manager.remove_task(task_name)
                    if result.get("success"):
                        removed_tasks.append(task_info)
            
            return {
                "project_path": str(project_path_obj),
                "dry_run": False,
                "pruned_tasks": [
                    {
                        "name": task.get("task", "unknown"),
                        "reason": task.get("reason", "unknown"),
                        "domain": "unknown",
                    }
                    for task in removed_tasks
                ],
                "total_pruned": len(removed_tasks),
            }

    except Exception as e:
        return {"error": f"Pruning failed: {str(e)}"}


@app.tool()
async def remove_task(
    project_path: str = Field(description="Path to the project directory"),
    task_name: str = Field(description="Name of the task to remove")
) -> Dict[str, Any]:
    """
    Remove a specific task from the project.

    This tool removes a named task from the mise configuration, handling
    any cleanup needed and warning about dependent tasks that might be affected.
    """
    try:
        project_path_obj = Path(project_path)
        if not project_path_obj.exists():
            return {"error": f"Project path {project_path} does not exist"}

        manager = TaskManager(project_path_obj)

        # Check if task exists
        analyzer = TaskAnalyzer(project_path_obj)
        existing_tasks = analyzer.extract_existing_tasks()

        target_task = None
        for task in existing_tasks:
            if task.full_name == task_name or task.name == task_name:
                target_task = task
                break

        if not target_task:
            return {
                "error": f"Task '{task_name}' not found",
                "available_tasks": [task.full_name for task in existing_tasks],
            }

        # Check for dependent tasks
        task_graph = analyzer.build_dependency_graph(existing_tasks)
        dependents = analyzer.find_dependent_tasks(target_task, task_graph)

        # Remove the task
        result = manager.remove_task(target_task.full_name)

        return {
            "project_path": str(project_path_obj),
            "removed_task": {
                "name": target_task.full_name,
                "domain": target_task.domain.value,
                "description": target_task.description,
            },
            "dependent_tasks_affected": [
                {
                    "name": task.full_name,
                    "domain": task.domain.value,
                }
                for task in dependents
            ],
            "warnings": result.get("warnings", []),
            "success": result.get("success", True),
        }

    except Exception as e:
        return {"error": f"Task removal failed: {str(e)}"}


@app.tool()
async def get_task_recommendations() -> Dict[str, Any]:
    """
    Get general recommendations for mise task organization and best practices.

    This tool provides guidance on how to structure tasks effectively,
    naming conventions, dependency patterns, and optimization strategies.
    """
    return {
        "best_practices": {
            "naming": [
                "Use hierarchical names with domains (build:dev, test:unit)",
                "Keep names short but descriptive",
                "Use consistent naming patterns across domains",
                "Avoid special characters except colons for hierarchy",
            ],
            "organization": [
                "Group related tasks by domain (build, test, lint, deploy)",
                "Use sub-domains for environment or type (dev/prod, unit/e2e)",
                "Keep task files organized in .mise/tasks/ directory",
                "One domain per file when using TOML format",
            ],
            "dependencies": [
                "Declare explicit dependencies rather than implicit ordering",
                "Avoid circular dependencies",
                "Use source/output tracking for incremental builds",
                "Keep dependency chains shallow when possible",
            ],
            "performance": [
                "Use source tracking to avoid unnecessary rebuilds",
                "Parallelize independent tasks",
                "Cache expensive operations",
                "Use outputs to enable incremental workflows",
            ],
        },
        "common_patterns": {
            "build_pipeline": "lint → test → build → deploy",
            "development": "install → dev (parallel with test:watch)",
            "ci_pipeline": "install → lint → test → build → deploy",
            "release": "test → build → version → publish",
        },
        "domain_guidelines": {
            "build": "Compilation, bundling, asset processing",
            "test": "Unit, integration, e2e testing",
            "lint": "Code quality, formatting, static analysis",
            "deploy": "Deployment, release, publishing",
            "dev": "Development servers, hot reloading",
            "db": "Database operations, migrations",
            "docs": "Documentation generation, serving",
            "clean": "Cleanup, reset operations",
        },
    }


@app.tool()
async def get_mise_architecture_rules() -> Dict[str, Any]:
    """
    Get the architectural rules and patterns that Wise Mise MCP follows.

    This tool explains the design principles, domain organization, and
    architectural decisions that guide intelligent task management.
    """
    return {
        "architecture_principles": {
            "domain_driven": "Tasks are organized by functional domains (build, test, etc.)",
            "hierarchical": "Use colon-separated names for sub-domains and environments",
            "dependency_explicit": "All dependencies should be explicitly declared",
            "source_aware": "Track source files to enable incremental builds",
            "output_tracked": "Define outputs for caching and dependency resolution",
        },
        "domain_hierarchy": {
            "build": {
                "purpose": "Compilation, bundling, asset processing",
                "sub_domains": ["dev", "prod", "watch", "clean"],
                "typical_sources": ["src/**/*", "package.json", "tsconfig.json"],
                "typical_outputs": ["dist/**/*", "build/**/*"],
            },
            "test": {
                "purpose": "All forms of testing",
                "sub_domains": ["unit", "integration", "e2e", "watch", "coverage"],
                "typical_sources": ["src/**/*", "test/**/*", "tests/**/*"],
                "typical_outputs": ["coverage/**/*", "test-results/**/*"],
            },
            "lint": {
                "purpose": "Code quality and formatting",
                "sub_domains": ["code", "types", "format", "fix"],
                "typical_sources": ["src/**/*", "test/**/*"],
                "typical_outputs": ["lint-results.json"],
            },
            "deploy": {
                "purpose": "Deployment and publishing",
                "sub_domains": ["staging", "prod", "preview"],
                "typical_sources": ["dist/**/*", "build/**/*"],
                "typical_outputs": ["deployment-info.json"],
            },
        },
        "complexity_levels": {
            "simple": {
                "description": "Single command, no complex logic",
                "examples": ["npm run build", "python -m pytest"],
                "characteristics": ["One-liner", "No conditionals", "Standard tools"],
            },
            "moderate": {
                "description": "Multiple steps or conditional logic",
                "examples": ["Build with environment checks", "Multi-stage testing"],
                "characteristics": ["2-5 commands", "Some conditionals", "Environment aware"],
            },
            "complex": {
                "description": "Advanced workflows with multiple tools",
                "examples": ["Full CI/CD pipeline", "Multi-environment deployment"],
                "characteristics": ["Many steps", "Complex logic", "Multiple tools"],
            },
        },
        "dependency_patterns": {
            "sequential": "A → B → C (each step depends on the previous)",
            "parallel": "A + B → C (independent tasks feeding into one)",
            "fan_out": "A → B + C (one task enabling multiple)",
            "diamond": "A → B + C → D (parallel middle, converging end)",
        },
    }


@app.tool()
async def mise_task_expert_guidance() -> Dict[str, Any]:
    """
    Get expert guidance on mise task management and optimization.

    This tool provides advanced tips, troubleshooting advice, and expert
    recommendations for getting the most out of mise task management.
    """
    return {
        "expert_tips": {
            "performance_optimization": [
                "Use source tracking to avoid unnecessary task execution",
                "Leverage outputs for proper caching and incremental builds",
                "Parallelize independent tasks with proper dependency declaration",
                "Use environment-specific tasks (dev vs prod) to optimize workflows",
                "Consider task granularity - too fine-grained can hurt performance",
            ],
            "debugging_tasks": [
                "Use 'mise tasks ls' to see all available tasks",
                "Check 'mise tasks deps <task>' to understand dependencies",
                "Use 'mise run --dry-run <task>' to see what would execute",
                "Enable verbose output with 'mise run -v <task>' for debugging",
                "Check source/output tracking with 'mise tasks info <task>'",
            ],
            "advanced_patterns": [
                "Use task templates for repetitive patterns",
                "Implement conditional tasks based on environment",
                "Create meta-tasks that orchestrate multiple workflows",
                "Use file watching for development workflows",
                "Implement proper cleanup tasks for each domain",
            ],
        },
        "common_issues": {
            "circular_dependencies": {
                "problem": "Tasks depend on each other in a loop",
                "solution": "Refactor to break the cycle, often by extracting common dependencies",
                "prevention": "Use dependency visualization tools regularly",
            },
            "slow_builds": {
                "problem": "Tasks take too long to execute",
                "solution": "Implement proper source tracking and output caching",
                "prevention": "Design tasks with incremental builds in mind",
            },
            "missing_dependencies": {
                "problem": "Tasks fail because prerequisites aren't met",
                "solution": "Explicitly declare all dependencies",
                "prevention": "Use validation tools to check architecture",
            },
        },
        "migration_strategies": {
            "from_npm_scripts": [
                "Map npm scripts to appropriate mise domains",
                "Convert package.json scripts to .mise/tasks/ files",
                "Add proper source/output tracking",
                "Implement dependency relationships",
            ],
            "from_make": [
                "Convert Makefile targets to mise tasks",
                "Map make dependencies to mise dependencies",
                "Use mise's source tracking instead of file timestamps",
                "Organize by domain rather than alphabetically",
            ],
            "from_just": [
                "Convert justfile recipes to mise tasks",
                "Maintain recipe organization but add domain structure",
                "Add source/output tracking for better caching",
                "Use mise's environment handling",
            ],
        },
    }


@app.tool()
async def task_chain_analyst() -> Dict[str, Any]:
    """
    Analyze and optimize task execution chains for better performance.

    This tool provides insights into task execution patterns, identifies
    bottlenecks, and suggests optimizations for complex task workflows.
    """
    return {
        "analysis_techniques": {
            "critical_path": "Identify the longest chain of dependent tasks",
            "parallelization": "Find tasks that can run concurrently",
            "bottleneck_detection": "Locate tasks that block multiple others",
            "redundancy_analysis": "Find duplicate or unnecessary work",
        },
        "optimization_strategies": {
            "dependency_reduction": [
                "Remove unnecessary dependencies",
                "Use outputs instead of implicit dependencies",
                "Break large tasks into smaller, more focused ones",
            ],
            "parallel_execution": [
                "Identify independent tasks that can run together",
                "Use proper dependency declaration to enable parallelism",
                "Consider resource constraints when parallelizing",
            ],
            "caching_optimization": [
                "Implement proper source tracking",
                "Use outputs for intermediate results",
                "Cache expensive operations across runs",
            ],
        },
        "performance_metrics": {
            "execution_time": "Total time from start to finish",
            "parallel_efficiency": "How well tasks utilize available parallelism",
            "cache_hit_rate": "Percentage of tasks skipped due to caching",
            "dependency_depth": "Maximum depth of dependency chains",
        },
        "visualization_tips": [
            "Use dependency graphs to understand task relationships",
            "Create execution timelines to identify bottlenecks",
            "Track cache hit rates over time",
            "Monitor parallel execution efficiency",
        ],
    }


def main():
    """Main entry point for the MCP server."""
    import sys
    import os
    
    # For Docker/HTTP deployment, check if we should use HTTP transport
    if ('--transport' in sys.argv and 'http' in sys.argv) or '--http' in sys.argv or os.getenv('MCP_TRANSPORT') == 'http':
        # Run with HTTP transport for Docker/web deployment
        port = 3000
        host = "0.0.0.0"
        
        # Parse port from command line args
        try:
            if '--port' in sys.argv:
                port_idx = sys.argv.index('--port') + 1
                port = int(sys.argv[port_idx])
        except (ValueError, IndexError):
            port = 3000
            
        # Parse host from command line args
        try:
            if '--host' in sys.argv:
                host_idx = sys.argv.index('--host') + 1
                host = sys.argv[host_idx]
        except IndexError:
            host = "0.0.0.0"
            
        print(f"Starting HTTP MCP server on {host}:{port}")
        
        # Add health check endpoint for Docker - access underlying FastAPI app
        try:
            @app.app.get("/health")
            async def health_check():
                return {"status": "healthy", "service": "wise-mise-mcp"}
        except Exception as e:
            print(f"Could not add health endpoint: {e}")
            
        app.run(transport="http", host=host, port=port, path="/mcp")
    else:
        # Default to stdio transport
        app.run()


if __name__ == "__main__":
    main()