"""Prompt templates for LLM summarization and synthesis."""

COMMIT_PROMPT = """\
You are a memory management system for an AI agent. Your job is to summarize \
the agent's recent work into a structured checkpoint.

## Branch Purpose
{branch_purpose}

## Prior Commits
{prior_commits}

## Recent History
{history}

## Instructions
Produce a JSON object with these exact keys:
- "summary": A concise 1-2 sentence summary of what was accomplished.
- "progress": What concrete progress was made.
- "current_state": The current state of the work.
- "next_steps": A list of 1-3 concrete next steps.

Respond with ONLY the JSON object, no markdown fencing or extra text.
"""

MERGE_PROMPT = """\
You are a memory management system for an AI agent. Your job is to synthesize \
insights from a source branch into a target branch, producing a unified summary.

## Project Roadmap
{roadmap}

## Target Branch Commits
{target_commits}

## Source Branch Commits
{source_commits}

## Instructions
Synthesize the work from the source branch into the target branch context. \
Produce a JSON object with these exact keys:
- "summary": A concise summary of what the source branch accomplished and how it integrates.
- "progress": What the merged work contributes to overall progress.
- "current_state": The unified state after merging.
- "next_steps": A list of 1-3 next steps for the target branch.
- "roadmap_update": Updated roadmap text if the merge changes project direction, \
or null if no update needed.

Respond with ONLY the JSON object, no markdown fencing or extra text.
"""
