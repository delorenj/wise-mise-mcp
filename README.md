# 🎯 Wise Mise

> **The intelligent CLI and MCP server that transforms mise task management with AI-powered analysis and domain expertise**

[![PyPI version](https://badge.fury.io/py/wise-mise.svg)](https://badge.fury.io/py/wise-mise)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-blue.svg)](https://wise-mise.readthedocs.io)
[![Deploy to Smithery](https://smithery.ai/badge)](https://smithery.ai/server/wise-mise)

**Stop wrestling with mise configuration.** Wise Mise brings enterprise-grade intelligence to your [mise](https://mise.jdx.dev/) workflow. Use it as a powerful **CLI** for instant project analysis, or run it as an **MCP server** to supercharge your existing development tools.

## Why Wise Mise?

**🧠 Intelligent Task Analysis**

- Automatically analyzes your project structure to extract meaningful tasks
- Understands 10+ technology domains (build, test, lint, deploy, CI/CD, etc.)
- Suggests optimal task organization and dependency patterns

**🏗️ Architecture-Aware**

- Follows mise best practices with hierarchical task organization
- Supports complex dependency graphs with source/output tracking
- Optimizes for incremental builds and performance

**🔧 Developer Experience**

- Integrates seamlessly with any MCP-compatible client
- Provides detailed explanations and recommendations
- Reduces cognitive load of task management

## Quick Start

### CLI Usage (Recommended)

Install and run the analyzer on your project in one command:
```bash
uvx wise-mise analyze .
```

Or, install it first:
```bash
uv tool install wise-mise
# then run it
wise-mise analyze .
```

### MCP Server Usage

If you want to use Wise Mise as an MCP server, you can start it with:
```bash
wise-mise server
```

You can also use `uvx` to run the server without installing:
```bash
uvx wise-mise server
```

#### Add to Your MCP Client

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "wise-mise": {
      "command": "wise-mise",
      "args": ["server"]
    }
  }
}
```

### Deploy with Smithery (One-Click Deployment)

[![Deploy to Smithery](https://smithery.ai/badge)](https://smithery.ai/server/wise-mise)

Deploy Wise Mise MCP instantly to Smithery's cloud infrastructure with one click. Smithery provides managed MCP server hosting with built-in monitoring, scaling, and zero-configuration deployment.

**Quick Smithery Deployment:**
1. Click the "Deploy to Smithery" badge above
2. Connect your GitHub account (if needed)
3. Your MCP server will be automatically deployed and configured
4. Use the provided endpoint in your MCP client configuration

**Benefits of Smithery Deployment:**
- ✅ Zero server management overhead
- ✅ Automatic scaling and load balancing  
- ✅ Built-in monitoring and health checks
- ✅ Global CDN for low-latency access
- ✅ Automatic SSL/TLS encryption
- ✅ Integration with popular MCP clients

## What Makes It "Wise"?

Wise Mise goes beyond simple task creation. It brings intelligence to your mise configuration:

### 🔍 Project Analysis

The `analyze` command gives you an instant overview of your project and suggests a task architecture.
```bash
wise-mise analyze .
```
```json
{
  "project_path": "/path/to/your/project",
  "project_structure": {
    "package_managers": ["npm"],
    "languages": ["javascript", "typescript"],
    "frameworks": ["react", "next.js"]
  },
  "recommended_tasks": [
    {
      "name": "build:prod",
      "domain": "build",
      "description": "Build for production",
      "reasoning": "Detected Next.js production build script."
    }
  ]
}
```
This output can be used directly or as a starting point for your `.mise.toml`.

## Core Features

### 🎯 **Domain Experts**

- **Build**: Frontend/Backend build systems, bundlers, compilers
- **Test**: Unit, integration, e2e testing strategies
- **Lint**: Code quality, formatting, static analysis
- **Deploy**: CI/CD, containerization, release management
- **Database**: Migrations, seeding, schema management
- **Development**: Local dev servers, hot reloading, debugging

### 📊 **Intelligent Analysis**

- **Complexity Assessment**: Automatically categorizes tasks as Simple, Moderate, or Complex
- **Dependency Detection**: Identifies natural task relationships
- **Source/Output Tracking**: Optimizes incremental builds
- **Redundancy Elimination**: Finds and removes duplicate tasks

### 🔧 **MCP Tools**

| Tool                         | Purpose                                        |
| ---------------------------- | ---------------------------------------------- |
| `analyze_project_for_tasks`  | Extract strategic tasks from project structure |
| `trace_task_chain`           | Map task dependencies and execution flow       |
| `create_task`                | Add new tasks with intelligent placement       |
| `prune_tasks`                | Remove outdated or redundant tasks             |
| `validate_task_architecture` | Ensure configuration follows best practices    |
| `get_task_recommendations`   | Get suggestions for optimization               |

## Architecture Philosophy

Wise Mise follows a **Domain-Driven Design** approach to task organization:

### 🏛️ **Hierarchical Structure**

- **Level 1**: Domain (build, test, lint, etc.)
- **Level 2**: Environment/Type (dev, prod, unit, e2e)
- **Level 3**: Specific Implementation (server, client, api)

### 🔄 **Dependency Patterns**

- **Sequential**: `lint → test → build → deploy`
- **Parallel**: `test:unit` + `test:e2e` → `deploy`
- **Conditional**: `deploy:staging` → `test:smoke` → `deploy:prod`

### ⚡ **Performance Optimization**

- **Source Tracking**: Only rebuild when sources change
- **Output Caching**: Reuse previous build artifacts
- **Incremental Builds**: Support for modern build tools

## Technology Support

Wise Mise includes expert knowledge for:

**Frontend**: React, Vue, Angular, Svelte, Next.js, Nuxt, Vite, Webpack
**Backend**: Node.js, Python, Go, Rust, Java, .NET, PHP
**Databases**: PostgreSQL, MySQL, MongoDB, Redis, Prisma, TypeORM
**Testing**: Jest, Vitest, Cypress, Playwright, PyTest, Go Test
**CI/CD**: GitHub Actions, GitLab CI, CircleCI, Jenkins
**Deployment**: Docker, Kubernetes, Vercel, Netlify, AWS, GCP

## Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Start for Contributors

```bash
# Clone and setup with UV
git clone https://github.com/delorenj/wise-mise
cd wise-mise
uv sync

# Run tests
uv run pytest

# Format code
uv run black .
uv run ruff check --fix .
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- **Documentation**: [Full API Documentation](https://wise-mise.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/delorenj/wise-mise/issues)
- **Discussions**: [GitHub Discussions](https://github.com/delorenj/wise-mise/discussions)

---

_Built with ❤️ by [Jarad DeLorenzo](https://github.com/delorenj) and the open source community_

