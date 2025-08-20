# Contributing to Wise Mise MCP

Thank you for your interest in contributing to Wise Mise MCP! This project thrives on community contributions, and we're excited to see what you'll bring to the table.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- [UV](https://docs.astral.sh/uv/) (recommended) or pip
- Git
- A curious mind and willingness to experiment!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/delorenj/wise-mise-mcp
cd wise-mise-mcp

# Install with UV (recommended)
uv sync

# Or with pip
pip install -e ".[dev]"

# Verify installation
uv run python -m wise_mise_mcp --help
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=wise_mise_mcp --cov-report=html

# Run specific test categories
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest -m "not slow"  # Skip slow tests
```

### Code Quality

We maintain high code quality standards:

```bash
# Format code
uv run black .

# Lint and fix issues
uv run ruff check --fix .

# Type checking
uv run mypy wise_mise_mcp/

# Run all quality checks
uv run pytest && uv run black --check . && uv run ruff check . && uv run mypy wise_mise_mcp/
```

## 🎯 How to Contribute

### 1. Finding Something to Work On

**Good First Issues**: Look for issues labeled `good first issue` or `help wanted`

**Domain Experts**: Each technology domain (build, test, lint, etc.) can always use more expert knowledge

**Documentation**: We value clear, helpful documentation as much as code

**Testing**: More test coverage, especially integration tests with real-world projects

### 2. Types of Contributions We Love

#### 🧠 **Domain Expertise**
Add or improve domain experts for specific technologies:

```python
class RustExpert(DomainExpert):
    """Expert in Rust build systems and tooling."""
    
    def analyze_tasks(self, project: ProjectStructure) -> List[TaskDefinition]:
        # Your expertise here!
```

#### 🔧 **Tool Improvements**
Enhance existing MCP tools or add new ones:

```python
@app.tool()
async def my_new_tool(request: MyRequest) -> MyResponse:
    """A helpful new tool for mise task management."""
    # Your innovation here!
```

#### 📚 **Documentation & Examples**
- Real-world usage examples
- Tutorial improvements
- API documentation
- Video guides or demos

#### 🧪 **Testing & Quality**
- Edge case testing
- Performance benchmarks
- Cross-platform compatibility
- Integration test scenarios

### 3. The Contribution Process

1. **Fork & Clone**: Fork the repo and clone your fork
2. **Create Branch**: `git checkout -b feature/my-awesome-feature`
3. **Develop**: Make your changes with tests
4. **Test**: Ensure all tests pass and quality checks succeed
5. **Commit**: Use descriptive commit messages
6. **Push**: Push to your fork
7. **Pull Request**: Open a PR with a clear description

### Commit Message Style

We follow conventional commits:

```
feat: add Rust build system expert
fix: handle missing mise.toml gracefully
docs: update API examples for v0.2.0
test: add integration tests for Node.js projects
refactor: simplify task dependency resolution
```

## 🏗️ Architecture Overview

Understanding the codebase helps you contribute effectively:

### Core Components

```
wise_mise_mcp/
├── server.py          # FastMCP server and tool definitions
├── models.py          # Core data models (TaskDefinition, etc.)
├── analyzer.py        # Project analysis and dependency graphs
├── manager.py         # Task creation and configuration management
├── experts.py         # Domain expert implementations
└── additional_experts.py  # Extended domain experts
```

### Key Concepts

**Domain Experts**: Classes that understand specific technology stacks and can suggest appropriate mise tasks.

**Task Definitions**: Structured representations of mise tasks with metadata like complexity, dependencies, and domain.

**Project Analysis**: The process of examining a project's structure to understand its technology stack and suggest relevant tasks.

**Dependency Graphs**: NetworkX-based representation of task relationships for optimization and validation.

## 🎨 Code Style Guide

### Python Style

We follow PEP 8 with some modifications:

- **Line Length**: 100 characters (not 79)
- **String Quotes**: Prefer double quotes for strings
- **Type Hints**: Required for all public APIs
- **Docstrings**: Google-style docstrings for all public functions

### Example Code Style

```python
from typing import List, Optional
from pathlib import Path

from .models import TaskDefinition, TaskDomain


class MyExpert:
    """Expert for analyzing my technology stack.
    
    This expert specializes in detecting and creating tasks for
    my specific technology or framework.
    """
    
    def analyze_project(self, project_path: Path) -> List[TaskDefinition]:
        """Analyze project and suggest appropriate tasks.
        
        Args:
            project_path: Path to the project root directory.
            
        Returns:
            List of suggested task definitions.
            
        Raises:
            AnalysisError: If project analysis fails.
        """
        # Implementation here
        pass
```

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/              # Fast, isolated unit tests
├── integration/       # Tests with real projects
├── fixtures/          # Test data and project samples
└── conftest.py        # Pytest configuration
```

### Writing Good Tests

```python
import pytest
from pathlib import Path

from wise_mise_mcp.experts import BuildExpert
from wise_mise_mcp.models import TaskDomain


class TestBuildExpert:
    """Test the BuildExpert domain expert."""
    
    def test_detects_nodejs_project(self, nodejs_project_fixture):
        """Should detect Node.js projects and suggest build tasks."""
        expert = BuildExpert()
        tasks = expert.analyze_project(nodejs_project_fixture)
        
        assert any(task.domain == TaskDomain.BUILD for task in tasks)
        assert any("npm run build" in task.run for task in tasks)
    
    @pytest.mark.integration
    def test_real_world_project(self, tmp_path):
        """Integration test with a real project structure."""
        # Set up real project structure
        # Test actual behavior
```

### Test Categories

Use pytest markers to categorize tests:

```python
@pytest.mark.unit
def test_fast_unit_test():
    pass

@pytest.mark.integration  
def test_integration_with_real_project():
    pass

@pytest.mark.slow
def test_expensive_operation():
    pass
```

## 📝 Documentation

### Code Documentation

- **Public APIs**: Comprehensive docstrings with examples
- **Complex Logic**: Inline comments explaining the "why"
- **Type Hints**: Use for all parameters and return values

### User Documentation

- **README**: Keep the main README focused and engaging
- **API Docs**: Detailed tool documentation with examples
- **Tutorials**: Step-by-step guides for common use cases
- **Architecture**: Document design decisions and patterns

## 🤝 Community Guidelines

### Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/). In summary:

- **Be Respectful**: Treat everyone with kindness and respect
- **Be Inclusive**: Welcome contributors from all backgrounds
- **Be Constructive**: Provide helpful feedback and suggestions
- **Be Patient**: Remember everyone is learning and growing

### Communication

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and community chat
- **Pull Requests**: For code review and collaboration

### Getting Help

Stuck? We're here to help!

1. **Check Documentation**: Start with the README and docs
2. **Search Issues**: Someone might have faced the same problem
3. **Ask Questions**: Open a GitHub Discussion
4. **Join the Community**: We're friendly and welcoming!

## 🎉 Recognition

Contributors are recognized in several ways:

- **Contributors List**: Listed in README and release notes
- **Hall of Fame**: Special recognition for significant contributions
- **Maintainer Status**: Long-term contributors may become maintainers
- **Speaking Opportunities**: Conference talks and blog posts

## 📋 Development Workflow

### Branch Strategy

- **main**: Stable release branch
- **develop**: Integration branch for new features
- **feature/***: Feature development branches
- **hotfix/***: Critical bug fixes

### Release Process

1. **Feature Freeze**: Stop adding new features
2. **Testing**: Comprehensive testing and QA
3. **Documentation**: Update docs and changelog
4. **Release**: Tag and publish to PyPI
5. **Post-Release**: Monitor for issues and gather feedback

## 🔮 Roadmap & Vision

### Short Term (Next 3 months)
- Enhanced domain experts for popular frameworks
- Performance optimizations
- Better error handling and user feedback

### Medium Term (6 months)
- Plugin system for custom domain experts
- Visual task dependency graphs
- Integration with more MCP clients

### Long Term (1 year+)
- AI-powered task optimization suggestions
- Cloud-based project analysis
- Enterprise features and support

---

## Questions?

Don't hesitate to reach out! We're excited to work with you and make Wise Mise MCP even better.

**Happy Contributing!** 🎉

*The Wise Mise MCP Team*