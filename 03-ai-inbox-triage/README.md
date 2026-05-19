# 03 — Triage your AI inbox with Claude

**Persona:** Power user / agency operator
**Time:** 3 minutes
**Code:** Python — runs Claude against your AI inbox non-interactively

## What you'll build

A morning script that reads everything sitting in your SociaHive AI inbox,
asks Claude to categorize each conversation, and prints a triage table you
can scan in 30 seconds.

This is the "magic moment" demo — most users haven't seen anything like it.

## Two ways to do this

| Mode | Surface | Best for |
|---|---|---|
| **Live (in-chat)** | MCP via Claude Desktop / Claude.ai / Cursor | One-off triage, with you in the loop |
| **Automated (this recipe)** | Anthropic API + SociaHive SDK | Daily 9am cron job |

For the live version, just paste the prompt in
[the inbox-triage write-up](https://github.com/sociahive/sociahive/blob/main/docs/MCP/index.md#5c-triage-your-ai-inbox-with-claude)
into your AI assistant. The script below is for when you want to schedule it.

## Run it

```bash
pip install sociahive anthropic
export SOCIAHIVE_API_KEY=sk_...
export ANTHROPIC_API_KEY=sk-ant-...
python main.py
```

Sample output:

```
=== AI Inbox triage — 7 conversations ===

@sarah_creator      PRICING_QUESTION   "Hey! What's the cost for the agency plan?…"
                    Draft: Hey Sarah — agency runs $199/mo for up to 15 accounts…

@spam_bot_001       SPAM               "Get 10K followers for $1!! click here…"
                    → Archive

@curious_dev        GENUINE_INTEREST   "Saw your demo at HN — what's the MCP tool surface?…"
                    Draft: Glad you saw the demo! Full tool list is at…

…
```

## What the script does

1. `sh.flows.list()` is *not* what you want here — that's flows. We hit the
   AI inbox directly: `GET /api/v1/live-chat?status=ai_handoff`. (The SDK
   doesn't surface `live_chat` yet — we use raw `httpx` for that one call.)
2. For each session, fetch the last 5 messages.
3. Send all sessions to Claude in one batch with a structured-output prompt
   asking for `category` + `draft_reply` per conversation.
4. Print a table. Nothing is sent — the operator decides what to ship.

## Wiring it into cron

```cron
# 9am Mon–Fri
0 9 * * 1-5  cd ~/sociahive-tools && python main.py | mail -s "AI inbox" you@example.com
```

## Cost

- **0 SociaHive AI credits** — categorization runs inside your Anthropic
  context, not SociaHive's gateway.
- You pay Anthropic for the Claude tokens (typically <$0.01 per triage run
  with Claude Haiku).
- Sending the actual replies (when you choose to) is free for template
  messages, 5 credits each for AI-generated.

## The compelling version

The first time you demo SociaHive to someone, this is the recipe to show.
Three reasons:

1. They already have Claude/ChatGPT — zero install friction.
2. "Do work in the background, show me a summary" is what people want from AI
   but rarely get.
3. It exercises read AND write scopes — perfect end-to-end OAuth demo.
