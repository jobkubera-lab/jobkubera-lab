"""
KUBERA AGENT OS - Production-Ready Components
Based on awesome-artificial-intelligence + Anthropic engineering best practices

Add these to your codebase:
- Copy to kubera_agent_os/
- Update imports in agent_loop.py and execution_engine.py
"""

import threading
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Callable, Dict
from enum import Enum


class ToolPermission(Enum):
    """Tool permission levels"""
    READ = "read"
    CREATE = "create"
    ACT = "act"
    ADMIN = "admin"


class PermissionManager:
    """Manage tool permissions and human approval"""
    REQUIRES_APPROVAL = {ToolPermission.ACT, ToolPermission.ADMIN}

    def __init__(self, human_approver: Optional[Callable] = None):
        self.human_approver = human_approver
        self.approval_log = []

    def can_execute(self, tool_name: str, permission: ToolPermission, params: Dict) -> bool:
        if permission not in self.REQUIRES_APPROVAL:
            return True
        if self.human_approver is None:
            raise PermissionError(
                f"Tool '{tool_name}' requires {permission.value} approval but no approver is configured"
            )
        approval = self.human_approver(tool=tool_name, action=permission.value, params=params)
        self.approval_log.append({
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "permission": permission.value,
            "approved": bool(approval),
            "params": params,
        })
        return bool(approval)

    def get_approval_history(self) -> list:
        return self.approval_log


class PrivacyGate:
    """Filter sensitive data before tool execution"""
    SENSITIVE_PATTERNS = [
        r'api[_-]?key\s*[=:]\s*["\']?(\S+)',
        r'password\s*[=:]\s*["\']?(\S+)',
        r'token\s*[=:]\s*["\']?(\S+)',
        r'authorization\s*[=:]\s*["\']?(\S+)',
        r'secret\s*[=:]\s*["\']?(\S+)',
        r'bearer\s+(\S+)',
        r'sk_live_\S+',
        r'sk_test_\S+',
        r'sk-\w{20,}',
    ]

    @classmethod
    def sanitize_params(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = {}
        for key, value in params.items():
            if isinstance(value, str):
                is_secret = any(re.search(pattern, value, re.I) for pattern in cls.SENSITIVE_PATTERNS)
                sanitized[key] = "***REDACTED***" if is_secret else value
            elif isinstance(value, dict):
                sanitized[key] = cls.sanitize_params(value)
            elif isinstance(value, list):
                sanitized[key] = [cls.sanitize_params(item) if isinstance(item, dict) else item for item in value]
            else:
                sanitized[key] = value
        return sanitized

    @classmethod
    def redact_output(cls, output: str) -> str:
        redacted = output
        for pattern in cls.SENSITIVE_PATTERNS:
            redacted = re.sub(pattern, r'***REDACTED***', redacted, flags=re.I)
        return redacted


class ToolValidator:
    """Validate tool calls against schema"""
    @staticmethod
    def validate(tool_name: str, params: Dict[str, Any], schema: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        required = schema.get("required", [])
        for field in required:
            if field not in params:
                return False, f"Missing required field: {field}"
        properties = schema.get("properties", {})
        for key, value in params.items():
            if key not in properties:
                continue
            prop_schema = properties[key]
            expected_type = prop_schema.get("type")
            if expected_type == "string" and not isinstance(value, str):
                return False, f"Field '{key}' must be string, got {type(value)}"
            if expected_type == "number" and not isinstance(value, (int, float)):
                return False, f"Field '{key}' must be number, got {type(value)}"
            if expected_type == "boolean" and not isinstance(value, bool):
                return False, f"Field '{key}' must be boolean, got {type(value)}"
            if expected_type == "array" and not isinstance(value, list):
                return False, f"Field '{key}' must be array, got {type(value)}"
            if "enum" in prop_schema and value not in prop_schema["enum"]:
                return False, f"Field '{key}' must be one of {prop_schema['enum']}"
        return True, None


class EvidenceLedger:
    """Concurrent-safe action audit log"""
    def __init__(self, log_file: str = ".kubera/evidence.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log_action(self, action_type: str, details: Dict[str, Any], thread_id: Optional[str] = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": action_type,
            "thread": thread_id or threading.current_thread().name,
            **details,
        }
        with self._lock:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + "\n")

    def query(self, action_type: Optional[str] = None, limit: int = 100) -> list:
        with self._lock:
            if not self.log_file.exists():
                return []
            entries = []
            with open(self.log_file) as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        entry = json.loads(line)
                        if action_type is None or entry.get("type") == action_type:
                            entries.append(entry)
                    except json.JSONDecodeError:
                        continue
            return entries[-limit:]


class FailureMemory:
    """Remember tool failures for better error recovery"""
    def __init__(self, memory_file: str = ".kubera/failures.json"):
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._load()

    def _load(self):
        if self.memory_file.exists():
            with open(self.memory_file) as f:
                self.failures = json.load(f)
        else:
            self.failures = {}

    def record_failure(self, tool_name: str, error_type: str, error_msg: str, params: Dict):
        if tool_name not in self.failures:
            self.failures[tool_name] = []
        self.failures[tool_name].append({
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_msg": error_msg,
            "params_summary": str(params)[:100],
            "retry_suggested": self._suggest_retry(error_type),
        })
        self._save()

    def _suggest_retry(self, error_type: str) -> bool:
        retryable = {"TimeoutError", "ConnectionError", "HTTPError"}
        return error_type in retryable

    def _save(self):
        with self._lock:
            with open(self.memory_file, 'w') as f:
                json.dump(self.failures, f, indent=2)

    def get_failures(self, tool_name: str) -> list:
        return self.failures.get(tool_name, [])

    def is_tool_failing(self, tool_name: str, threshold: int = 3) -> bool:
        failures = self.get_failures(tool_name)
        one_hour_ago = datetime.now().timestamp() - 3600
        recent_failures = 0
        for failure in failures:
            ts = datetime.fromisoformat(failure["timestamp"]).timestamp()
            if ts > one_hour_ago:
                recent_failures += 1
        return recent_failures >= threshold


class PersistentKnowledgeStore:
    """Learn and remember facts between sessions"""
    def __init__(self, kb_file: str = ".kubera/knowledge.json"):
        self.kb_file = Path(kb_file)
        self.kb_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._load()

    def _load(self):
        if self.kb_file.exists():
            with open(self.kb_file) as f:
                self.knowledge = json.load(f)
        else:
            self.knowledge = {}

    def add_fact(self, key: str, value: Any, ttl: Optional[int] = None):
        entry = {"value": value, "learned_at": datetime.now().isoformat()}
        if ttl:
            entry["expires_at"] = datetime.now().timestamp() + ttl
        with self._lock:
            self.knowledge[key] = entry
            self._save()

    def recall(self, key: str) -> Optional[Any]:
        if key not in self.knowledge:
            return None
        entry = self.knowledge[key]
        if "expires_at" in entry and datetime.now().timestamp() > entry["expires_at"]:
            return None
        return entry["value"]

    def get_context(self) -> str:
        facts = []
        for key, data in self.knowledge.items():
            value = data.get("value")
            if isinstance(value, dict):
                facts.append(f"- {key}: {json.dumps(value, indent=2)}")
            else:
                facts.append(f"- {key}: {value}")
        return "\n".join(facts) if facts else "No known facts"

    def _save(self):
        with open(self.kb_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)


class ToolLoopGuard:
    """Prevent agent from getting stuck in tool loops"""
    def __init__(self, max_iterations: int = 100, timeout_seconds: float = 60):
        self.max_iterations = max_iterations
        self.timeout_seconds = timeout_seconds
        self.iteration_count = 0
        self.start_time = None

    def start(self):
        self.iteration_count = 0
        self.start_time = datetime.now()

    def step(self):
        self.iteration_count += 1
        if self.iteration_count > self.max_iterations:
            raise RuntimeError(f"Tool loop exceeded max iterations ({self.max_iterations})")
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed > self.timeout_seconds:
            raise TimeoutError(f"Tool loop exceeded timeout ({self.timeout_seconds}s)")

    def get_stats(self) -> Dict:
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        return {
            "iterations": self.iteration_count,
            "elapsed_seconds": elapsed,
            "max_iterations": self.max_iterations,
            "timeout_seconds": self.timeout_seconds,
        }
