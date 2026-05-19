"""Triage the SociaHive AI inbox with Claude — non-interactive.

Usage:
    pip install sociahive anthropic httpx
    export SOCIAHIVE_API_KEY=sk_...
    export ANTHROPIC_API_KEY=sk-ant-...
    python main.py

Reads conversations flagged for human review, asks Claude to categorize and
draft replies, prints a triage table. Does NOT send anything — review the
drafts in the SociaHive inbox and send manually.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

import httpx
from anthropic import Anthropic

API_BASE = os.environ.get("SOCIAHIVE_API_URL", "https://www.sociahive.com/api/v1")
API_KEY = os.environ["SOCIAHIVE_API_KEY"]
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

CATEGORIES = (
    "SPAM",
    "PRICING_QUESTION",
    "BUG_REPORT",
    "FEATURE_REQUEST",
    "FOLLOWUP_NEEDED",
    "GENUINE_INTEREST",
)


def list_handoff_sessions() -> list[dict[str, Any]]:
    with httpx.Client(base_url=API_BASE, headers=HEADERS, timeout=30.0) as c:
        resp = c.get("/live-chat", params={"status": "ai_handoff", "limit": 50})
        resp.raise_for_status()
        return resp.json().get("data", [])


def fetch_history(session_id: str) -> list[dict[str, Any]]:
    with httpx.Client(base_url=API_BASE, headers=HEADERS, timeout=30.0) as c:
        resp = c.get(f"/live-chat/{session_id}/messages", params={"limit": 5})
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        return resp.json().get("data", [])


def triage(sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ask Claude to categorize + draft a reply for each session."""
    client = Anthropic()
    summaries = []
    for s in sessions:
        history = fetch_history(s["id"])
        summaries.append({
            "id": s["id"],
            "contact": s.get("contact_handle") or s.get("contact_id") or "unknown",
            "last_messages": [
                {"role": m.get("role"), "text": (m.get("text") or "")[:200]}
                for m in history[-5:]
            ],
        })

    prompt = f"""You are triaging a SociaHive AI inbox. For each conversation,
output JSON: {{ "id": str, "category": one of {list(CATEGORIES)},
"draft_reply": str (empty string if category is SPAM or no reply needed) }}.

Voice for drafts: concise, warm, no exclamation marks.

Conversations:
{json.dumps(summaries, indent=2)}

Respond with ONLY a JSON array — no prose, no markdown fences."""

    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    text = "".join(block.text for block in resp.content if hasattr(block, "text"))
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"Claude returned non-JSON: {exc}", file=sys.stderr)
        print(text, file=sys.stderr)
        return []


def main() -> None:
    sessions = list_handoff_sessions()
    if not sessions:
        print("Inbox clean — no conversations need human review.")
        return

    print(f"=== AI Inbox triage — {len(sessions)} conversations ===\n")

    decisions = triage(sessions)
    by_id = {d["id"]: d for d in decisions}

    for s in sessions:
        d = by_id.get(s["id"], {"category": "FOLLOWUP_NEEDED", "draft_reply": ""})
        contact = s.get("contact_handle") or s.get("contact_id") or "unknown"
        category = d.get("category", "?")
        last = s.get("last_message_preview") or ""
        print(f"{contact:<22} {category:<18} \"{last[:60]}…\"")
        if d.get("draft_reply"):
            print(f"{'':<22} Draft: {d['draft_reply']}")
        elif category == "SPAM":
            print(f"{'':<22} → Archive")
        print()


if __name__ == "__main__":
    main()
