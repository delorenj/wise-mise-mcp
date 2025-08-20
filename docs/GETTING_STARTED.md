# 🚀 Getting Started with Wise Mise MCP

> **Transform your development workflow in under 5 minutes**

Welcome to Wise Mise MCP! This guide will get you up and running with intelligent mise task management, from installation to advanced usage patterns. Whether you're new to mise or a power user looking to optimize your workflows, this guide has you covered.

---

## 🎯 **What You'll Learn**

- **Quick Setup**: Install and configure Wise Mise MCP in your environment
- **First Analysis**: Understand what your project needs for optimal task management
- **Task Creation**: Create intelligent tasks that follow best practices
- **Workflow Integration**: Seamlessly integrate with your existing development process
- **Advanced Patterns**: Leverage expert features for complex projects

---

## 📋 **Prerequisites**

Before starting, ensure you have:

- **Python 3.9+** (3.11+ recommended for best performance)
- **mise installed** ([mise.jdx.dev](https://mise.jdx.dev/))
- **MCP-compatible client** (Claude Desktop, Continue, etc.)
- **UV package manager** (recommended) or pip

### Installing Prerequisites

```bash
# Install mise (if not already installed)
curl https://mise.jdx.dev/install.sh | sh

# Install UV (recommended for fast package management)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installations
mise --version
uv --version
python --version
```

---

## ⚡ **Installation**

### Method 1: UV (Recommended)

```bash
# Install Wise Mise MCP with UV
uv add wise-mise-mcp

# Or install globally
uv tool install wise-mise-mcp

# Verify installation
uv run python -m wise_mise_mcp --version
```

### Method 2: Traditional pip

```bash
# Install with pip
pip install wise-mise-mcp

# Verify installation  
python -m wise_mise_mcp --version
```

### Method 3: Development Installation

```bash
# Clone the repository
git clone https://github.com/delorenj/wise-mise-mcp
cd wise-mise-mcp

# Install with UV (recommended)
uv sync

# Or with pip
pip install -e ".[dev]"

# Run tests to ensure everything works
uv run pytest --tb=short
```

---

## 🔧 **MCP Client Configuration**

### Claude Desktop Setup

Add Wise Mise MCP to your Claude Desktop configuration:

**Location**: 
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

**Configuration**:
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

**Alternative Configuration** (without UV):
```json
{
  "mcpServers": {
    "wise-mise-mcp": {
      "command": "python",
      "args": ["-m", "wise_mise_mcp"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

### Other MCP Clients

For other MCP-compatible clients, use similar configuration patterns. The key is:
- **Command**: Path to Python or UV
- **Args**: Module invocation arguments
- **Working Directory**: Your project root

---

## 🧪 **Health Check**

Let's verify everything is working correctly:

**In your MCP client (like Claude Desktop):**

```
Check the health of the Wise Mise MCP server
```

You should see a comprehensive health report showing:
- ✅ Server status: healthy
- ✅ All dependencies available
- ✅ Core features operational
- ✅ Project analysis capabilities ready

If you see any issues, check the [Troubleshooting](#troubleshooting) section below.

---

## 🎯 **Your First Project Analysis**

Now for the exciting part! Let's analyze your first project.

### Step 1: Navigate to Your Project

Open your MCP client and navigate to a project directory. Any project will work, but these types show the best results:

- **Node.js/TypeScript** projects (React, Next.js, etc.)
- **Python** projects (FastAPI, Django, etc.)
- **Rust** projects (CLI tools, web services)
- **Multi-language** projects

### Step 2: Analyze Project Structure

**In your MCP client:**

```
Analyze my current project for intelligent task recommendations
```

The system will automatically:
1. **Detect your technology stack** (languages, frameworks, tools)
2. **Analyze existing tasks** (if any)
3. **Recommend optimized tasks** based on best practices
4. **Prioritize recommendations** by impact and effort

### Example Output

```
🎯 Project Analysis Complete!

📊 Detected Technology Stack:
  • Languages: TypeScript, JavaScript
  • Frameworks: Next.js, React
  • Package Managers: npm
  • Testing: Jest detected
  • Build Tools: Next.js built-in

📋 Task Recommendations (8 found):

🔴 HIGH PRIORITY (Priority 9-10):
  1. dev - Start development server with hot reloading
  2. build:prod - Create optimized production build
  3. test:unit - Run Jest unit tests

🟡 MEDIUM PRIORITY (Priority 6-8):
  4. lint:code - ESLint code quality checks
  5. lint:types - TypeScript type checking
  6. test:e2e - End-to-end testing setup

🟢 LOW PRIORITY (Priority 4-5):
  7. clean - Clean build artifacts and cache
  8. docs:build - Generate documentation
```

### Step 3: Understand the Recommendations

Each recommendation includes:
- **Domain Classification**: Where the task belongs (build, test, lint, etc.)
- **Reasoning**: Why this task is recommended for your stack
- **Priority Score**: How important this task is (1-10 scale)
- **Effort Estimate**: Time/complexity to implement
- **Suggested Implementation**: Actual command and configuration

---

## 🛠️ **Creating Your First Tasks**

Now let's create some tasks! Wise Mise MCP makes this incredibly easy.

### Method 1: High-Priority Batch Creation

**In your MCP client:**

```
Create the top 3 highest-priority tasks from the recommendations
```

This will automatically:
1. Create tasks with optimal domain organization
2. Set up proper dependencies between tasks
3. Configure source/output tracking for performance
4. Generate appropriate descriptions and documentation

### Method 2: Individual Task Creation

**Create a specific task:**

```
Create a task to run TypeScript type checking in watch mode for development
```

**Example response:**
```
✅ Created Task: lint:types:watch

📍 Placement: .mise.toml (simple task)
🔧 Configuration:
  [tasks.lint.types.watch]
  description = "TypeScript type checking in watch mode for development"
  run = "tsc --noEmit --watch"
  sources = ["src/**/*.ts", "src/**/*.tsx", "tsconfig.json"]

💡 Reasoning: TypeScript watch mode provides continuous type checking 
during development, catching type errors early without manual intervention.

🔗 Integration: This task complements the existing build:dev task and can 
run in parallel for enhanced development experience.
```

### Method 3: Natural Language Task Creation

Describe what you want in plain English:

```
I need a task that builds my React components library, runs tests, 
and creates a distribution bundle ready for NPM publishing
```

The system will:
1. **Analyze the complexity** (this requires multiple steps)
2. **Choose appropriate domain** (likely `build:lib` or `publish:prepare`)
3. **Create a file-based task** (for complex multi-step operations)
4. **Set up dependencies** (test must pass before building)
5. **Configure outputs** (dist folder, package files)

---

## 📊 **Understanding Task Architecture**

Wise Mise MCP organizes tasks using a hierarchical domain system:

### Core Domains

```
📁 build/     - Compilation, bundling, asset processing
├── build:dev     - Development builds with hot reloading
├── build:prod    - Production-optimized builds
└── build:lib     - Library/package builds

📁 test/      - All testing variants
├── test:unit     - Unit tests (fast, isolated)
├── test:integration - Integration tests
└── test:e2e      - End-to-end testing

📁 lint/      - Code quality and formatting
├── lint:code     - ESLint, Prettier, etc.
├── lint:types    - TypeScript, type checking
└── lint:security - Security vulnerability scanning

📁 dev/       - Development workflow tasks
├── dev:server    - Local development server
├── dev:db        - Database setup/reset
└── dev:watch     - File watching and auto-reload

📁 deploy/    - Deployment and infrastructure
├── deploy:staging - Staging environment deployment
├── deploy:prod   - Production deployment
└── deploy:docker - Container builds and pushes

📁 db/        - Database operations
├── db:migrate    - Run database migrations
├── db:seed       - Seed with test data
└── db:reset      - Reset database to clean state
```

### Why This Organization Matters

1. **Discoverability**: Easy to find related tasks
2. **Dependency Management**: Clear execution order
3. **Parallel Execution**: Independent domains can run simultaneously
4. **Scalability**: New tasks fit naturally into existing structure
5. **Team Consistency**: Everyone follows the same patterns

---

## 🔍 **Analyzing Task Dependencies**

Understanding how tasks relate to each other is crucial for optimization.

### Trace a Task Chain

**In your MCP client:**

```
Show me the complete execution chain for deploying to production
```

**Example output:**
```
🕸️ Task Chain Analysis: deploy:prod

📋 Execution Flow:
Step 1 (Parallel):
  • lint:code - Code quality checks
  • lint:types - TypeScript validation
  • test:unit - Unit test suite

Step 2 (Sequential):
  • test:integration - Integration tests
  
Step 3 (Sequential):
  • build:prod - Production build

Step 4 (Sequential):  
  • deploy:prod - Deploy to production

⏱️ Estimated Time: 4-6 minutes
🎯 Critical Path: test:integration → build:prod → deploy:prod

🔧 Optimization Opportunities:
  • Steps 1 can run in parallel (saves ~2 minutes)
  • Consider caching build artifacts
  • Integration tests could be optimized
```

This analysis helps you:
- **Identify bottlenecks** in your workflow
- **Optimize for parallel execution**
- **Understand dependencies** and their purposes
- **Estimate execution times** for planning

---

## ✅ **Validating Your Configuration**

Regular validation ensures your task setup follows best practices.

### Run Architecture Validation

**In your MCP client:**

```
Validate the architecture and health of my mise task configuration
```

**Example output:**
```
🏥 Architecture Health Report

📊 Overall Health: ✅ Excellent
📈 Total Tasks: 12 across 6 domains
🎯 Organization Score: 9/10

✅ Strengths:
  • Clear domain organization
  • No circular dependencies  
  • Good source/output tracking
  • Comprehensive test coverage tasks

⚠️ Recommendations:
  • Consider adding deploy:staging task
  • Missing documentation generation tasks
  • Some tasks could benefit from parallel execution

🔧 Performance Optimizations Available:
  • 3 tasks could use source tracking for faster builds
  • 2 opportunities for parallel execution
```

---

## 🚀 **Advanced Patterns**

Once you're comfortable with the basics, explore these advanced patterns:

### 1. Environment-Specific Tasks

Create tasks for different environments:

```
Create tasks for staging and production deployments with environment-specific configurations
```

### 2. Monorepo Support

For monorepos or multi-package projects:

```
Analyze this monorepo and create tasks that handle multiple packages efficiently
```

### 3. CI/CD Integration

Optimize for continuous integration:

```
Create CI-optimized tasks that leverage caching and parallel execution for GitHub Actions
```

### 4. Custom Domain Experts

If you work with specialized technologies:

```
I'm using [specific framework/tool]. Can you analyze and create appropriate task patterns?
```

---

## 🧹 **Maintenance and Optimization**

Keep your task configuration clean and efficient:

### Regular Cleanup

```
Analyze my task configuration for redundant or outdated tasks
```

### Performance Optimization

```
Get recommendations for optimizing my task architecture and improving build performance
```

### Strategic Planning

```
What new tasks should I consider adding to improve my development workflow?
```

---

## 🔧 **Troubleshooting**

### Common Issues

#### "Server Not Responding"

**Symptoms**: MCP client can't connect to Wise Mise MCP
**Solutions**:
1. Check that Python/UV is in your PATH
2. Verify the working directory in your MCP config
3. Try running the server manually: `python -m wise_mise_mcp`

#### "No Tasks Found" 

**Symptoms**: Analysis returns empty results
**Solutions**:
1. Ensure you're in a project directory
2. Check that project files are readable
3. Try with a simple Node.js or Python project first

#### "Permission Errors"

**Symptoms**: Cannot create or modify .mise.toml
**Solutions**:
1. Check file permissions in the project directory
2. Ensure the working directory in MCP config is correct
3. Run with appropriate user permissions

#### "Dependency Missing"

**Symptoms**: Health check shows missing dependencies
**Solutions**:
1. Reinstall with `uv sync` or `pip install wise-mise-mcp`
2. Check Python environment is activated
3. Verify all system requirements are met

### Debug Mode

For detailed troubleshooting:

```bash
# Run server with verbose logging
python -m wise_mise_mcp --debug

# Check server health
python -m wise_mise_mcp --health-check
```

### Getting Help

1. **Check the health report** first using the `get_server_health` tool
2. **Review logs** in your MCP client's debug output
3. **Create an issue** on [GitHub](https://github.com/delorenj/wise-mise-mcp/issues) with:
   - Health check output
   - Project structure (if possible)
   - MCP client configuration
   - Error messages or unexpected behavior

---

## 🎯 **Next Steps**

Now that you're set up with Wise Mise MCP, explore these areas:

### 📚 **Learn More**
- [API Reference](./API.md) - Complete tool documentation
- [Contributing Guide](./CONTRIBUTING.md) - Help improve the project
- [Best Practices](./BEST_PRACTICES.md) - Advanced patterns and tips

### 🛠️ **Customize**
- Add domain-specific experts for your tech stack
- Create custom task templates for your team
- Integrate with your CI/CD pipeline

### 🤝 **Connect**
- Join our [GitHub Discussions](https://github.com/delorenj/wise-mise-mcp/discussions)
- Follow [@WiseMiseMCP](https://twitter.com/WiseMiseMCP) for tips and updates
- Share your success stories and use cases

---

## 🎉 **You're Ready!**

Congratulations! You now have Wise Mise MCP set up and understand how to:

- ✅ **Analyze projects** for optimal task recommendations
- ✅ **Create intelligent tasks** using natural language
- ✅ **Understand task architecture** and dependencies
- ✅ **Validate and optimize** your configuration
- ✅ **Troubleshoot issues** when they arise

**Welcome to the future of intelligent task management!** 🚀

Your development workflow will never be the same. Enjoy building amazing things with Wise Mise MCP!

---

*Questions? Need help? We're here for you in [GitHub Discussions](https://github.com/delorenj/wise-mise-mcp/discussions)!*