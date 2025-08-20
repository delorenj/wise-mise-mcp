# Documentation

This directory contains comprehensive documentation for Wise Mise MCP.

## 📚 Documentation Index

- **[Main README](../README.md)** - Project overview, installation, and quick start
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Changelog](CHANGELOG.md)** - Release history and version changes

## 🔗 External Documentation

- **[GitHub Repository](https://github.com/delorenj/wise-mise-mcp)** - Source code and issue tracking
- **[PyPI Package](https://pypi.org/project/wise-mise-mcp/)** - Package distribution
- **[API Documentation](https://wise-mise-mcp.readthedocs.io/)** - Detailed API reference

## 📋 Quick Reference

### Installation
```bash
# With UV (recommended)
uv add wise-mise-mcp

# Traditional pip
pip install wise-mise-mcp
```

### MCP Configuration
```json
{
  "mcpServers": {
    "wise-mise-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "wise_mise_mcp"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

### Core Tools
- `analyze_project_for_tasks` - Extract strategic tasks
- `trace_task_chain` - Map task dependencies  
- `create_task` - Add intelligent tasks
- `prune_tasks` - Remove redundant tasks
- `validate_task_architecture` - Ensure best practices
- `get_task_recommendations` - Get optimization suggestions

---

*For complete documentation, see the [main README](../README.md)*