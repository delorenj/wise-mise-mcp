# 🚀 Getting Started with Wise Mise

> **Transform your development workflow in under 5 minutes**

Welcome to Wise Mise! This guide will get you up and running with intelligent mise task management, from installation to advanced usage patterns. Whether you're new to mise or a power user looking to optimize your workflows, this guide has you covered.

---

## 🎯 **What You'll Learn**

- **Quick Setup**: Install Wise Mise and run your first analysis.
- **CLI Usage**: Master the `analyze` command for instant insights.
- **MCP Server**: Learn how to run Wise Mise as an MCP server for your favorite client.
- **Task Creation**: Create intelligent tasks that follow best practices.
- **Workflow Integration**: Seamlessly integrate with your existing development process.

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
# Install Wise Mise globally
uv tool install wise-mise

# Verify installation
wise-mise --version
```

### Method 2: Traditional pip

```bash
# Install with pip
pip install wise-mise

# Verify installation  
wise-mise --version
```

### Method 3: Development Installation

```bash
# Clone the repository
git clone https://github.com/delorenj/wise-mise
cd wise-mise

# Install with UV (recommended)
uv sync

# Or with pip
pip install -e ".[dev]"

# Run tests to ensure everything works
uv run pytest --tb=short
```

---

## 🔧 **MCP Server Configuration**

To use Wise Mise as an MCP server, you'll need to configure your client.

### Claude Desktop Setup

Add Wise Mise to your Claude Desktop configuration:

**Location**: 
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

**Configuration**:
```json
{
  "mcpServers": {
    "wise-mise": {
      "command": "wise-mise",
      "args": ["server"],
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

Let's verify everything is working correctly.

### CLI Health Check
The easiest way to check the health of your installation and environment is to use the (planned) `doctor` command:
```bash
wise-mise doctor
```

### MCP Server Health Check
If you are running the MCP server, you can check its health from your client:

**In your MCP client (like Claude Desktop):**

```
Check the health of the Wise Mise server
```

You should see a comprehensive health report showing:
- ✅ Server status: healthy
- ✅ All dependencies available
- ✅ Core features operational
- ✅ Project analysis capabilities ready

If you see any issues, check the [Troubleshooting](#troubleshooting) section below.

---

## 🎯 **Your First Project Analysis**

Now for the exciting part! Let's analyze your first project using the CLI.

### Step 1: Navigate to Your Project

Open your terminal and navigate to a project directory. Any project will work, but these types show the best results:

- **Node.js/TypeScript** projects (React, Next.js, etc.)
- **Python** projects (FastAPI, Django, etc.)
- **Rust** projects (CLI tools, web services)
- **Multi-language** projects

### Step 2: Analyze Project Structure

Run the `analyze` command:
```bash
wise-mise analyze .
```

The system will automatically:
1. **Detect your technology stack** (languages, frameworks, tools)
2. **Analyze existing tasks** (if any)
3. **Recommend optimized tasks** based on best practices
4. **Output a JSON with the analysis** that you can inspect or pipe to other tools.

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

While the CLI provides analysis, task creation is currently handled by the MCP server.

### Using the MCP Server to Create Tasks

Once you have the server running and connected to your client, you can create tasks using natural language.

**In your MCP client:**

```
Create the top 3 highest-priority tasks from the recommendations
```

This will automatically:
1. Create tasks with optimal domain organization
2. Set up proper dependencies between tasks
3. Configure source/output tracking for performance
4. Generate appropriate descriptions and documentation

**Create a specific task:**

```
Create a task to run TypeScript type checking in watch mode for development
```

---

## 📊 **Understanding Task Architecture**

Wise Mise organizes tasks using a hierarchical domain system:

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

**Symptoms**: MCP client can't connect to Wise Mise
**Solutions**:
1. Check that `wise-mise` is in your PATH.
2. Verify the working directory in your MCP config.
3. Try running the server manually: `wise-mise server`

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
1. Reinstall with `uv sync` or `pip install wise-mise`
2. Check Python environment is activated
3. Verify all system requirements are met

### Debug Mode

For detailed troubleshooting:

```bash
# Run server with verbose logging
wise-mise server --verbose

# Check server health
wise-mise server --health-check
```

### Getting Help

1. **Check the health report** first using the `get_server_health` tool
2. **Review logs** in your MCP client's debug output
3. **Create an issue** on [GitHub](https://github.com/delorenj/wise-mise/issues) with:
   - Health check output
   - Project structure (if possible)
   - MCP client configuration
   - Error messages or unexpected behavior

---

## 🎯 **Next Steps**

Now that you're set up with Wise Mise, explore these areas:

### 📚 **Learn More**
- [API Reference](./API.md) - Complete tool documentation
- [Contributing Guide](./CONTRIBUTING.md) - Help improve the project
- [Best Practices](./BEST_PRACTICES.md) - Advanced patterns and tips

### 🛠️ **Customize**
- Add domain-specific experts for your tech stack
- Create custom task templates for your team
- Integrate with your CI/CD pipeline

### 🤝 **Connect**
- Join our [GitHub Discussions](https://github.com/delorenj/wise-mise/discussions)
- Follow [@WiseMise](https://twitter.com/WiseMise) for tips and updates
- Share your success stories and use cases

---

## 🎉 **You're Ready!**

Congratulations! You now have Wise Mise set up and understand how to:

- ✅ **Analyze projects** for optimal task recommendations
- ✅ **Create intelligent tasks** using the MCP server
- ✅ **Understand task architecture** and dependencies
- ✅ **Validate and optimize** your configuration
- ✅ **Troubleshoot issues** when they arise

**Welcome to the future of intelligent task management!** 🚀

Your development workflow will never be the same. Enjoy building amazing things with Wise Mise!

---

*Questions? Need help? We're here for you in [GitHub Discussions](https://github.com/delorenj/wise-mise/discussions)!*