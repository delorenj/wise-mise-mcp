# 🛠️ Wise Mise MCP API Reference

> **Complete reference for all MCP tools, prompts, and capabilities**

This comprehensive API reference covers every tool and capability provided by Wise Mise MCP. Each tool is designed to work seamlessly with MCP-compatible clients like Claude Desktop, providing intelligent mise task management through natural language interactions.

---

## 📋 **Quick Reference**

| Tool | Purpose | Use Case |
|------|---------|----------|
| [`analyze_project_for_tasks`](#analyze_project_for_tasks) | Analyze project structure and recommend tasks | Starting a new project or optimizing existing tasks |
| [`trace_task_chain`](#trace_task_chain) | Map task dependencies and execution flow | Understanding complex workflows and debugging |
| [`create_task`](#create_task) | Intelligently create new mise tasks | Adding tasks with optimal placement and configuration |
| [`validate_task_architecture`](#validate_task_architecture) | Check configuration for best practices | Ensuring your task setup follows optimal patterns |
| [`prune_tasks`](#prune_tasks) | Remove outdated or redundant tasks | Cleaning up and optimizing task configurations |
| [`remove_task`](#remove_task) | Delete specific tasks | Removing individual tasks that are no longer needed |
| [`get_task_recommendations`](#get_task_recommendations) | Get strategic optimization suggestions | Continuous improvement of task organization |
| [`get_server_health`](#get_server_health) | Server diagnostics and health check | Troubleshooting and monitoring |
| [`get_mise_architecture_rules`](#get_mise_architecture_rules) | Get comprehensive architecture guidelines | Understanding the principles behind task organization |

---

## 🧠 **Core Analysis Tools**

### `analyze_project_for_tasks`

**Purpose**: The flagship tool that analyzes your entire project structure and provides intelligent task recommendations based on detected technologies, frameworks, and development patterns.

**When to Use**:
- Setting up mise tasks for a new project
- Migrating from other build systems
- Optimizing existing task configurations
- Understanding what tasks would be valuable for your stack

#### Request Parameters

```typescript
interface AnalyzeProjectRequest {
  project_path: string;  // Path to your project directory
}
```

#### Response Structure

```typescript
interface AnalyzeProjectResponse {
  project_path: string;
  project_structure: {
    package_managers: string[];      // npm, pip, cargo, etc.
    languages: string[];            // javascript, python, rust, etc.
    frameworks: string[];           // react, fastapi, django, etc.
    has_tests: boolean;
    has_docs: boolean;
    has_ci: boolean;
    has_database: boolean;
    source_dirs: string[];
  };
  existing_tasks: Array<{
    name: string;
    domain: string;                // build, test, lint, etc.
    description: string;
    complexity: string;            // simple, moderate, complex
  }>;
  recommendations: Array<{
    task_name: string;
    domain: string;
    description: string;
    reasoning: string;             // Why this task is recommended
    priority: number;              // 1-10 priority score
    estimated_effort: string;      // Time/complexity estimate
    run_command: string;           // Suggested command to run
    sources: string[];             // Input files/patterns
    outputs: string[];             // Output files/patterns
    complexity: string;
  }>;
}
```

#### Example Usage

```javascript
// Analyze a Next.js project
const result = await analyze_project_for_tasks({
  project_path: "/path/to/my-nextjs-app"
});

console.log(`Found ${result.recommendations.length} task recommendations`);
console.log(`Detected: ${result.project_structure.frameworks.join(", ")}`);

// Example output:
// Found 8 task recommendations
// Detected: nextjs, react, typescript
```

#### Real-World Example

```json
{
  "project_path": "/home/user/my-app",
  "project_structure": {
    "package_managers": ["npm"],
    "languages": ["javascript", "typescript"],
    "frameworks": ["nextjs", "react"],
    "has_tests": true,
    "has_docs": false,
    "has_ci": true,
    "has_database": false,
    "source_dirs": ["src", "pages", "components"]
  },
  "existing_tasks": [],
  "recommendations": [
    {
      "task_name": "dev",
      "domain": "dev",
      "description": "Start Next.js development server with hot reloading",
      "reasoning": "Next.js projects need a development server for local development with hot module replacement",
      "priority": 9,
      "estimated_effort": "low",
      "run_command": "npm run dev",
      "sources": ["src/**/*", "pages/**/*", "next.config.js"],
      "outputs": [".next/**/*"],
      "complexity": "simple"
    },
    {
      "task_name": "build:prod",
      "domain": "build",
      "description": "Build optimized production bundle",
      "reasoning": "Production builds are essential for deployment with optimizations and minification",
      "priority": 10,
      "estimated_effort": "medium",
      "run_command": "npm run build",
      "sources": ["src/**/*", "pages/**/*", "public/**/*"],
      "outputs": [".next/**/*", "out/**/*"],
      "complexity": "moderate"
    }
  ]
}
```

---

### `trace_task_chain`

**Purpose**: Analyze task dependencies to understand the complete execution flow, including parallel execution opportunities and bottlenecks.

**When to Use**:
- Understanding complex task workflows
- Debugging task execution issues
- Optimizing task dependencies
- Planning CI/CD pipeline structure

#### Request Parameters

```typescript
interface TraceTaskChainRequest {
  project_path: string;  // Path to project directory
  task_name: string;     // Name of task to trace (e.g., "deploy:prod")
}
```

#### Response Structure

```typescript
interface TraceTaskChainResponse {
  task_name: string;
  execution_chain: Array<{
    step: number;
    tasks: string[];              // Tasks that run in this step
    parallel_execution: boolean;   // Can these tasks run in parallel?
    estimated_duration: string;    // Estimated time for this step
  }>;
  total_tasks: number;
  estimated_total_time: string;
  bottlenecks: string[];          // Tasks that block parallel execution
  recommendations: string[];       // Suggestions for optimization
}
```

#### Example Usage

```javascript
// Trace the deployment chain
const chain = await trace_task_chain({
  project_path: "/path/to/project",
  task_name: "deploy:prod"
});

console.log(`Deployment requires ${chain.total_tasks} tasks`);
console.log(`Estimated time: ${chain.estimated_total_time}`);
chain.bottlenecks.forEach(task => 
  console.log(`Bottleneck: ${task}`)
);
```

---

## 🔧 **Task Management Tools**

### `create_task`

**Purpose**: Intelligently create new mise tasks with automatic domain classification, complexity assessment, and optimal configuration.

**When to Use**:
- Adding new tasks to your project
- Converting manual commands to automated tasks
- Setting up tasks for new features or workflows

#### Request Parameters

```typescript
interface CreateTaskRequest {
  project_path: string;
  task_description: string;        // Natural language description
  suggested_name?: string;         // Optional task name suggestion
  force_complexity?: "simple" | "moderate" | "complex";
  domain_hint?: string;           // Optional domain suggestion
}
```

#### Response Structure

```typescript
interface CreateTaskResponse {
  success: boolean;
  task_created?: {
    name: string;
    domain: string;
    placement: "toml" | "file";    // Where the task was created
    file_path?: string;            // Path if created as file
    configuration: string;          // Task configuration
  };
  reasoning: string;               // Why this configuration was chosen
  suggestions: string[];           // Additional recommendations
  error?: string;
}
```

#### Example Usage

```javascript
// Create a task from natural language description
const result = await create_task({
  project_path: "/path/to/project",
  task_description: "Run TypeScript type checking with strict mode"
});

if (result.success) {
  console.log(`Created task: ${result.task_created.name}`);
  console.log(`Reasoning: ${result.reasoning}`);
}
```

#### Advanced Examples

```javascript
// Force specific complexity and provide domain hint
const complexTask = await create_task({
  project_path: "/path/to/project",
  task_description: "Build Docker image with multi-stage optimization and push to registry",
  suggested_name: "docker:build-push",
  force_complexity: "complex",
  domain_hint: "deploy"
});

// Simple task creation
const simpleTask = await create_task({
  project_path: "/path/to/project",
  task_description: "Format code with prettier",
  suggested_name: "format"
});
```

---

### `validate_task_architecture`

**Purpose**: Comprehensive validation of your mise task configuration against architectural best practices and optimization opportunities.

**When to Use**:
- Regular health checks of your task configuration
- Before major deployments or releases
- After adding multiple new tasks
- Troubleshooting task execution issues

#### Request Parameters

```typescript
interface ValidateArchitectureRequest {
  project_path: string;
}
```

#### Response Structure

```typescript
interface ValidateArchitectureResponse {
  overall_health: "excellent" | "good" | "needs_attention" | "poor";
  total_tasks: number;
  domains_used: string[];
  issues: Array<{
    severity: "error" | "warning" | "info";
    category: string;
    description: string;
    affected_tasks: string[];
    recommendation: string;
  }>;
  suggestions: Array<{
    type: "optimization" | "best_practice" | "performance";
    description: string;
    impact: "high" | "medium" | "low";
    effort: "low" | "medium" | "high";
  }>;
  metrics: {
    circular_dependencies: number;
    missing_descriptions: number;
    performance_optimizations: number;
    domain_organization_score: number; // 1-10
  };
}
```

#### Example Usage

```javascript
const validation = await validate_task_architecture({
  project_path: "/path/to/project"
});

console.log(`Overall health: ${validation.overall_health}`);
console.log(`Found ${validation.issues.length} issues`);

validation.issues
  .filter(issue => issue.severity === "error")
  .forEach(error => console.log(`ERROR: ${error.description}`));
```

---

## 🧹 **Optimization Tools**

### `prune_tasks`

**Purpose**: Identify and optionally remove redundant, outdated, or unused tasks to keep your configuration clean and efficient.

#### Request Parameters

```typescript
interface PruneTasksRequest {
  project_path: string;
  dry_run: boolean;        // true = report only, false = actually remove
}
```

#### Example Usage

```javascript
// Check what would be pruned (safe)
const dryRun = await prune_tasks({
  project_path: "/path/to/project",
  dry_run: true
});

console.log(`Found ${dryRun.redundant_tasks.length} redundant tasks`);

// Actually remove redundant tasks
const pruneResult = await prune_tasks({
  project_path: "/path/to/project", 
  dry_run: false
});

console.log(`Removed ${pruneResult.removed_tasks.length} tasks`);
```

---

### `get_task_recommendations`

**Purpose**: Get strategic recommendations for improving your task organization, including new tasks, architectural improvements, and optimization opportunities.

#### Response Structure

```typescript
interface TaskRecommendationsResponse {
  project_path: string;
  new_task_recommendations: Array<{
    task_name: string;
    domain: string;
    description: string;
    reasoning: string;
    priority: number;        // 1-10
    estimated_effort: string;
  }>;
  architecture_improvements: {
    issues: string[];
    suggestions: string[];
  };
  redundancy_analysis: {
    redundant_tasks: number;
    details: any[];
  };
  summary: {
    total_existing_tasks: number;
    domains_in_use: number;
    high_priority_recommendations: number;
  };
}
```

#### Example Usage

```javascript
const recommendations = await get_task_recommendations({
  project_path: "/path/to/project"
});

// Show high-priority recommendations
recommendations.new_task_recommendations
  .filter(rec => rec.priority >= 8)
  .forEach(rec => {
    console.log(`HIGH PRIORITY: ${rec.task_name}`);
    console.log(`  Reasoning: ${rec.reasoning}`);
  });
```

---

## 🔍 **Diagnostic Tools**

### `get_server_health`

**Purpose**: Comprehensive server health check and diagnostics information for troubleshooting and monitoring.

#### Response Structure

```typescript
interface ServerHealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  timestamp: string;
  server_info: {
    name: string;
    version: string;
    author: string;
    description: string;
  };
  system_info: {
    python_version: string;
    platform: string;
    working_directory: string;
    python_path: string[];
  };
  dependencies: Record<string, {
    status: "available" | "missing";
    version?: string;
    description: string;
    error?: string;
  }>;
  features: Record<string, {
    status: "available" | "error";
    [key: string]: any;
  }>;
  diagnostics: {
    mise_config: {
      exists: boolean;
      path: string;
      readable: boolean;
    };
    mise_directory: {
      exists: boolean;
      tasks_dir_exists: boolean;
      path: string;
    };
    available_tools: string[];
    available_prompts: string[];
  };
  summary: {
    overall_status: string;
    dependencies_checked: number;
    features_tested: number;
    diagnostics_collected: number;
    error_count: number;
  };
}
```

#### Example Usage

```javascript
const health = await get_server_health();

console.log(`Server status: ${health.status}`);
console.log(`Available tools: ${health.diagnostics.available_tools.length}`);

if (health.status !== "healthy") {
  console.log("Issues found:");
  Object.entries(health.dependencies)
    .filter(([_, dep]) => dep.status === "missing")
    .forEach(([name, dep]) => 
      console.log(`  Missing dependency: ${name} - ${dep.description}`)
    );
}
```

---

## 📚 **Knowledge Base**

### `get_mise_architecture_rules`

**Purpose**: Get the complete set of architectural rules, patterns, and conventions that guide intelligent task creation.

#### Response Structure

```typescript
interface ArchitectureRulesResponse {
  domains: {
    core_domains: string[];
    descriptions: Record<string, string>;
  };
  naming_conventions: {
    hierarchical_structure: string;
    sub_domain_nesting: string;
    environment_variants: string;
    tool_specific: string;
  };
  file_structure: {
    root_config: string;
    task_directory: string;
    file_tasks: string;
    domain_subdirs: string;
    local_overrides: string;
  };
  task_types: {
    toml_tasks: string;
    file_tasks: string;
    complexity_guidelines: Record<string, string>;
  };
  dependencies: {
    depends: string;
    depends_post: string;
    wait_for: string;
    best_practices: string[];
  };
  performance: {
    source_tracking: string;
    output_tracking: string;
    parallel_execution: string;
    glob_patterns: string;
  };
}
```

---

## 🎯 **Expert Prompts**

Wise Mise MCP provides intelligent prompts that give you expert guidance on task architecture and analysis.

### `mise_task_expert_guidance`

**Purpose**: Get comprehensive guidance on mise task architecture and best practices.

**Usage**: This prompt transforms your MCP client (like Claude) into a mise task expert, providing detailed guidance on:
- Task creation decision trees
- Domain classification
- Dependency analysis
- Performance optimization
- Architecture best practices

**Example**:
```
> Use the mise_task_expert_guidance prompt
> Help me organize tasks for a full-stack TypeScript application
```

### `task_chain_analyst`

**Purpose**: Get expert analysis of complex task dependency graphs and execution flows.

**Usage**: This prompt provides specialized analysis capabilities for understanding task chains, including:
- Execution flow mapping
- Bottleneck identification
- Performance optimization
- Parallel execution opportunities

**Example**:
```
> Use the task_chain_analyst prompt  
> Analyze the deployment chain for my microservices architecture
```

---

## 🔧 **Integration Examples**

### Claude Desktop Configuration

Add Wise Mise MCP to your Claude Desktop configuration:

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

### Common Workflow Patterns

#### 1. **New Project Setup**

```javascript
// 1. Analyze the project structure
const analysis = await analyze_project_for_tasks({
  project_path: "/path/to/new/project"
});

// 2. Review and implement high-priority recommendations
const highPriority = analysis.recommendations
  .filter(rec => rec.priority >= 8);

// 3. Create tasks for essential workflows
for (const rec of highPriority.slice(0, 5)) {
  const result = await create_task({
    project_path: "/path/to/new/project",
    task_description: rec.description,
    suggested_name: rec.task_name
  });
}

// 4. Validate the resulting configuration
const validation = await validate_task_architecture({
  project_path: "/path/to/new/project"
});
```

#### 2. **Configuration Optimization**

```javascript
// 1. Get optimization recommendations
const recommendations = await get_task_recommendations({
  project_path: "/path/to/project"
});

// 2. Clean up redundant tasks
await prune_tasks({
  project_path: "/path/to/project",
  dry_run: false
});

// 3. Validate improvements
const validation = await validate_task_architecture({
  project_path: "/path/to/project"
});
```

#### 3. **Deployment Pipeline Analysis**

```javascript
// Trace the deployment workflow
const deployChain = await trace_task_chain({
  project_path: "/path/to/project",
  task_name: "deploy:production"
});

console.log("Deployment Steps:");
deployChain.execution_chain.forEach((step, i) => {
  console.log(`Step ${step.step}: ${step.tasks.join(", ")}`);
  if (step.parallel_execution) {
    console.log("  (Can run in parallel)");
  }
});

if (deployChain.bottlenecks.length > 0) {
  console.log("Bottlenecks to address:");
  deployChain.bottlenecks.forEach(task => console.log(`  - ${task}`));
}
```

---

## 🚨 **Error Handling**

All tools return consistent error structures when issues occur:

```typescript
interface ErrorResponse {
  error: string;          // Human-readable error message
  code?: string;          // Optional error code
  details?: any;          // Additional error context
}
```

### Common Error Scenarios

- **Project path doesn't exist**: Verify the path and ensure it's accessible
- **No mise configuration found**: The tool will analyze the project but may have limited context
- **Permission issues**: Ensure the server has read/write access to the project directory
- **Malformed task configuration**: The validation tool will identify specific issues

---

## 🎨 **Best Practices**

### 1. **Start with Analysis**

Always begin by analyzing your project structure to understand what Wise Mise MCP can detect:

```javascript
const analysis = await analyze_project_for_tasks({
  project_path: "/your/project"
});
```

### 2. **Validate Regularly**

Run architecture validation periodically to maintain optimal configuration:

```javascript
const health = await validate_task_architecture({
  project_path: "/your/project"
});
```

### 3. **Use Natural Language**

When creating tasks, describe what you want in natural language:

```javascript
await create_task({
  project_path: "/your/project",
  task_description: "Run integration tests against the staging environment with database reset"
});
```

### 4. **Leverage Expert Guidance**

Use the expert prompts to get contextual advice for your specific situation.

---

## 📈 **Performance Considerations**

- **Analysis operations** typically complete in under 2 seconds for most projects
- **Large monorepos** (10,000+ files) may take up to 5 seconds for full analysis
- **Task creation** is near-instantaneous for most configurations
- **Dependency tracing** scales linearly with task complexity

---

**Happy building with Wise Mise MCP!** 🚀

For more examples and tutorials, see our [Usage Guide](./USAGE.md) and [Contributing Guide](./CONTRIBUTING.md).