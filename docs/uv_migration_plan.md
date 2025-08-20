# UV Migration Plan: mise-task-tools

## Executive Summary

This document outlines the complete migration strategy from the current hatchling-based build system to UV (Ultra-fast Python package manager) for the mise-task-tools MCP server project.

## Current State Analysis

### Existing Configuration
- **Build Backend**: hatchling  
- **Python Version**: 3.11.13 (meets UV requirements >=3.9)
- **Package Management**: pip-based dependencies
- **Project Structure**: Standard Python package with pyproject.toml
- **Dependencies**: 6 core + 5 dev dependencies
- **UV Availability**: ✅ Installed via mise (v0.7.19)

### Current pyproject.toml Structure
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mise-task-tools"
version = "0.1.0"
# ... standard project metadata
```

## Migration Strategy

### Phase 1: UV Project Initialization

#### 1.1 Install UV Dependencies (if needed)
```bash
# UV is already available via mise at:
# /home/delorenj/.local/share/mise/installs/uv/0.7.19/uv-x86_64-unknown-linux-musl/uv
```

#### 1.2 Initialize UV Project
```bash
cd /home/delorenj/code/mcp/mise-task-tools
uv init --no-readme --no-gitignore --build-backend uv
```

#### 1.3 Migration Decision Matrix

| Current Tool | UV Replacement | Action Required |
|--------------|----------------|----------------|
| pip install | uv add | Replace installation commands |
| pip freeze | uv lock | Use UV lock file instead |
| venv creation | uv venv | UV handles automatically |
| Build system | hatchling → uv_build | Update pyproject.toml |
| Dependency resolution | pip resolver | UV's faster resolver |

### Phase 2: Build System Migration

#### 2.1 Updated pyproject.toml Configuration

**Option A: Keep Hatchling (Conservative)**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mise-task-tools"
version = "0.1.0"
description = "MCP server for intelligent mise task management and organization"
authors = [{name = "Jarad DeLorenzo", email = "jarad@delorenzo.dev"}]
requires-python = ">=3.9"
dependencies = [
    "fastmcp>=0.3.0",
    "pydantic>=2.0.0",
    "tomli>=2.0.0",
    "tomli-w>=1.0.0",
    "pathlib>=1.0.0",
    "typing-extensions>=4.0.0",
    "glob2>=0.7",
    "networkx>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

# UV-specific configuration
[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

[tool.uv.workspace]
members = ["mise_task_tools"]

[tool.black]
line-length = 100
target-version = ['py39']

[tool.ruff]
line-length = 100
target-version = "py39"

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**Option B: Full UV Build Backend (Aggressive)**
```toml
[build-system]
requires = ["uv_build>=0.8.12,<0.9.0"]
build-backend = "uv_build"

# ... rest same as Option A
```

#### 2.2 UV Lock File Generation
The migration will create `uv.lock` which provides:
- **Deterministic builds**: Exact version locking
- **Cross-platform compatibility**: Platform-specific locks
- **Faster resolution**: UV's Rust-based resolver
- **Better conflict detection**: Advanced dependency analysis

### Phase 3: Dependency Management Migration

#### 3.1 Dependency Installation Commands

**Current (pip-based)**:
```bash
pip install -e .
pip install -e ".[dev]"
```

**New (UV-based)**:
```bash
uv sync                    # Install all dependencies
uv sync --extra dev        # Install with dev dependencies
uv add <package>          # Add new dependency
uv add --dev <package>    # Add dev dependency
uv remove <package>       # Remove dependency
```

#### 3.2 Development Workflow Changes

| Task | Current Command | New UV Command |
|------|----------------|----------------|
| Install deps | `pip install -e .` | `uv sync` |
| Add dependency | Manual pyproject.toml edit | `uv add package` |
| Create venv | `python -m venv venv` | `uv venv` (automatic) |
| Run script | `python script.py` | `uv run script.py` |
| Run tests | `pytest` | `uv run pytest` |
| Build package | `pip wheel .` | `uv build` |

### Phase 4: MCP Server Integration

#### 4.1 MCP Client Configuration Updates

**Current Configuration**:
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

**UV-Enhanced Configuration**:
```json
{
  "mcpServers": {
    "mise-task-tools": {
      "command": "uv",
      "args": ["run", "python", "-m", "mise_task_tools"],
      "cwd": "/home/delorenj/code/mcp/mise-task-tools"
    }
  }
}
```

#### 4.2 Alternative MCP Execution Methods

**Option 1: Direct Python Execution (maintains compatibility)**
```json
{
  "mcpServers": {
    "mise-task-tools": {
      "command": "python",
      "args": ["-m", "mise_task_tools"],
      "cwd": "/home/delorenj/code/mcp/mise-task-tools",
      "env": {
        "UV_PROJECT_ENVIRONMENT": "/home/delorenj/code/mcp/mise-task-tools/.venv"
      }
    }
  }
}
```

**Option 2: UV Run Wrapper Script**
Create `run_mcp_server.sh`:
```bash
#!/bin/bash
cd /home/delorenj/code/mcp/mise-task-tools
exec uv run python -m mise_task_tools "$@"
```

### Phase 5: Performance Optimizations

#### 5.1 Expected Performance Improvements
- **Installation Speed**: 10-100x faster than pip
- **Dependency Resolution**: Rust-based resolver
- **Lock File Updates**: Incremental updates
- **Parallel Downloads**: Concurrent package fetching
- **Memory Usage**: Reduced memory footprint

#### 5.2 UV-Specific Optimizations

```toml
[tool.uv]
# Cache management
cache-dir = ".uv-cache"
no-cache = false

# Resolution strategy
resolution = "highest"  # or "lowest-direct"

# Build configuration
compile-bytecode = true
no-sources = false

# Index configuration
index-url = "https://pypi.org/simple"
extra-index-url = []

# Workspace configuration
workspace = true
```

### Phase 6: CI/CD Integration

#### 6.1 GitHub Actions Updates

**Current CI/CD** (if exists):
```yaml
- name: Install dependencies
  run: |
    pip install -e .
    pip install -e ".[dev]"
```

**UV-Enhanced CI/CD**:
```yaml
- name: Set up uv
  uses: astral-sh/setup-uv@v2
  with:
    version: "latest"

- name: Install dependencies
  run: uv sync --extra dev

- name: Run tests
  run: uv run pytest

- name: Build package
  run: uv build
```

#### 6.2 Caching Strategy
```yaml
- name: Cache uv dependencies
  uses: actions/cache@v4
  with:
    path: |
      ~/.cache/uv
      .venv
    key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}
    restore-keys: |
      ${{ runner.os }}-uv-
```

## Migration Timeline

### Immediate Actions (Day 1)
1. ✅ **System Check**: Verify UV installation (completed)
2. 🔄 **Backup Current State**: Create git branch for migration
3. 🔄 **Initialize UV Project**: Run `uv init` with appropriate flags
4. 🔄 **Update pyproject.toml**: Choose conservative (hatchling) or aggressive (uv_build) approach

### Short Term (Days 2-3)
1. 🔄 **Generate uv.lock**: Create lock file with `uv lock`
2. 🔄 **Test Dependencies**: Verify all packages install correctly
3. 🔄 **Update Documentation**: Reflect new installation procedures
4. 🔄 **Test MCP Integration**: Ensure server still functions properly

### Medium Term (Week 1)
1. 🔄 **Performance Testing**: Benchmark installation/build times
2. 🔄 **CI/CD Updates**: Migrate automated workflows
3. 🔄 **Developer Guidelines**: Update contribution instructions
4. 🔄 **Rollback Plan**: Document reversion procedure if needed

## Risk Assessment

### Low Risk ✅
- **Dependency Management**: UV maintains pip compatibility
- **Python Compatibility**: Project already uses Python 3.11
- **MCP Server Function**: Core functionality unchanged

### Medium Risk ⚠️
- **Build Backend Change**: If switching from hatchling to uv_build
- **Developer Workflow**: Team adaptation to new commands
- **CI/CD Integration**: Pipeline modifications required

### High Risk 🚨
- **Lock File Conflicts**: Potential dependency resolution differences
- **Environment Isolation**: UV environment vs existing setups
- **Production Deployment**: Changes to deployment procedures

## Rollback Strategy

### Emergency Rollback Steps
1. **Revert pyproject.toml**: Restore original hatchling configuration
2. **Remove UV Files**: Delete `uv.lock` and `.venv` directories
3. **Reinstall with pip**: `pip install -e ".[dev]"`
4. **Test Functionality**: Verify MCP server operates normally

### Rollback Triggers
- MCP server fails to start after migration
- Critical dependency conflicts arise
- Significant performance degradation
- Team productivity severely impacted

## Success Metrics

### Performance Targets
- **Installation Speed**: >5x improvement over pip
- **Build Time**: Maintain or improve current build performance
- **Lock File Updates**: <10 seconds for dependency changes
- **CI/CD Runtime**: Reduce pipeline execution time by 30%+

### Functionality Validation
- ✅ MCP server starts without errors
- ✅ All tools function correctly
- ✅ Development workflow maintains efficiency
- ✅ Dependencies resolve without conflicts

## Recommendations

### Primary Recommendation: Conservative Migration
1. **Keep hatchling** as build backend initially
2. **Use UV for dependency management** only
3. **Gradual adoption** of UV-specific features
4. **Monitor performance** and stability for 1-2 weeks
5. **Consider uv_build** migration after validation

### Secondary Options
1. **Full UV Migration**: For teams comfortable with bleeding edge
2. **Hybrid Approach**: UV for development, pip for production
3. **Delayed Migration**: Wait for UV 1.0 stable release

## Next Steps

1. **Execute Phase 1**: Initialize UV project structure
2. **Test Dependencies**: Verify all packages install via UV
3. **Update Documentation**: Reflect new procedures
4. **Monitor Performance**: Track installation and build times
5. **Team Training**: Update development workflows

---

**Migration Champion**: UV Converter Agent  
**Last Updated**: 2025-08-19  
**Status**: Ready for Implementation  
**Risk Level**: Low-Medium  
**Estimated Effort**: 2-3 days initial, 1 week total validation