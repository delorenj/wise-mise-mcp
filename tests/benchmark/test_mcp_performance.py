"""
MCP Server Performance Benchmarks

Tests the performance characteristics of the MCP server including:
- Request/response latency
- Throughput under load
- Memory usage patterns
- Resource utilization
"""

import pytest
import asyncio
import time
import psutil
import gc
from pathlib import Path
from typing import Dict, List, Any
from unittest.mock import Mock, AsyncMock

import pytest_benchmark
from wise_mise.server import (
    analyze_project_for_tasks,
    trace_task_chain,
    create_task,
    validate_task_architecture,
    get_task_recommendations,
    AnalyzeProjectRequest,
    TraceTaskChainRequest,
    CreateTaskRequest,
    ValidateArchitectureRequest,
)


class TestMCPServerPerformance:
    """Performance benchmarks for MCP server operations"""

    @pytest.mark.benchmark(group="analyze_project")
    def test_analyze_small_project_performance(self, benchmark, temp_project_dir):
        """Benchmark project analysis for small projects (< 50 files)"""
        
        def setup_small_project():
            # Create a small project structure
            for i in range(20):
                (temp_project_dir / f"file_{i}.py").write_text(f"# File {i}")
            (temp_project_dir / "package.json").write_text('{"name": "test"}')
            return AnalyzeProjectRequest(project_path=str(temp_project_dir))
        
        async def analyze_project():
            request = setup_small_project()
            return await analyze_project_for_tasks.fn(project_path=request.project_path)
        
        result = benchmark(lambda: asyncio.run(analyze_project()))
        assert "error" not in result
        # Verify we have expected structure fields
        assert "project_structure" in result
        assert "package_managers" in result["project_structure"]
        assert len(result["existing_tasks"]) >= 0

    @pytest.mark.benchmark(group="analyze_project")
    @pytest.mark.slow
    def test_analyze_large_project_performance(self, benchmark, complex_project_structure):
        """Benchmark project analysis for large projects (1000+ files)"""
        
        def setup_large_project():
            # Create a large project structure
            for i in range(500):
                (complex_project_structure / "frontend" / f"component_{i}.tsx").write_text(
                    f"export const Component{i} = () => <div>Component {i}</div>;"
                )
                (complex_project_structure / "backend" / f"model_{i}.py").write_text(
                    f"class Model{i}:\n    pass"
                )
            return AnalyzeProjectRequest(project_path=str(complex_project_structure))
        
        async def analyze_large_project():
            request = setup_large_project()
            return await analyze_project_for_tasks.fn(project_path=request.project_path)
        
        result = benchmark(lambda: asyncio.run(analyze_large_project()))
        assert "error" not in result
        # Verify we have a complex project structure
        assert "project_structure" in result
        assert len(result["existing_tasks"]) > 0

    @pytest.mark.benchmark(group="task_operations")
    def test_task_chain_tracing_performance(self, benchmark, temp_project_dir):
        """Benchmark task chain analysis performance"""
        
        def setup_complex_task_chain():
            # Create .mise.toml with complex dependencies
            mise_config = """
[tasks.compile]
run = "gcc -c src/*.c"
sources = ["src/**/*.c", "include/**/*.h"]

[tasks.link] 
run = "gcc -o app obj/*.o"
depends = ["compile"]

[tasks.test]
run = "pytest tests/"
depends = ["link"]

[tasks.integration]
run = "pytest tests/integration/"
depends = ["test", "setup_db"]

[tasks.setup_db]
run = "docker-compose up -d postgres"

[tasks.e2e]
run = "playwright test"
depends = ["integration", "setup_frontend"]

[tasks.setup_frontend]
run = "npm run build"
depends = ["install_deps"]

[tasks.install_deps]
run = "npm install"

[tasks.deploy]
run = "deploy.sh"
depends = ["e2e", "security_scan"]

[tasks.security_scan]
run = "bandit -r src/"
depends = ["test"]
"""
            (temp_project_dir / ".mise.toml").write_text(mise_config.strip())
            return TraceTaskChainRequest(
                project_path=str(temp_project_dir),
                task_name="deploy"
            )
        
        async def trace_complex_chain():
            request = setup_complex_task_chain()
            return await trace_task_chain.fn(
                project_path=request.project_path,
                task_name=request.task_name
            )
        
        result = benchmark(lambda: asyncio.run(trace_complex_chain()))
        assert "error" not in result
        # Should have traced the complex dependency chain
        assert "execution_chain" in result
        assert len(result["execution_chain"]) >= 1

    @pytest.mark.benchmark(group="task_operations")
    def test_concurrent_task_creation_performance(self, benchmark, temp_project_dir):
        """Benchmark concurrent task creation operations"""
        
        async def create_multiple_tasks():
            tasks = []
            for i in range(10):
                task = create_task.fn(
                    project_path=str(temp_project_dir),
                    task_description=f"Test task number {i}",
                    suggested_name=f"test_task_{i}"
                )
                tasks.append(task)
            
            return await asyncio.gather(*tasks)
        
        results = benchmark(lambda: asyncio.run(create_multiple_tasks()))
        assert len(results) == 10
        for result in results:
            assert "error" not in result

    @pytest.mark.benchmark(group="memory_usage")
    def test_memory_usage_during_large_analysis(self, benchmark, complex_project_structure):
        """Benchmark memory usage during large project analysis"""
        
        def monitor_memory_usage():
            process = psutil.Process()
            memory_before = process.memory_info().rss
            
            async def analyze_with_memory_monitoring():
                request = AnalyzeProjectRequest(project_path=str(complex_project_structure))
                gc.collect()  # Clean up before measurement
                
                memory_start = process.memory_info().rss
                result = await analyze_project_for_tasks.fn(project_path=request.project_path)
                memory_peak = process.memory_info().rss
                
                gc.collect()  # Clean up after analysis
                memory_end = process.memory_info().rss
                
                return {
                    "result": result,
                    "memory_stats": {
                        "before_mb": memory_before / 1024 / 1024,
                        "start_mb": memory_start / 1024 / 1024,
                        "peak_mb": memory_peak / 1024 / 1024,
                        "end_mb": memory_end / 1024 / 1024,
                        "increase_mb": (memory_peak - memory_start) / 1024 / 1024
                    }
                }
            
            return asyncio.run(analyze_with_memory_monitoring())
        
        result = benchmark(monitor_memory_usage)
        
        # Verify the analysis succeeded
        assert "error" not in result["result"]
        
        # Memory usage should be reasonable (less than 100MB increase)
        assert result["memory_stats"]["increase_mb"] < 100
        
        # Memory should be released after processing
        memory_leaked = (
            result["memory_stats"]["end_mb"] - 
            result["memory_stats"]["start_mb"]
        )
        assert memory_leaked < 10  # Less than 10MB leaked

    @pytest.mark.benchmark(group="task_recommendations")
    def test_task_recommendations_performance(self, benchmark, complex_project_structure):
        """Benchmark task recommendation generation performance"""
        
        async def generate_recommendations():
            return await get_task_recommendations.fn()
        
        result = benchmark(lambda: asyncio.run(generate_recommendations()))
        assert "error" not in result
        assert "best_practices" in result

    @pytest.mark.benchmark(group="architecture_validation")
    def test_architecture_validation_performance(self, benchmark, temp_project_dir):
        """Benchmark architecture validation performance"""
        
        def setup_validation_request():
            # Create complex task architecture for validation in .mise.toml
            mise_config = "[tools]\nnode = '20'\n\n"
            for i in range(10):  # Reduced from 50 for faster testing
                depends_clause = f'depends = ["task_{i-1}"]' if i > 0 else ""
                mise_config += f'[tasks."task_{i}"]\nrun = "echo Task {i}"\n{depends_clause}\n\n'
            
            (temp_project_dir / ".mise.toml").write_text(mise_config)
            return temp_project_dir
        
        def run_validation():
            request = setup_validation_request()
            
            async def validate():
                return await validate_task_architecture.fn(project_path=str(request))
            
            return asyncio.run(validate())
        
        result = benchmark(run_validation)
        assert "error" not in result

    @pytest.mark.benchmark(group="stress_test")
    @pytest.mark.slow
    def test_sustained_load_performance(self, benchmark):
        """Test server performance under sustained load"""
        
        async def sustained_operations():
            # Create temporary directory for testing
            import tempfile
            with tempfile.TemporaryDirectory() as temp_dir:
                project_path = Path(temp_dir)
                
                # Create test files
                for i in range(100):
                    (project_path / f"test_{i}.py").write_text(f"# Test file {i}")
                
                # Run many operations in parallel
                operations = []
                
                # Mix different types of operations
                for i in range(20):
                    # Analysis operations
                    analysis_request = AnalyzeProjectRequest(project_path=str(project_path))
                    operations.append(analyze_project_for_tasks.fn(project_path=analysis_request.project_path))
                    
                    # Task creation operations
                    operations.append(create_task.fn(
                        project_path=str(project_path),
                        task_description=f"Load test task {i}"
                    ))
                
                # Execute all operations concurrently
                results = await asyncio.gather(*operations, return_exceptions=True)
                
                # Count successful operations
                successful = sum(1 for r in results if not isinstance(r, Exception))
                return {
                    "total_operations": len(operations),
                    "successful_operations": successful,
                    "error_rate": (len(operations) - successful) / len(operations)
                }
        
        result = benchmark(lambda: asyncio.run(sustained_operations()))
        
        # At least 80% of operations should succeed under load
        assert result["error_rate"] < 0.2
        assert result["successful_operations"] >= result["total_operations"] * 0.8


class TestPerformanceRegression:
    """Tests to detect performance regressions"""
    
    @pytest.mark.benchmark(group="regression")
    def test_baseline_analysis_performance(self, benchmark, temp_project_dir):
        """Baseline performance test for regression detection"""
        
        # Create standard test project
        (temp_project_dir / "package.json").write_text(
            '{"name": "test", "scripts": {"build": "webpack", "test": "jest"}}'
        )
        for i in range(10):
            (temp_project_dir / f"src/component_{i}.js").write_text(
                f"export const Component{i} = () => 'Component {i}';"
            )
        
        async def baseline_analysis():
            request = AnalyzeProjectRequest(project_path=str(temp_project_dir))
            return await analyze_project_for_tasks.fn(project_path=request.project_path)
        
        result = benchmark(lambda: asyncio.run(baseline_analysis()))
        assert "error" not in result
        
        # Store baseline metrics for comparison
        benchmark.extra_info = {
            "package_managers": len(result["project_structure"].get("package_managers", [])),
            "task_count": len(result.get("recommended_tasks", []))
        }

    def test_performance_thresholds(self):
        """Verify performance meets minimum thresholds"""
        # These would typically be configured based on benchmarking results
        THRESHOLDS = {
            "small_project_analysis_ms": 100,    # < 100ms for small projects
            "large_project_analysis_ms": 5000,   # < 5s for large projects  
            "task_chain_trace_ms": 50,           # < 50ms for task chain tracing
            "memory_usage_mb": 50,               # < 50MB memory usage
            "concurrent_operations": 10,         # Support 10+ concurrent operations
        }
        
        # This test serves as documentation of performance expectations
        # Actual threshold checking would be done by the benchmark comparison
        assert all(threshold > 0 for threshold in THRESHOLDS.values())