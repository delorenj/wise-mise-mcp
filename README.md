# Mise Task Tools MCP Server

An opinionated MCP server for intelligent mise task management, organization, and maintenance.

## Features

- **Domain Expert Analysis**: Analyze projects to extract useful, strategically organized tasks
- **Task Chain Tracing**: Reverse-engineer task dependencies to provide context to other agents
- **Intelligent Task Creation**: Add tasks with automatic placement, organization, and documentation
- **Task Pruning**: Remove outdated or redundant tasks to keep the task set lean and purposeful
- **Architecture Enforcement**: Ensure tasks follow the comprehensive mise architecture rules

## Installation

```bash
cd /home/delorenj/code/mcp/mise-task-tools
pip install -e .
```

## Usage

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "mise-task-tools": {
      "command": "python",
      "args": ["-m", "mise_task_tools"],
      "cwd": "/home/delorenj/code/mcp/mise-task-tools"
    }
  }
}
```

## Architecture

This server implements the comprehensive mise task architecture with:

- 10 core domains (build, test, lint, dev, deploy, db, ci, docs, clean, setup)
- Hierarchical task organization with colon separators
- Intelligent source/output tracking
- Dependency graph management
- Performance optimization through incremental builds

## Tools

- `analyze_project_for_tasks`: Extract strategic tasks from project structure
- `trace_task_chain`: Analyze task dependencies and execution flow
- `create_task`: Intelligently add new tasks with proper organization
- `prune_tasks`: Remove outdated or redundant tasks
- `validate_task_architecture`: Ensure mise configuration follows best practices
- `get_task_recommendations`: Get suggestions for improving task organization

## Domain Experts

The server includes specialized domain experts for:
- Frontend/Backend build systems
- Testing frameworks and strategies  
- CI/CD pipeline optimization
- Database operations
- Development workflow
- Documentation generation
