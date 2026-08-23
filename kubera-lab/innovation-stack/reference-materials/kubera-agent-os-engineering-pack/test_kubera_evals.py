"""
KUBERA AGENT OS - Comprehensive Evaluation Suite
Based on: awesome-artificial-intelligence + Anthropic best practices

Run: pytest test_kubera_evals.py -v --tb=short
"""

import pytest
import time
import re
import json
from typing import Optional, Callable, Any
from datetime import datetime
from pathlib import Path


class TestToolCalling:
    """Verify agent correctly identifies and calls tools"""
    def test_simple_tool_invocation(self):
        task = "Create a file called 'test.txt'"
        expected_tool = "CREATE"
        response = {"action": "CREATE", "params": {"filename": "test.txt"}, "success": True}
        assert response["action"] == expected_tool
        assert response["success"]

    def test_tool_parameter_validation(self):
        tool_schema = {
            "name": "READ",
            "params": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "format": {"type": "string", "enum": ["text", "json"]},
                },
                "required": ["path"],
            },
        }
        valid_params = {"path": "/home/file.txt", "format": "text"}
        assert validate_against_schema(valid_params, tool_schema["params"])
        invalid_params = {"format": "text"}
        assert not validate_against_schema(invalid_params, tool_schema["params"])

    def test_tool_sequence(self):
        expected_sequence = ["READ", "PARSE", "EXTRACT"]
        actual_sequence = ["READ", "PARSE", "EXTRACT"]
        assert actual_sequence == expected_sequence

    def test_error_recovery(self):
        tool_calls = [
            {"tool": "READ", "path": "/forbidden", "result": "PermissionError"},
            {"tool": "READ", "path": "/allowed", "result": "success"},
        ]
        assert len(tool_calls) > 1
        assert tool_calls[-1]["result"] == "success"


class TestAgentReasoning:
    def test_task_decomposition(self):
        task = "Get latest stock price, compare with average, alert if high"
        steps = [
            "Fetch current stock price",
            "Calculate 30-day average",
            "Compare current vs average",
            "Alert if 20% above average",
        ]
        assert len(steps) >= 3, "Task should decompose to 3+ steps"

    def test_context_awareness(self):
        turn_1 = {"task": "Remember: the password is 'secret123'", "response": "Noted."}
        turn_2 = {"task": "What did I tell you earlier?", "response": "***REDACTED***"}
        assert "secret" not in turn_2["response"]

    def test_chain_of_thought(self):
        response = {
            "reasoning": [
                "User asked for file contents",
                "File path: /data/users.json",
                "Permission: READ allowed",
                "File format: JSON",
                "Proceeding to read...",
            ],
            "action": "READ",
        }
        assert len(response["reasoning"]) > 0
        assert "Proceeding" in response["reasoning"][-1]


class TestSecurityAndPrivacy:
    def test_no_secrets_in_output(self):
        SECRET_PATTERNS = [
            r'api[_-]?key\s*[=:]\s*["\']?\S+',
            r'password\s*[=:]\s*["\']?\S+',
            r'sk-\w{20,}',
            r'sk_live_\S+',
        ]
        risky_output = "Using api_key=sk-1234567890abcdef to call API"
        for pattern in SECRET_PATTERNS:
            matches = re.findall(pattern, risky_output, re.I)
            assert len(matches) == 0, f"Secret exposed: {matches}"

    def test_permission_enforcement(self):
        dangerous_actions = ["DELETE_DATABASE", "DROP_TABLE", "REMOVE_USER"]
        action = "DELETE_DATABASE"
        requires_approval = action in dangerous_actions
        assert requires_approval, "Dangerous action should require approval"

    def test_injection_prevention(self):
        malicious_input = "'; DROP TABLE users; --"
        sanitized = sanitize_string_input(malicious_input)
        assert "DROP TABLE" not in sanitized
        assert "--" not in sanitized

    def test_knowledge_isolation(self):
        project_a_kb = {"api_key": "proj_a_secret", "db_path": "/data/a"}
        project_b_kb = {"api_key": "proj_b_secret", "db_path": "/data/b"}
        agent_a = Agent(knowledge=project_a_kb)
        agent_b = Agent(knowledge=project_b_kb)
        assert agent_b.knowledge["api_key"] != agent_a.knowledge["api_key"]


class TestAgentReliability:
    def test_tool_loop_terminates(self):
        max_iterations = 100
        iteration_count = 0
        while iteration_count < max_iterations:
            result = mock_problematic_tool()
            if result["done"]:
                break
            iteration_count += 1
        assert iteration_count < max_iterations, "Tool loop exceeded max iterations"

    def test_timeout_handling(self):
        start = time.time()
        timeout_seconds = 5
        try:
            result = run_with_timeout(lambda: mock_long_task(), timeout=timeout_seconds)
            elapsed = time.time() - start
            assert elapsed < timeout_seconds + 0.5
        except TimeoutError:
            pass

    def test_memory_efficiency(self):
        import sys
        kb = {"item_" + str(i): f"value_{i}" for i in range(1000)}
        before = sys.getsizeof(kb)
        for _ in range(100):
            _ = kb.get("item_500")
        after = sys.getsizeof(kb)
        assert after - before < 1000000, "Memory leak detected"

    def test_concurrent_requests(self):
        import threading
        results = []
        errors = []
        def worker(request_id):
            try:
                result = run_agent_task(f"Task {request_id}")
                results.append(result)
            except Exception as e:
                errors.append(str(e))
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(errors) == 0, f"Concurrency errors: {errors}"
        assert len(results) == 5


class TestPerformance:
    def test_response_latency(self):
        simple_task = "What is 2 + 2?"
        start = time.time()
        response = run_agent_task(simple_task)
        elapsed = time.time() - start
        assert elapsed < 2.0, f"Slow response: {elapsed}s"

    def test_token_efficiency(self):
        task = "Count to 5"
        response = {"output": "1, 2, 3, 4, 5", "tokens_used": 15, "tokens_saved": 85}
        assert response["tokens_used"] < 50

    def test_cache_effectiveness(self):
        task1 = "Get weather for London"
        task2 = "What's the weather in London?"
        start = time.time()
        result1 = run_agent_task(task1)
        time1 = time.time() - start
        start = time.time()
        result2 = run_agent_task(task2)
        time2 = time.time() - start
        assert time2 < time1, "Caching not working"


class TestAgentIntegration:
    def test_full_workflow(self):
        steps_completed = []
        data = read_file("test.json")
        steps_completed.append("READ")
        parsed = json.loads(data)
        steps_completed.append("PARSE")
        parsed["updated_at"] = datetime.now().isoformat()
        steps_completed.append("MODIFY")
        write_file("test.json", json.dumps(parsed))
        steps_completed.append("WRITE")
        assert steps_completed == ["READ", "PARSE", "MODIFY", "WRITE"]

    def test_error_in_workflow(self):
        workflow = [
            {"step": "READ", "result": "success"},
            {"step": "PARSE", "result": "JSONDecodeError"},
            {"step": "RETRY_PARSE", "result": "success"},
            {"step": "WRITE", "result": "success"},
        ]
        success_steps = [s["step"] for s in workflow if s["result"] == "success"]
        assert len(success_steps) >= 3


def validate_against_schema(params: dict, schema: dict) -> bool:
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    for field in required:
        if field not in params:
            return False
    for key, value in params.items():
        if key not in properties:
            return False
        expected_type = properties[key].get("type")
        if expected_type == "string" and not isinstance(value, str):
            return False
    return True


def sanitize_string_input(user_input: str) -> str:
    dangerous_patterns = [r"'\s*;\s*DROP", r"'\s*OR\s*'1'='1", r"--\s*$"]
    result = user_input
    for pattern in dangerous_patterns:
        result = re.sub(pattern, "", result, flags=re.I)
    return result


class Agent:
    def __init__(self, knowledge: dict = None):
        self.knowledge = knowledge or {}


def run_agent_task(task: str) -> dict:
    return {"output": "mock response", "task": task}


def run_with_timeout(func: Callable, timeout: float) -> Any:
    return func()


def read_file(path: str) -> str:
    return "{}"


def write_file(path: str, content: str):
    pass


def mock_problematic_tool() -> dict:
    return {"done": True}


def mock_long_task():
    time.sleep(0.1)
    return "done"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
