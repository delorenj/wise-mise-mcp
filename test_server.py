#!/usr/bin/env python3
"""
Test script to validate the Wise Mise MCP server functionality
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, Any

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from wise_mise_mcp.analyzer import TaskAnalyzer
from wise_mise_mcp.manager import TaskManager
from wise_mise_mcp.models import ProjectStructure


async def test_project_analysis(project_path: Path) -> Dict[str, Any]:
    """Test project analysis functionality"""
    print(f"🔍 Analyzing project at: {project_path}")
    
    try:
        # Test project structure analysis
        structure = ProjectStructure.analyze(project_path)
        print(f"  📦 Package managers: {structure.package_managers}")
        print(f"  🔤 Languages: {structure.languages}")
        print(f"  🧪 Has tests: {structure.has_tests}")
        print(f"  📚 Has docs: {structure.has_docs}")
        print(f"  🔄 Has CI: {structure.has_ci}")
        
        # Test task analyzer
        analyzer = TaskAnalyzer(project_path)
        existing_tasks = analyzer.extract_existing_tasks()
        print(f"  📋 Existing tasks: {len(existing_tasks)}")
        
        for task in existing_tasks[:3]:  # Show first 3 tasks
            print(f"    - {task.full_name}: {task.description}")
        
        # Test recommendations
        recommendations = analyzer.get_task_recommendations()
        print(f"  💡 Recommendations: {len(recommendations)}")
        
        for rec in recommendations[:3]:  # Show first 3 recommendations
            print(f"    - {rec.task.full_name} (priority: {rec.priority}): {rec.reasoning}")
        
        # Test architecture validation
        validation = analyzer.validate_task_architecture()
        print(f"  ✅ Architecture validation:")
        print(f"    - Total tasks: {validation['total_tasks']}")
        print(f"    - Domains used: {len(validation['domains_used'])}")
        print(f"    - Issues: {len(validation['issues'])}")
        print(f"    - Suggestions: {len(validation['suggestions'])}")
        
        return {
            "success": True,
            "project_structure": {
                "package_managers": list(structure.package_managers),
                "languages": list(structure.languages),
                "has_tests": structure.has_tests,
                "has_docs": structure.has_docs,
                "has_ci": structure.has_ci
            },
            "existing_tasks": len(existing_tasks),
            "recommendations": len(recommendations),
            "validation": {
                "total_tasks": validation["total_tasks"],
                "domains_used": [d.value if hasattr(d, 'value') else str(d) for d in validation["domains_used"]],
                "issues": validation["issues"],
                "suggestions": validation["suggestions"]
            }
        }
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {"success": False, "error": str(e)}


async def test_task_creation(project_path: Path) -> Dict[str, Any]:
    """Test task creation functionality"""
    print(f"🔨 Testing task creation at: {project_path}")
    
    try:
        manager = TaskManager(project_path)
        
        # Test intelligent task creation
        result = manager.create_task_intelligently(
            task_description="Run unit tests with coverage reporting",
            suggested_name="coverage"
        )
        
        print(f"  📝 Task creation result: {result}")
        
        return result
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {"success": False, "error": str(e)}


async def test_task_tracing(project_path: Path, task_name: str = "build") -> Dict[str, Any]:
    """Test task chain tracing"""
    print(f"🔗 Testing task tracing for '{task_name}' at: {project_path}")
    
    try:
        analyzer = TaskAnalyzer(project_path)
        trace_result = analyzer.trace_task_chain(task_name)
        
        if "error" in trace_result:
            print(f"  ⚠️  {trace_result['error']}")
        else:
            print(f"  🎯 Task: {trace_result['task_name']}")
            print(f"  📊 Execution order: {trace_result['execution_order']}")
            print(f"  🔗 Dependencies: {trace_result['dependencies']}")
            print(f"  ⬆️  Dependents: {trace_result['dependents']}")
            print(f"  ⏱️  Parallel groups: {len(trace_result['parallelizable_groups'])}")
        
        return trace_result
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {"success": False, "error": str(e)}


async def main():
    """Main test runner"""
    print("🚀 Testing Wise Mise MCP Server")
    print("=" * 50)
    
    # Test with current project
    current_project = Path.cwd()
    print(f"📂 Current project: {current_project}")
    
    # Run tests
    tests = [
        ("Project Analysis", test_project_analysis(current_project)),
        ("Task Tracing", test_task_tracing(current_project)),
        ("Task Creation", test_task_creation(current_project)),
    ]
    
    results = {}
    for test_name, test_coro in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            result = await test_coro
            results[test_name] = result
            if result.get("success", True):
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"💥 {test_name} crashed: {e}")
            results[test_name] = {"success": False, "error": str(e)}
    
    # Summary
    print(f"\n📊 Test Summary:")
    print("=" * 50)
    passed = sum(1 for r in results.values() if r.get("success", True))
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check output above for details.")
    
    # Save detailed results
    results_file = Path("test_results.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"📁 Detailed results saved to: {results_file}")


if __name__ == "__main__":
    asyncio.run(main())
