# gitmem

Version-controlled memory system for LLM agents. Gives AI agents persistent, structured memory using Git-like operations.

## The Problem

LLM agents working on long tasks face:
- **Context overflow** — conversations grow beyond the context window
- **Context decay** — important early decisions get lost
- **No exploration** — can't try alternatives without losing current progress
- **Session breaks** — restarting means re-explaining everything

## How It Works

GitMem creates a `.gitmem/` workspace in your project with Git-inspired operations:

| Command | What it does |
|---------|-------------|
| `init` | Create a `.gitmem/` workspace |
| `commit` | LLM-summarized checkpoint of progress |
| `branch` | Fork a reasoning path to explore alternatives |
| `merge` | LLM-synthesized integration of branch insights |
| `context` | Retrieve memory at low/medium/high resolution |
| `checkout` | Switch between branches |
| `log` | Append execution trace entries |

## Install

```bash
pip install gitmem
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add gitmem
```

For MCP server support:

```bash
pip install gitmem[mcp]
```

## Quick Start

### Python API

```python
import asyncio
from gitmem import GitMem

gm = GitMem(root="./my-project")
gm.init()

# Log work as you go
gm.log("Analyzed authentication module")
gm.log("Found token expiration bug")

# Commit a checkpoint (uses LLM to summarize)
entry = asyncio.run(gm.commit(history="Found and fixed token expiration bug in auth.py"))
print(entry.summary)  # "Fixed token expiration bug in authentication module"

# Or commit with a manual message (no LLM needed)
entry = asyncio.run(gm.commit(history="n/a", message="Manual checkpoint"))

# Branch to explore an alternative
gm.branch("refactor-tokens", "Try sliding window token expiration")
asyncio.run(gm.commit(history="Implemented sliding window approach", message="Sliding window done"))

# Switch back and merge
gm.checkout("main")
summary = asyncio.run(gm.merge(source="refactor-tokens"))
print(summary)  # LLM-synthesized merge summary

# Retrieve context at different resolutions
ctx = gm.context(resolution="low")    # Project roadmap
ctx = gm.context(resolution="medium") # Commit summaries
ctx = gm.context(resolution="high")   # Full execution traces
ctx = gm.context(query="auth")        # Filter by keyword
```

### MCP Server

GitMem ships as an MCP server compatible with Claude Code, Claude Desktop, and any MCP client.

**Claude Code** — add to `~/.claude/mcp_servers.json`:

```json
{
  "gitmem": {
    "command": "uvx",
    "args": ["gitmem[mcp]"],
    "env": {
      "ANTHROPIC_API_KEY": "your-key-here"
    }
  }
}
```

**Claude Desktop** — add to your config:

```json
{
  "mcpServers": {
    "gitmem": {
      "command": "uvx",
      "args": ["gitmem[mcp]"],
      "env": {
        "ANTHROPIC_API_KEY": "your-key-here"
      }
    }
  }
}
```

This exposes 7 tools: `gitmem_init`, `gitmem_commit`, `gitmem_branch`, `gitmem_merge`, `gitmem_context`, `gitmem_checkout`, `gitmem_log`.

## Configuration

GitMem requires an `ANTHROPIC_API_KEY` environment variable for LLM-powered operations (`commit` without a manual message, and `merge`). Get one at [console.anthropic.com](https://console.anthropic.com).

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

The default model is `claude-sonnet-4-20250514`. You can change it:

```python
gm = GitMem(root=".", model="claude-haiku-4-5-20251001")
```

## Workspace Structure

```
.gitmem/
├── main.md                 # Project roadmap (low-res context)
├── HEAD                    # Current branch name
└── branches/
    └── main/
        ├── commit.md       # Append-only commit log (medium-res context)
        ├── log.md          # Execution traces (high-res context)
        └── metadata.yaml   # Branch metadata
```

All files are human-readable plain text. No binary formats, no database.

## Development

```bash
git clone https://github.com/BradenStitt/gitmem.git
cd gitmem
uv sync --all-extras
uv run pytest tests/ -v
uv run ruff check src/ tests/
```

## License

MIT
