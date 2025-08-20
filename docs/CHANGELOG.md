# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial open source release as "wise-mise-mcp"
- Comprehensive README with examples and documentation
- Contributing guidelines and code of conduct
- MIT license for open source distribution
- GitHub Actions CI/CD pipeline
- UV package manager support
- Professional project structure and documentation

### Changed
- Project renamed from "mise-task-tools" to "wise-mise-mcp"
- Updated Python requirement to >=3.10 (FastMCP compatibility)
- Enhanced project description and branding
- Improved package metadata and dependencies

### Technical
- Migrated to UV for dependency management
- Added comprehensive test coverage requirements
- Implemented automated release pipeline
- Added security scanning and quality gates
- Enhanced development workflow with pre-commit hooks

## [0.1.0] - 2025-08-19

### Added
- Initial implementation of intelligent mise task management
- Domain expert system for 10+ technology domains
- MCP server with 6 core tools for task analysis and management
- Support for hierarchical task organization
- Dependency graph analysis and optimization
- Project structure analysis and task suggestions
- Task pruning and architecture validation
- Integration with FastMCP framework

### Core Tools
- `analyze_project_for_tasks` - Extract strategic tasks from project structure
- `trace_task_chain` - Analyze task dependencies and execution flow
- `create_task` - Intelligently add new tasks with proper organization
- `prune_tasks` - Remove outdated or redundant tasks
- `validate_task_architecture` - Ensure configuration follows best practices
- `get_task_recommendations` - Get suggestions for optimization

### Domain Experts
- BuildExpert - Frontend/Backend build systems
- TestExpert - Testing frameworks and strategies
- LintExpert - Code quality and static analysis
- DevExpert - Development workflow optimization
- DeployExpert - CI/CD and deployment automation
- DbExpert - Database operations and migrations
- CiExpert - Continuous integration optimization
- DocsExpert - Documentation generation
- CleanExpert - Cleanup and maintenance tasks
- SetupExpert - Project initialization and setup

---

## Release Notes Format

Each release follows this structure:

### Added
- New features and capabilities

### Changed
- Changes to existing functionality

### Deprecated
- Features marked for removal

### Removed
- Features removed in this version

### Fixed
- Bug fixes and corrections

### Security
- Security-related changes and improvements

---

*For the complete history, see [GitHub Releases](https://github.com/delorenj/wise-mise-mcp/releases)*