# 🔧 KUBERA AGENT OS 1.0: Integration Checklist

**Apply awesome-ai best practices to your codebase**

---

## 📋 STEP 1: Copy Production Components

```bash
# Copy the new module to your project
cp kubera_production_components.py \
   your_kubera_project/kubera_agent_os/production.py
```

---

## 📋 STEP 2: Update `execution_engine.py`

### Add Imports
```python
from kubera_agent_os.production import (
    PermissionManager,
    PrivacyGate,
    ToolValidator,
    ToolLoopGuard,
    EvidenceLedger,
)
```

### Update `execute_tool()` Function
```python
def execute_tool(
    tool_name: str,
    params: dict,
    tool_schema: dict,
    permission: str = "read"
) -> any:
    """Execute tool with all safeguards"""
    
    # 1. VALIDATE schema
    is_valid, error = ToolValidator.validate(
        tool_name, params, tool_schema
    )
    if not is_valid:
        return {"error": f"Invalid params: {error}"}
    
    # 2. CHECK permissions
    if not self.permission_manager.can_execute(
        tool_name, permission, params
    ):
        return {"error": "Permission denied"}
    
    # 3. REDACT secrets
    safe_params = PrivacyGate.sanitize_params(params)
    
    # 4. LOOP guard
    self.loop_guard.step()
    
    # 5. EXECUTE
    try:
        result = call_tool(tool_name, safe_params)
        
        # 6. LOG to ledger
        self.ledger.log_action("tool_success", {
            "tool": tool_name,
            "result": str(result)[:100]
        })
        
        return result
    
    except Exception as e:
        # 7. RECORD failure
        self.failure_memory.record_failure(
            tool_name,
            type(e).__name__,
            str(e),
            params
        )
        
        # 8. RETRY if applicable
        if self.failure_memory._suggest_retry(type(e).__name__):
            return {"retry": True, "error": str(e)}
        
        return {"error": str(e)}
```

### Add to `__init__`
```python
class ExecutionEngine:
    def __init__(self, ...):
        # ... existing code ...
        self.permission_manager = PermissionManager()
        self.loop_guard = ToolLoopGuard()
        self.ledger = EvidenceLedger()
        self.failure_memory = FailureMemory()
```

---

## 📋 STEP 3: Update `agent_loop.py`

### Add Knowledge Management
```python
from kubera_agent_os.production import PersistentKnowledgeStore

class AgentLoop:
    def __init__(self, model: str):
        self.model = model
        self.kb = PersistentKnowledgeStore()
    
    def run(self, task: str) -> dict:
        """Main agent loop with knowledge"""
        
        # 1. BUILD system prompt with known facts
        kb_context = self.kb.get_context()
        system_prompt = f"""You are KUBERA agent.
        
Known facts:
{kb_context}

Available tools:
{self._format_tool_list()}"""
        
        messages = [{"role": "user", "content": task}]
        
        # 2. LOOP with knowledge
        while len(messages) < 20:  # Prevent infinite loops
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                tools=self.tools,
                messages=messages
            )
            
            # 3. CHECK if done
            if response.stop_reason != "tool_use":
                return {
                    "output": response.content,
                    "success": True,
                    "facts_learned": self.kb.knowledge
                }
            
            # 4. EXTRACT and execute tools
            for content in response.content:
                if content.type == "tool_use":
                    result = self.execution_engine.execute_tool(
                        content.name,
                        content.input
                    )
                    
                    # 5. LEARN from results
                    self._learn_from_result(content.name, result)
            
            # Add response and result to messages
            messages.append(response)
            messages.append({
                "role": "user",
                "content": [{"type": "tool_result", "result": str(result)}]
            })
        
        return {"error": "Max iterations reached", "success": False}
    
    def _learn_from_result(self, tool_name: str, result: dict):
        """Extract and store learnings"""
        if "schema" in result:
            self.kb.add_fact(f"{tool_name}_schema", result["schema"])
        
        if "available_paths" in result:
            self.kb.add_fact(f"{tool_name}_paths", result["available_paths"])
```

---

## 📋 STEP 4: Update `tool_runtime.py`

### Add Tool Registration with Schemas
```python
from kubera_agent_os.production import ToolValidator

class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.register_default_tools()
    
    def register(self, name: str, schema: dict, handler: callable):
        """Register tool with schema"""
        self.tools[name] = {
            "schema": schema,
            "handler": handler
        }
    
    def register_default_tools(self):
        """Built-in tools"""
        
        # READ tool
        self.register(
            "READ",
            schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "format": {
                        "type": "string",
                        "enum": ["text", "json", "yaml"]
                    }
                },
                "required": ["path"]
            },
            handler=self._handle_read
        )
        
        # CREATE tool
        self.register(
            "CREATE",
            schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            },
            handler=self._handle_create
        )
        
        # ACT tool (external action)
        self.register(
            "ACT",
            schema={
                "type": "object",
                "properties": {
                    "action": {"type": "string"},
                    "params": {"type": "object"}
                },
                "required": ["action"]
            },
            handler=self._handle_act
        )
    
    def _handle_read(self, path: str, format: str = "text"):
        """Read file"""
        # ... implementation ...
        pass
    
    def _handle_create(self, path: str, content: str):
        """Create file"""
        # ... implementation ...
        pass
    
    def _handle_act(self, action: str, params: dict):
        """External action (requires approval)"""
        # ... implementation ...
        pass
```

---

## 📋 STEP 5: Update `cli.py`

### Add Permission Approval UI
```python
from kubera_agent_os.production import PermissionManager

class CLI:
    def __init__(self):
        self.agent = Agent()
        self.agent.execution_engine.permission_manager = \
            PermissionManager(human_approver=self._human_approver)
    
    def _human_approver(self, tool: str, action: str, params: dict) -> bool:
        """Interactive approval prompt"""
        print(f"\n⚠️  REQUIRES APPROVAL")
        print(f"   Tool: {tool}")
        print(f"   Action: {action}")
        print(f"   Parameters: {json.dumps(params, indent=2)}")
        
        response = input("\n   Approve? (yes/no): ").strip().lower()
        return response == "yes"
    
    def run(self, task: str, require_approval: bool = False):
        """Run agent task"""
        if require_approval and task.upper().startswith(("DELETE", "DROP", "REMOVE")):
            print("⚠️  Dangerous action detected. Human approval required.")
        
        result = self.agent.run(task)
        
        print(f"\n✅ Result: {result['output']}")
        print(f"📋 Actions: {len(result.get('actions', []))}")
        print(f"💡 Learned: {len(result.get('facts_learned', {}))} facts")
```

---

## 📋 STEP 6: Add Evals

### Run Tests
```bash
# Copy evals
cp test_kubera_evals.py your_kubera_project/tests/

# Run all tests
pytest tests/test_kubera_evals.py -v

# Run specific category
pytest tests/test_kubera_evals.py::TestSecurityAndPrivacy -v

# With coverage
pytest tests/test_kubera_evals.py --cov=kubera_agent_os
```

### Add CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Test KUBERA

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - run: pip install -r requirements.txt
      - run: pytest tests/test_kubera_evals.py -v --tb=short
```

---

## 📋 STEP 7: Local Testing (Windows 10 + Ollama)

### Install Ollama
```powershell
# Download from https://ollama.ai
# Run installer (admin)

# Test
ollama --version

# Start server (in another terminal)
ollama serve
```

### Start KUBERA Locally
```powershell
# Clone repo
git clone https://github.com/jobkubera-lab/kubera-local-ai
cd kubera-local-ai

# Install
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Configure for local Ollama
$env:OLLAMA_HOST="http://localhost:11434"
$env:KUBERA_MODEL="mistral:7b"

# Run
python -m kubera_agent_os.cli "What can you do?"
```

### Test Locally with Evals
```powershell
pytest tests/test_kubera_evals.py -v
pytest tests/test_agent_evals.py --tb=short
```

---

## 📋 STEP 8: Verify Compliance

### Checklist Before Release 1.0.1

- [ ] `execution_engine.py` has ToolValidator
- [ ] `execution_engine.py` has PermissionManager
- [ ] `execution_engine.py` has PrivacyGate
- [ ] `agent_loop.py` has PersistentKnowledgeStore
- [ ] `tool_runtime.py` has schema validation
- [ ] All tools registered with schemas
- [ ] Tests pass: `pytest tests/ -v`
- [ ] Evidence ledger works: `python -m kubera_agent_os.cli --log`
- [ ] Failures tracked: `.kubera/failures.json` exists
- [ ] No secrets in logs: Check `.kubera/evidence.jsonl`
- [ ] CLI supports `--require-approval` flag
- [ ] Windows install script tested

---

## 📋 STEP 9: Documentation Updates

### Update README.md
```markdown
# KUBERA AGENT OS 1.0.1

## Safety Features
- ✅ Permission model (READ/CREATE/ACT/ADMIN)
- ✅ Privacy gate (redacts secrets)
- ✅ Tool validation (JSON schema)
- ✅ Loop guard (max iterations + timeout)
- ✅ Evidence ledger (audit log)
- ✅ Failure memory (error tracking)
- ✅ Persistent knowledge (learns between sessions)
```

---

## 📋 STEP 10: Deploy & Monitor

### Production Checklist
```bash
# 1. Test everything locally
pytest tests/ -v --tb=short

# 2. Check for secrets
grep -r "sk-\|api_key\|password" .kubera/ || echo "✅ No secrets found"

# 3. Verify evidence ledger
cat .kubera/evidence.jsonl | wc -l

# 4. Check failure rate
python -c "import json; print(json.load(open('.kubera/failures.json')))"

# 5. Build release
python setup.py sdist bdist_wheel

# 6. Tag version
git tag v1.0.1
git push origin v1.0.1

# 7. Deploy
pip install dist/kubera_agent_os-1.0.1-py3-none-any.whl
```

---

## 🎯 Quick Start (TL;DR)

```bash
# 1. Copy files
cp kubera_production_components.py \
   kubera_agent_os/production.py

# 2. Update imports in:
#    - execution_engine.py
#    - agent_loop.py
#    - tool_runtime.py
#    - cli.py

# 3. Add evals
cp test_kubera_evals.py tests/

# 4. Test locally
pytest tests/ -v

# 5. Deploy
git commit -am "feat: add production safety components"
git push
```

---

## ❓ Questions?

- **Anthropic Guide:** https://www.anthropic.com/engineering/building-effective-agents
- **OpenAI Guide:** https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- **awesome-ai:** https://github.com/owainlewis/awesome-artificial-intelligence

---

**Ready to ship KUBERA 1.0.1? 🚀**
