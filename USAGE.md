# Example MCP Client Configuration

Add this to your MCP client configuration (e.g., Claude Desktop config):

```json
{
  "mcpServers": {
    "mise-task-tools": {
      "command": "python",
      "args": ["/home/delorenj/code/mcp/mise-task-tools/run_server.py"],
      "cwd": "/home/delorenj/code/mcp/mise-task-tools"
    }
  }
}
```

# Example Usage Scenarios

## 1. Analyze a New Project
```
Use the analyze_project_for_tasks tool to examine a project at /path/to/project and get intelligent task recommendations.
```

## 2. Understand Task Dependencies  
```
Use trace_task_chain to understand what happens when you run `mise run build` - shows the complete dependency chain and parallel execution opportunities.
```

## 3. Add a New Task
```
Use create_task with description "Set up database with migrations and seed data" to intelligently create and organize the task.
```

## 4. Validate Architecture
```
Use validate_task_architecture to check if your mise configuration follows best practices and get improvement suggestions.
```

## 5. Clean Up Redundant Tasks
```
Use prune_tasks with dry_run=true to see what tasks might be redundant or outdated without actually removing them.
```

## 6. Get Architecture Guidance
```
Use the mise_task_expert_guidance prompt to get comprehensive guidance on mise task best practices.
```

# Advanced Usage

## For Coding Agents
The task_chain_analyst prompt provides detailed insights about project structure and development workflows by analyzing task dependencies. This helps coding agents understand:

- Project architecture from task organization
- Build and deployment patterns  
- Testing strategies
- Development tool usage
- Workflow optimization opportunities

## For Project Onboarding
1. `analyze_project_for_tasks` - Understand what the project does
2. `trace_task_chain` for "dev" or "build" - See the development workflow  
3. `get_task_recommendations` - Identify missing but useful tasks
4. `validate_task_architecture` - Check for improvements

## For CI/CD Optimization
1. `trace_task_chain` for "ci" tasks - Understand CI pipeline
2. Analyze parallel execution opportunities
3. Identify bottlenecks in dependency chains
4. Recommend task reorganization for better performance
