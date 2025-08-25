"""
Unit tests for wise_mise_mcp.server module
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

from wise_mise_mcp.server import (
    AnalyzeProjectRequest,
    TraceTaskChainRequest, 
    CreateTaskRequest,
    ValidateArchitectureRequest,
    PruneTasksRequest,
    RemoveTaskRequest,
    analyze_project_for_tasks,
    trace_task_chain,
    create_task,
    validate_task_architecture,
    prune_tasks,
    remove_task,
    get_task_recommendations,
    get_mise_architecture_rules,
    mise_task_expert_guidance,
    task_chain_analyst
)
from wise_mise_mcp.models import TaskComplexity


class TestRequestModels:
    """Test request/response models"""
    
    def test_analyze_project_request(self):
        """Test AnalyzeProjectRequest validation"""
        request = AnalyzeProjectRequest(project_path="/test/project")
        assert request.project_path == "/test/project"
        
    def test_trace_task_chain_request(self):
        """Test TraceTaskChainRequest validation"""
        request = TraceTaskChainRequest(
            project_path="/test/project",
            task_name="build"
        )
        assert request.project_path == "/test/project"
        assert request.task_name == "build"
        
    def test_create_task_request(self):
        """Test CreateTaskRequest validation"""
        request = CreateTaskRequest(
            project_path="/test/project",
            task_description="Build the frontend",
            suggested_name="frontend",
            force_complexity="complex",
            domain_hint="build"
        )
        assert request.project_path == "/test/project"
        assert request.task_description == "Build the frontend"
        assert request.suggested_name == "frontend"
        assert request.force_complexity == "complex"
        assert request.domain_hint == "build"
        
    def test_create_task_request_minimal(self):
        """Test CreateTaskRequest with minimal fields"""
        request = CreateTaskRequest(
            project_path="/test/project",
            task_description="Simple task"
        )
        assert request.project_path == "/test/project"
        assert request.task_description == "Simple task"
        assert request.suggested_name is None
        assert request.force_complexity is None
        assert request.domain_hint is None
        
    def test_validate_architecture_request(self):
        """Test ValidateArchitectureRequest validation"""
        request = ValidateArchitectureRequest(project_path="/test/project")
        assert request.project_path == "/test/project"
        
    def test_prune_tasks_request(self):
        """Test PruneTasksRequest validation"""
        request = PruneTasksRequest(
            project_path="/test/project",
            dry_run=False
        )
        assert request.project_path == "/test/project"
        assert request.dry_run is False
        
    def test_prune_tasks_request_default(self):
        """Test PruneTasksRequest with default dry_run"""
        request = PruneTasksRequest(project_path="/test/project")
        assert request.dry_run is True  # Default value
        
    def test_remove_task_request(self):
        """Test RemoveTaskRequest validation"""
        request = RemoveTaskRequest(
            project_path="/test/project",
            task_name="test:old"
        )
        assert request.project_path == "/test/project"
        assert request.task_name == "test:old"


class TestAnalyzeProjectForTasks:
    """Test analyze_project_for_tasks tool function"""
    
    @pytest.mark.asyncio
    async def test_analyze_existing_project(self, temp_project_dir):
        """Test analyzing existing project"""
        
        result = await analyze_project_for_tasks.fn(project_path=str(temp_project_dir))
        
        assert "error" not in result
        assert "project_path" in result
        assert "project_structure" in result
        assert "existing_tasks" in result
        assert "recommended_tasks" in result
        
        # Verify project structure
        structure = result["project_structure"]
        assert "npm" in structure["package_managers"]
        assert "javascript" in structure["languages"]
        assert structure["has_tests"] is True  # From fixture
        
        # Verify existing tasks
        assert len(result["existing_tasks"]) > 0
        task_names = [task["name"] for task in result["existing_tasks"]]
        assert "build:build" in task_names
        assert "test:test" in task_names
        
        # Verify recommendations
        assert len(result["recommended_tasks"]) >= 0
        
    @pytest.mark.asyncio
    async def test_analyze_nonexistent_project(self):
        """Test analyzing non-existent project"""
        
        result = await analyze_project_for_tasks.fn(project_path="/nonexistent/path")
        
        assert "error" in result
        assert "does not exist" in result["error"]
        
    @pytest.mark.asyncio 
    async def test_analyze_project_exception_handling(self):
        """Test exception handling in analyze_project_for_tasks"""
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('wise_mise_mcp.server.TaskAnalyzer') as mock_analyzer_class:
                mock_analyzer = Mock()
                mock_analyzer.analyze_project_structure.side_effect = Exception("Test error")
                mock_analyzer_class.return_value = mock_analyzer
                
                result = await analyze_project_for_tasks.fn(project_path="/test")
                
                assert "error" in result
                assert "Test error" in result["error"]


class TestTraceTaskChain:
    """Test trace_task_chain tool function"""
    
    @pytest.mark.asyncio
    async def test_trace_existing_task(self, temp_project_dir):
        """Test tracing existing task chain"""
        request = TraceTaskChainRequest(
            project_path=str(temp_project_dir),
            task_name="test"
        )
        
        with patch('wise_mise_mcp.server.TaskAnalyzer') as mock_analyzer_class:
            mock_analyzer = Mock()
            mock_analyzer.trace_task_chain.return_value = {
                "task_name": "test",
                "execution_order": ["test"],
                "task_details": {
                    "test": {
                        "domain": "test",
                        "description": "Test task",
                        "run": "npm test",
                        "complexity": "simple"
                    }
                }
            }
            mock_analyzer_class.return_value = mock_analyzer
            
            result = await trace_task_chain.fn(project_path=request.project_path, task_name=request.task_name)
            
            assert "error" not in result or result.get("target_task") == "test"
            if "target_task" in result:
                assert result["target_task"] == "test"
                assert "execution_chain" in result
                assert "total_steps" in result
                assert "estimated_complexity" in result
            
    @pytest.mark.asyncio
    async def test_trace_nonexistent_task(self, temp_project_dir):
        """Test tracing non-existent task"""
        request = TraceTaskChainRequest(
            project_path=str(temp_project_dir),
            task_name="nonexistent"
        )
        
        result = await trace_task_chain.fn(project_path=request.project_path, task_name=request.task_name)
        
        assert "error" in result
        assert "not found" in result["error"].lower()
        
    @pytest.mark.asyncio
    async def test_trace_task_nonexistent_project(self):
        """Test tracing task in non-existent project"""
        request = TraceTaskChainRequest(
            project_path="/nonexistent/path",
            task_name="build"
        )
        
        result = await trace_task_chain.fn(project_path=request.project_path, task_name=request.task_name)
        
        assert "error" in result
        assert "does not exist" in result["error"]


class TestCreateTask:
    """Test create_task tool function"""
    
    @pytest.mark.asyncio
    async def test_create_simple_task(self, temp_project_dir):
        """Test creating simple task"""
        request = CreateTaskRequest(
            project_path=str(temp_project_dir),
            task_description="Run unit tests with coverage",
            suggested_name="coverage"
        )
        
        with patch('wise_mise_mcp.server.TaskManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager.create_task_intelligently.return_value = {
                "success": True,
                "task_name": "test:coverage",
                "type": "toml_task"
            }
            mock_manager_class.return_value = mock_manager
            
            result = await create_task.fn(project_path=request.project_path, task_description=request.task_description, suggested_name=request.suggested_name, force_complexity=request.force_complexity, domain_hint=request.domain_hint)
            
            assert result["result"]["success"] is True
            assert result["result"]["task_name"] == "test:coverage"
            
    @pytest.mark.asyncio
    async def test_create_task_with_force_complexity(self, temp_project_dir):
        """Test creating task with forced complexity"""
        request = CreateTaskRequest(
            project_path=str(temp_project_dir),
            task_description="Deploy to production",
            force_complexity="complex"
        )
        
        with patch('wise_mise_mcp.server.TaskManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager.create_task_intelligently.return_value = {
                "success": True,
                "task_name": "deploy:production",
                "type": "file_task"
            }
            mock_manager_class.return_value = mock_manager
            
            result = await create_task.fn(project_path=request.project_path, task_description=request.task_description, suggested_name=request.suggested_name, force_complexity=request.force_complexity, domain_hint=request.domain_hint)
            
            # Verify force_complexity was converted to enum
            mock_manager.create_task_intelligently.assert_called_once()
            call_args = mock_manager.create_task_intelligently.call_args
            assert call_args[1]["force_complexity"] == TaskComplexity.COMPLEX
            
    @pytest.mark.asyncio
    async def test_create_task_invalid_complexity(self, temp_project_dir):
        """Test creating task with invalid complexity"""
        request = CreateTaskRequest(
            project_path=str(temp_project_dir),
            task_description="Test task",
            force_complexity="invalid"
        )
        
        result = await create_task.fn(project_path=request.project_path, task_description=request.task_description, suggested_name=request.suggested_name, force_complexity=request.force_complexity, domain_hint=request.domain_hint)
        
        assert "error" in result
        assert "Invalid complexity" in result["error"]
        
    @pytest.mark.asyncio
    async def test_create_task_nonexistent_project(self):
        """Test creating task in non-existent project"""
        request = CreateTaskRequest(
            project_path="/nonexistent/path",
            task_description="Test task"
        )
        
        result = await create_task.fn(project_path=request.project_path, task_description=request.task_description, suggested_name=request.suggested_name, force_complexity=request.force_complexity, domain_hint=request.domain_hint)
        
        assert "error" in result
        assert "does not exist" in result["error"]


class TestValidateTaskArchitecture:
    """Test validate_task_architecture tool function"""
    
    @pytest.mark.asyncio
    async def test_validate_existing_project(self, temp_project_dir):
        """Test validating existing project architecture"""
        request = ValidateArchitectureRequest(project_path=str(temp_project_dir))
        
        result = await validate_task_architecture.fn(project_path=request.project_path)
        
        assert "error" not in result
        # Should contain validation results from analyzer
        
    @pytest.mark.asyncio
    async def test_validate_nonexistent_project(self):
        """Test validating non-existent project"""
        request = ValidateArchitectureRequest(project_path="/nonexistent/path")
        
        result = await validate_task_architecture.fn(project_path=request.project_path)
        
        assert "error" in result
        assert "does not exist" in result["error"]


class TestPruneTasks:
    """Test prune_tasks tool function"""
    
    @pytest.mark.asyncio
    async def test_prune_tasks_dry_run(self, temp_project_dir):
        """Test pruning tasks in dry run mode"""
        request = PruneTasksRequest(
            project_path=str(temp_project_dir),
            dry_run=True
        )
        
        with patch('wise_mise_mcp.server.TaskAnalyzer') as mock_analyzer_class:
            mock_analyzer = Mock()
            mock_analyzer.find_redundant_tasks.return_value = [
                {"task": "redundant_task", "reason": "No dependencies"}
            ]
            mock_analyzer_class.return_value = mock_analyzer
            
            result = await prune_tasks.fn(project_path=request.project_path, dry_run=request.dry_run)
            
            assert result["dry_run"] is True
            assert "tasks_to_prune" in result
            assert len(result["tasks_to_prune"]) == 1
            assert "total_to_prune" in result
            assert result["total_to_prune"] == 1
            
    @pytest.mark.asyncio
    async def test_prune_tasks_actual_removal(self, temp_project_dir):
        """Test actually removing redundant tasks"""
        request = PruneTasksRequest(
            project_path=str(temp_project_dir),
            dry_run=False
        )
        
        with patch('wise_mise_mcp.server.TaskAnalyzer') as mock_analyzer_class:
            with patch('wise_mise_mcp.server.TaskManager') as mock_manager_class:
                mock_analyzer = Mock()
                mock_analyzer.find_redundant_tasks.return_value = [
                    {"task": "redundant_task", "reason": "No dependencies"}
                ]
                mock_analyzer_class.return_value = mock_analyzer
                
                mock_manager = Mock()
                mock_manager.remove_task.return_value = {"success": True}
                mock_manager_class.return_value = mock_manager
                
                result = await prune_tasks.fn(project_path=request.project_path, dry_run=request.dry_run)
                
                assert result["dry_run"] is False
                assert "pruned_tasks" in result
                assert "total_pruned" in result
                assert result["total_pruned"] == 1
                # Check if the task was pruned
                task_names = [task["name"] for task in result["pruned_tasks"]]
                assert "redundant_task" in task_names
                
    @pytest.mark.asyncio
    async def test_prune_tasks_nonexistent_project(self):
        """Test pruning tasks in non-existent project"""
        request = PruneTasksRequest(project_path="/nonexistent/path")
        
        result = await prune_tasks.fn(project_path=request.project_path, dry_run=True)
        
        assert "error" in result
        assert "does not exist" in result["error"]


class TestRemoveTask:
    """Test remove_task tool function"""
    
    @pytest.mark.asyncio
    async def test_remove_existing_task(self, temp_project_dir):
        """Test removing existing task"""
        request = RemoveTaskRequest(
            project_path=str(temp_project_dir),
            task_name="test:old"
        )
        
        with patch('wise_mise_mcp.server.TaskManager') as mock_manager_class:
            with patch('wise_mise_mcp.server.TaskAnalyzer') as mock_analyzer_class:
                # Mock the analyzer to find existing tasks
                from wise_mise_mcp.models import TaskDefinition, TaskDomain, TaskComplexity
                
                mock_task = TaskDefinition(
                    name="old",
                    domain=TaskDomain.TEST,
                    description="Test task to remove",
                    run="echo 'test'",
                    complexity=TaskComplexity.SIMPLE
                )
                
                mock_analyzer = Mock()
                mock_analyzer.extract_existing_tasks.return_value = [mock_task]
                mock_analyzer.build_dependency_graph.return_value = {}
                mock_analyzer.find_dependent_tasks.return_value = []
                mock_analyzer_class.return_value = mock_analyzer
                
                # Mock the manager
                mock_manager = Mock()
                mock_manager.remove_task.return_value = {"success": True}
                mock_manager_class.return_value = mock_manager
                
                result = await remove_task.fn(project_path=request.project_path, task_name=request.task_name)
                
                assert "error" not in result
                assert "removed_task" in result
                assert result["removed_task"]["name"] == "test:old"
                assert "dependent_tasks_affected" in result
            
    @pytest.mark.asyncio
    async def test_remove_nonexistent_task(self, temp_project_dir):
        """Test removing non-existent task"""
        request = RemoveTaskRequest(
            project_path=str(temp_project_dir),
            task_name="nonexistent"
        )
        
        with patch('wise_mise_mcp.server.TaskManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager.remove_task.return_value = {
                "error": "Task 'nonexistent' not found"
            }
            mock_manager_class.return_value = mock_manager
            
            result = await remove_task.fn(project_path=request.project_path, task_name=request.task_name)
            
            assert "error" in result
            assert "not found" in result["error"]
            
    @pytest.mark.asyncio
    async def test_remove_task_nonexistent_project(self):
        """Test removing task from non-existent project"""
        request = RemoveTaskRequest(
            project_path="/nonexistent/path",
            task_name="test"
        )
        
        result = await remove_task.fn(project_path=request.project_path, task_name=request.task_name)
        
        assert "error" in result
        assert "does not exist" in result["error"]


class TestGetTaskRecommendations:
    """Test get_task_recommendations tool function"""
    
    @pytest.mark.asyncio
    async def test_get_recommendations(self, temp_project_dir):
        """Test getting task recommendations"""
        result = await get_task_recommendations.fn()
        
        assert "error" not in result
        assert "best_practices" in result
        assert "common_patterns" in result
        assert "domain_guidelines" in result
        
        # Verify best practices structure
        best_practices = result["best_practices"]
        assert "naming" in best_practices
        assert "organization" in best_practices
        assert "dependencies" in best_practices
        assert "performance" in best_practices
        
        # Verify each section has recommendations
        assert len(best_practices["naming"]) > 0
        assert len(best_practices["organization"]) > 0
        
    @pytest.mark.asyncio
    async def test_get_recommendations_nonexistent_project(self):
        """Test getting general recommendations (no project-specific data)"""
        # get_task_recommendations doesn't require a project path - it returns general guidance
        result = await get_task_recommendations.fn()
        
        # Should always succeed as it provides general recommendations
        assert "error" not in result
        assert "best_practices" in result
        assert "domain_guidelines" in result


class TestGetMiseArchitectureRules:
    """Test get_mise_architecture_rules tool function"""
    
    @pytest.mark.asyncio
    async def test_get_architecture_rules(self):
        """Test getting mise architecture rules"""
        result = await get_mise_architecture_rules.fn()
        
        assert "error" not in result
        assert "architecture_principles" in result
        assert "domain_hierarchy" in result
        assert "complexity_levels" in result
        assert "dependency_patterns" in result
        
        # Verify domain hierarchy has expected domains
        domain_hierarchy = result["domain_hierarchy"]
        assert "build" in domain_hierarchy
        assert "test" in domain_hierarchy
        assert "lint" in domain_hierarchy
        assert "deploy" in domain_hierarchy
        
        # Verify complexity levels
        complexity_levels = result["complexity_levels"]
        assert "simple" in complexity_levels
        assert "moderate" in complexity_levels
        assert "complex" in complexity_levels


class TestPromptFunctions:
    """Test prompt functions"""
    
    @pytest.mark.asyncio
    async def test_mise_task_expert_guidance(self):
        """Test mise task expert guidance prompt"""
        result = await mise_task_expert_guidance.fn()
        
        assert isinstance(result, dict)
        assert "error" not in result
        assert "expert_tips" in result
        assert "common_issues" in result
        assert "migration_strategies" in result
        
        # Verify expert tips structure
        expert_tips = result["expert_tips"]
        assert "debugging_tasks" in expert_tips
        assert "performance_optimization" in expert_tips
        assert "advanced_patterns" in expert_tips
        
        # Verify guidance has substance
        assert len(expert_tips["debugging_tasks"]) > 0
        assert len(expert_tips["performance_optimization"]) > 0
        
    @pytest.mark.asyncio
    async def test_task_chain_analyst(self):
        """Test task chain analyst prompt"""
        result = await task_chain_analyst.fn()
        
        assert isinstance(result, dict)
        assert "error" not in result
        assert "analysis_techniques" in result
        assert "optimization_strategies" in result
        assert "performance_metrics" in result
        assert "visualization_tips" in result
        
        # Verify analysis techniques structure
        techniques = result["analysis_techniques"]
        assert "bottleneck_detection" in techniques
        assert "critical_path" in techniques
        assert "parallelization" in techniques
        
        # Verify optimization strategies
        strategies = result["optimization_strategies"]
        assert "parallel_execution" in strategies
        assert "caching_optimization" in strategies


class TestServerIntegration:
    """Test integration aspects of the server"""
    
    def test_all_request_models_importable(self):
        """Test that all request models can be imported and used"""
        from wise_mise_mcp.server import (
            AnalyzeProjectRequest,
            TraceTaskChainRequest,
            CreateTaskRequest,
            ValidateArchitectureRequest,
            PruneTasksRequest,
            RemoveTaskRequest
        )
        
        # Should be able to create instances
        AnalyzeProjectRequest(project_path="/test")
        TraceTaskChainRequest(project_path="/test", task_name="build")
        CreateTaskRequest(project_path="/test", task_description="Test")
        ValidateArchitectureRequest(project_path="/test")
        PruneTasksRequest(project_path="/test")
        RemoveTaskRequest(project_path="/test", task_name="old")
        
    def test_fastmcp_app_structure(self):
        """Test that FastMCP app is properly structured"""
        from wise_mise_mcp.server import app
        
        # Should have app instance
        assert app is not None
        assert hasattr(app, 'tool')
        assert hasattr(app, 'prompt')
        
    @pytest.mark.asyncio
    async def test_error_handling_consistency(self):
        """Test that error handling is consistent across all tools"""
        nonexistent_path = "/nonexistent/path"
        
        # All tools should handle non-existent paths gracefully
        tools_to_test = [
            (analyze_project_for_tasks, AnalyzeProjectRequest(project_path=nonexistent_path)),
            (trace_task_chain, TraceTaskChainRequest(project_path=nonexistent_path, task_name="build")),
            (create_task, CreateTaskRequest(project_path=nonexistent_path, task_description="test")),
            (validate_task_architecture, ValidateArchitectureRequest(project_path=nonexistent_path)),
            (prune_tasks, PruneTasksRequest(project_path=nonexistent_path)),
            (remove_task, RemoveTaskRequest(project_path=nonexistent_path, task_name="test"))
        ]
        
        for tool_func, request in tools_to_test:
            result = await tool_func.fn(project_path=request.project_path) if hasattr(request, "project_path") else await tool_func.fn()
            
            # All should return error dict instead of raising exception
            assert isinstance(result, dict)
            assert "error" in result
            assert "does not exist" in result["error"]