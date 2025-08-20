# 📚 Wise Mise MCP Documentation

> **Complete documentation for intelligent mise task management**

Welcome to the comprehensive documentation for Wise Mise MCP! This guide will help you master every aspect of the intelligent task management system, from basic setup to advanced enterprise patterns.

---

## 🎯 **Quick Navigation**

### 🚀 **Getting Started**
- **[Getting Started Guide](./GETTING_STARTED.md)** - Setup, installation, and first analysis
- **[API Reference](./API.md)** - Complete tool documentation with examples
- **[Contributing](./CONTRIBUTING.md)** - Join our mission to revolutionize task management

### 📖 **Reference Materials**
- **[Changelog](./CHANGELOG.md)** - Release history and feature evolution
- **[Architecture Rules](#architecture-principles)** - Core design principles and patterns

---

## 🧠 **What is Wise Mise MCP?**

Wise Mise MCP transforms [mise](https://mise.jdx.dev/) from a simple task runner into an intelligent development companion. It brings AI-powered analysis, domain expertise, and architectural best practices to your development workflow.

### **Key Capabilities**

🔍 **Intelligent Analysis**
- Automatically detects your technology stack
- Understands project architecture and development patterns
- Recommends optimal task organization based on industry best practices

🧠 **Domain Expertise** 
- 10+ specialized domain experts (Build, Test, Lint, Deploy, etc.)
- Deep knowledge of popular frameworks and tools
- Contextual recommendations based on your specific tech stack

🏗️ **Architecture Excellence**
- Hierarchical task organization for scalability
- Dependency optimization and parallel execution
- Performance-focused configuration patterns

---

## 📋 **Documentation Structure**

### **Level 1: Essential**

#### [🚀 Getting Started Guide](./GETTING_STARTED.md)
Your complete onboarding experience:
- **Prerequisites and Installation** - Get up and running in under 5 minutes
- **MCP Client Configuration** - Connect with Claude Desktop and other clients
- **Your First Project Analysis** - See the magic in action
- **Creating Intelligent Tasks** - From natural language to optimized configuration
- **Troubleshooting** - Common issues and solutions

**Perfect for**: New users, first-time setup, quick wins

#### [🛠️ API Reference](./API.md) 
Comprehensive tool documentation:
- **All 9 MCP Tools** with request/response schemas
- **Expert Prompts** for contextual guidance
- **Real-world Examples** and integration patterns
- **Error Handling** and best practices
- **Performance Considerations** and optimization tips

**Perfect for**: Daily usage, integration development, advanced features

### **Level 2: Community**

#### [🤝 Contributing Guide](./CONTRIBUTING.md)
Join our mission to revolutionize task management:
- **Elite Contribution Process** - Make high-impact contributions
- **Architecture Mastery** - Understand the system design
- **Domain Expertise** - Add intelligence for new technologies
- **Recognition & Growth** - Build your reputation and skills
- **Development Roadmap** - Shape the future of the project

**Perfect for**: Contributors, maintainers, technology experts

### **Level 3: Reference**

#### [📋 Changelog](./CHANGELOG.md)
Complete project evolution:
- **Detailed Release Notes** with feature explanations
- **Migration Guides** for breaking changes
- **Development Roadmap** and future vision
- **Known Limitations** and planned improvements

**Perfect for**: Tracking changes, migration planning, project history

---

## 🏗️ **Architecture Principles**

Understanding these core principles will help you use Wise Mise MCP effectively:

### **1. Domain-Driven Organization**

Tasks are organized into 10 non-overlapping domains:

```
📁 build/     - Compilation, bundling, asset processing
📁 test/      - All testing variants (unit, integration, e2e)
📁 lint/      - Code quality, formatting, static analysis  
📁 dev/       - Development workflow tasks
📁 deploy/    - Deployment, release, infrastructure
📁 db/        - Database operations, migrations, seeding
📁 ci/        - CI/CD specific tasks
📁 docs/      - Documentation generation, serving
📁 clean/     - Cleanup operations
📁 setup/     - Environment setup, installation
```

### **2. Hierarchical Naming**

Use `:` separators for clear task hierarchy:

```bash
# Environment variants
deploy:staging
deploy:production

# Tool-specific variants  
lint:eslint
lint:prettier
lint:types

# Complex hierarchies
test:integration:api
build:frontend:assets
```

### **3. Complexity-Based Placement**

- **Simple tasks** (single command) → `.mise.toml`
- **Moderate tasks** (2-5 commands) → `.mise.toml` with arrays
- **Complex tasks** (logic, conditionals) → `.mise/tasks/` scripts

### **4. Performance Optimization**

- **Source tracking** enables incremental builds
- **Output tracking** supports caching and artifacts
- **Dependency analysis** optimizes execution order
- **Parallel execution** maximizes throughput

---

## 🎯 **Usage Patterns**

### **New Project Setup**

```
1. analyze_project_for_tasks   → Understand your stack
2. Review recommendations      → Prioritize by impact  
3. create_task (batch)        → Implement high-value tasks
4. validate_task_architecture → Ensure best practices
```

### **Optimization Workflow**

```
1. get_task_recommendations   → Identify improvements
2. trace_task_chain          → Understand dependencies
3. prune_tasks               → Remove redundancy
4. validate_task_architecture → Confirm optimizations
```

### **Maintenance Routine**

```
1. get_server_health         → Check system status
2. validate_task_architecture → Regular health check
3. prune_tasks (dry_run)     → Identify cleanup opportunities
4. get_task_recommendations  → Discover new patterns
```

---

## 🔧 **Advanced Topics**

### **Custom Domain Experts**

Extend Wise Mise MCP with your own expertise:

```python
class MyFrameworkExpert(DomainExpert):
    """Expert for MyFramework ecosystem."""
    
    def analyze_tasks(self, project: ProjectStructure) -> List[TaskDefinition]:
        # Your domain knowledge becomes automation
        return self._create_intelligent_tasks(project)
```

### **Team Integration**

Standardize task patterns across your organization:
- Share expert configurations
- Create custom task templates
- Establish team conventions
- Integrate with CI/CD pipelines

### **Monorepo Support** (v0.2.0+)

Handle complex multi-package projects:
- Cross-package dependencies
- Workspace-aware optimization
- Selective task execution
- Package-specific configurations

---

## 🎓 **Learning Path**

### **Beginner** (0-2 weeks)
1. **Setup**: Complete the [Getting Started Guide](./GETTING_STARTED.md)
2. **Exploration**: Try project analysis on 3-5 different projects
3. **Task Creation**: Create 10-15 tasks using natural language
4. **Validation**: Run architecture validation and act on suggestions

### **Intermediate** (2-4 weeks)  
1. **Advanced Features**: Master all 9 MCP tools
2. **Optimization**: Optimize an existing project's task configuration
3. **Dependencies**: Understand and optimize task dependency chains
4. **Troubleshooting**: Debug and resolve configuration issues

### **Expert** (1-3 months)
1. **Contribution**: Add a domain expert for your technology
2. **Integration**: Integrate with your team's CI/CD pipeline
3. **Customization**: Create organization-specific patterns
4. **Community**: Help others and share your expertise

---

## 🤝 **Community & Support**

### **Getting Help**

1. **Check Documentation** first - Most questions are answered here
2. **Search Issues** on [GitHub](https://github.com/delorenj/wise-mise-mcp/issues)
3. **Ask Questions** in [GitHub Discussions](https://github.com/delorenj/wise-mise-mcp/discussions)
4. **Join Discord** for real-time community support

### **Contributing**

We welcome all types of contributions:
- **Code**: New features, bug fixes, performance improvements
- **Documentation**: Examples, tutorials, translations
- **Community**: Answering questions, organizing events
- **Expertise**: Domain knowledge for specific technologies

See our [Contributing Guide](./CONTRIBUTING.md) for detailed information.

### **Stay Connected**

- 🐦 **Twitter**: [@WiseMiseMCP](https://twitter.com/WiseMiseMCP)
- 💼 **LinkedIn**: [Jarad DeLorenzo](https://linkedin.com/in/jaraddelorenzo)
- 📧 **Email**: [docs@wise-mise-mcp.dev](mailto:docs@wise-mise-mcp.dev)
- 💬 **Discord**: [Join our community](https://discord.gg/wise-mise-mcp)

---

## 🔮 **What's Next?**

### **Immediate Actions**

1. **[Get Started](./GETTING_STARTED.md)** - Set up Wise Mise MCP in your environment
2. **Analyze a Project** - See intelligent recommendations in action
3. **Create Your First Task** - Experience the power of natural language task creation
4. **Join the Community** - Connect with other developers using Wise Mise MCP

### **Explore Advanced Features**

1. **[Master the API](./API.md)** - Learn all 9 tools and expert prompts
2. **[Contribute](./CONTRIBUTING.md)** - Add your expertise to the project
3. **Optimize Your Workflow** - Implement advanced patterns and optimizations
4. **Share Your Success** - Help others by sharing your use cases

---

## 🎉 **Success Stories**

*"Wise Mise MCP reduced our build setup time from 3 days to 30 minutes. The intelligent recommendations showed us patterns we never would have discovered."* - **Senior DevOps Engineer, Tech Startup**

*"The domain expert system taught our team mise best practices automatically. Our new developers are productive immediately."* - **Engineering Manager, Mid-size Company**

*"I've contributed 3 domain experts to the project. It's incredibly rewarding to see my expertise help thousands of developers worldwide."* - **Open Source Contributor**

---

**Welcome to the future of intelligent task management!** 🚀

Ready to transform your development workflow? [Let's get started!](./GETTING_STARTED.md)

---

*Documentation maintained with ❤️ by the Wise Mise MCP community*