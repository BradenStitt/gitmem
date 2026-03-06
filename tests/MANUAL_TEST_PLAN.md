# GitMem Manual Test Plan

## Prerequisites

```bash
uv sync --all-extras
```

Ensure `ANTHROPIC_API_KEY` is set for tests that use the real LLM (Section 3).

---

## 1. Python Package — Core Workflow (No LLM)

### 1.1 Initialize Workspace

```python
from gitmem import GitMem

gm = GitMem(root="/tmp/gitmem-test")
gm.init()
```

**Verify:**
- [ ] `/tmp/gitmem-test/.gitmem/` directory exists
- [ ] `/tmp/gitmem-test/.gitmem/HEAD` contains `main`
- [ ] `/tmp/gitmem-test/.gitmem/main.md` contains `# Project Roadmap`
- [ ] `/tmp/gitmem-test/.gitmem/branches/main/commit.md` exists (empty)
- [ ] `/tmp/gitmem-test/.gitmem/branches/main/log.md` exists (empty)
- [ ] `/tmp/gitmem-test/.gitmem/branches/main/metadata.yaml` exists with status `active`

### 1.2 Double Init Fails

```python
gm.init()  # Should raise WorkspaceExistsError
```

**Verify:**
- [ ] Raises `gitmem.errors.WorkspaceExistsError`

### 1.3 Log Entries

```python
gm.log("Started project analysis")
gm.log("Reviewed codebase structure")
```

**Verify:**
- [ ] `branches/main/log.md` contains both entries

### 1.4 Manual Commit (No LLM)

```python
import asyncio
entry = asyncio.run(gm.commit(history="Analyzed codebase", message="Manual checkpoint"))
print(entry.id, entry.summary)
```

**Verify:**
- [ ] Returns `CommitEntry` with `id="C-001"`
- [ ] `branches/main/commit.md` contains the serialized commit
- [ ] No API call was made (no ANTHROPIC_API_KEY needed)

### 1.5 Branch

```python
meta = gm.branch("experiment", "Try alternative approach")
print(meta.name, meta.parent, meta.status)
```

**Verify:**
- [ ] HEAD now reads `experiment`
- [ ] `branches/experiment/` directory exists with all files
- [ ] `metadata.yaml` has `parent: main`, `status: active`
- [ ] `commit.md` contains the last commit from main (C-001)

### 1.6 Checkout

```python
gm.checkout("main")
assert gm.workspace.read_head() == "main"
gm.checkout("experiment")
assert gm.workspace.read_head() == "experiment"
```

**Verify:**
- [ ] HEAD switches correctly
- [ ] Checking out nonexistent branch raises `BranchNotFoundError`

### 1.7 Context at All Resolutions

```python
gm.checkout("main")

# Low — project roadmap
ctx = gm.context(resolution="low")
print(ctx.source, ctx.content[:100])

# Medium — commit summaries
ctx = gm.context(resolution="medium")
print(ctx.source, ctx.content[:100])

# High — execution log
ctx = gm.context(resolution="high")
print(ctx.source, ctx.content[:100])
```

**Verify:**
- [ ] Low returns `main.md` content
- [ ] Medium returns formatted commit summaries
- [ ] High returns log entries
- [ ] Default (no args) returns medium

### 1.8 Context Query Filtering

```python
asyncio.run(gm.commit(history="work", message="Database migration complete"))
ctx = gm.context(resolution="medium", query="database")
print(ctx.content)  # Should only show database-related entries
```

**Verify:**
- [ ] Only lines containing "database" (case-insensitive) are returned

---

## 2. MCP Server

### 2.1 Launch Server

```bash
uv run gitmem-mcp
```

**Verify:**
- [ ] Server starts without errors
- [ ] Logs indicate it's listening (stdio transport by default)

### 2.2 Claude Code / MCP Client Integration

Add to your Claude Code MCP config (`~/.claude/mcp_servers.json` or equivalent):

```json
{
  "gitmem": {
    "command": "uv",
    "args": ["--directory", "/path/to/gitmem", "run", "gitmem-mcp"],
    "env": {
      "ANTHROPIC_API_KEY": "your-key-here"
    }
  }
}
```

Then in Claude Code, verify these tools are available:
- [ ] `gitmem_init`
- [ ] `gitmem_commit`
- [ ] `gitmem_branch`
- [ ] `gitmem_merge`
- [ ] `gitmem_context`
- [ ] `gitmem_checkout`
- [ ] `gitmem_log`

### 2.3 MCP Workflow

Using Claude Code or any MCP client:

1. `gitmem_init(root="/tmp/mcp-test")` → workspace created
2. `gitmem_log(entry="Testing MCP", root="/tmp/mcp-test")` → appended
3. `gitmem_commit(history="test", message="MCP test commit", root="/tmp/mcp-test")` → C-001
4. `gitmem_branch(name="feature", purpose="Test feature", root="/tmp/mcp-test")` → created
5. `gitmem_checkout(branch="main", root="/tmp/mcp-test")` → switched
6. `gitmem_context(resolution="low", root="/tmp/mcp-test")` → roadmap
7. `gitmem_context(resolution="medium", root="/tmp/mcp-test")` → commits

**Verify:**
- [ ] Each tool returns a descriptive string (not a crash)
- [ ] Error cases return `"Error: ..."` strings

---

## 3. LLM Integration (Requires ANTHROPIC_API_KEY)

### 3.1 LLM Commit Summarization

```python
import asyncio, os
os.environ["ANTHROPIC_API_KEY"] = "your-key"

from gitmem import GitMem
gm = GitMem(root="/tmp/gitmem-llm-test")
gm.init()

entry = asyncio.run(gm.commit(
    history="Analyzed the user authentication module. Found that session tokens "
            "expire after 30 minutes. Refactored the token refresh logic to use "
            "sliding window expiration. Updated 3 files: auth.py, middleware.py, "
            "and tests/test_auth.py."
))
print(f"ID: {entry.id}")
print(f"Summary: {entry.summary}")
print(f"Progress: {entry.progress}")
print(f"State: {entry.current_state}")
print(f"Next: {entry.next_steps}")
```

**Verify:**
- [ ] Returns a structured `CommitEntry` with meaningful content
- [ ] `summary` is a concise 1-2 sentence description
- [ ] `next_steps` is a non-empty list of actionable items
- [ ] Entry is persisted to `commit.md`

### 3.2 LLM Merge Synthesis

```python
# Continue from 3.1
gm.branch("token-refactor", "Improve token handling")
asyncio.run(gm.commit(
    history="Implemented sliding window tokens, added refresh endpoint",
    message="Token refactor complete"
))

gm.checkout("main")
summary = asyncio.run(gm.merge(source="token-refactor"))
print(f"Merge summary: {summary}")
print(f"Roadmap: {gm.workspace.read_main()[:200]}")
```

**Verify:**
- [ ] Merge commit is appended to main's `commit.md`
- [ ] Source branch metadata status is now `merged`
- [ ] `main.md` may be updated if LLM determines roadmap changes
- [ ] Merge summary is coherent and references the source branch work

---

## 4. Persistence / Session Continuity

### 4.1 Cross-Session State

```python
# Session 1
from gitmem import GitMem
gm1 = GitMem(root="/tmp/gitmem-persist")
gm1.init()
import asyncio
asyncio.run(gm1.commit(history="session 1 work", message="Session 1 done"))

# Session 2 (new process or new instance)
gm2 = GitMem(root="/tmp/gitmem-persist")
ctx = gm2.context(resolution="medium")
print(ctx.content)
```

**Verify:**
- [ ] Session 2 sees Session 1's commit
- [ ] All workspace files are human-readable plain text

### 4.2 Inspect Workspace Files

```bash
cat /tmp/gitmem-persist/.gitmem/HEAD
cat /tmp/gitmem-persist/.gitmem/main.md
cat /tmp/gitmem-persist/.gitmem/branches/main/commit.md
cat /tmp/gitmem-persist/.gitmem/branches/main/log.md
cat /tmp/gitmem-persist/.gitmem/branches/main/metadata.yaml
```

**Verify:**
- [ ] HEAD is plain text branch name
- [ ] commit.md is JSON blocks separated by `---`
- [ ] metadata.yaml is valid YAML
- [ ] All files are human-readable

---

## 5. Automated Test Suite

```bash
# Full test suite
uv run pytest tests/ -v

# Lint
uv run ruff check src/ tests/
```

**Expected:**
- [ ] 55 tests pass
- [ ] 0 lint errors

### Test Coverage by Feature

| Test File | Feature | Tests |
|-----------|---------|-------|
| `test_workspace.py` | F-001 Workspace | 20 |
| `test_commit.py` | F-002 COMMIT | 4 |
| `test_branch.py` | F-003 BRANCH | 5 |
| `test_merge.py` | F-004 MERGE | 4 |
| `test_context.py` | F-005 CONTEXT | 8 |
| `test_mcp_server.py` | F-006 MCP (direct) | 6 |
| `test_mcp_protocol.py` | F-006 MCP (protocol) | 5 |
| `test_integration.py` | E2E lifecycle | 3 |
| **Total** | | **55** |

---

## 6. Cleanup

```bash
rm -rf /tmp/gitmem-test /tmp/gitmem-llm-test /tmp/gitmem-persist /tmp/mcp-test
```
