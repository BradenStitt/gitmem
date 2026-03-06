"""LLM integration layer using the Anthropic SDK."""

from __future__ import annotations

import json

import anthropic

from gitmem.prompts import COMMIT_PROMPT, MERGE_PROMPT


class LLMError(Exception):
    """Raised when an LLM call fails."""


class LLMClient:
    """Thin wrapper around the Anthropic SDK for GitMem summarization."""

    def __init__(self, model: str = "claude-sonnet-4-20250514") -> None:
        self.client = anthropic.AsyncAnthropic()
        self.model = model

    async def summarize_for_commit(
        self,
        history: str,
        branch_purpose: str,
        prior_commits: str,
    ) -> dict:
        """Call LLM to produce a structured commit summary.

        Returns dict with keys: summary, progress, current_state, next_steps.
        """
        prompt = COMMIT_PROMPT.format(
            history=history,
            branch_purpose=branch_purpose,
            prior_commits=prior_commits or "(no prior commits)",
        )
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text
            return json.loads(text)
        except Exception as e:
            raise LLMError(f"Failed to summarize for commit: {e}") from e

    async def synthesize_for_merge(
        self,
        source_commits: str,
        target_commits: str,
        roadmap: str,
    ) -> dict:
        """Call LLM to synthesize merge insights.

        Returns dict with keys: summary, progress, current_state, next_steps, roadmap_update.
        """
        prompt = MERGE_PROMPT.format(
            source_commits=source_commits,
            target_commits=target_commits,
            roadmap=roadmap,
        )
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text
            return json.loads(text)
        except Exception as e:
            raise LLMError(f"Failed to synthesize for merge: {e}") from e
