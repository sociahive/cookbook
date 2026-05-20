# 03 — Daily performance recap with Claude

**Persona:** Power user / agency operator
**Time:** 2 minutes
**Code:** none — pure prompt via MCP

## What you'll build

A morning brief delivered by your AI assistant — which flows underperformed yesterday, which posts overperformed, what's queued to publish today, and what action to take. No clicks, no SQL, no dashboard hunting.

## Prerequisites

An MCP client connected to SociaHive — see the [MCP setup guide](https://docs.sociahive.com/setup-guide).

## The prompt

Paste this into Claude / ChatGPT / Cursor:

> Give me a brief on yesterday's SociaHive performance. Steps:
>
> 1. List my flows with stats for the last 24 hours.
> 2. Pull analytics overview for the same window across all platforms.
> 3. List anything scheduled to publish today.
> 4. Output a 6-line summary:
>    - Top performing flow (by completions) and why
>    - Worst performing flow (by error rate) and what to investigate
>    - Top post (by engagement) and what it had in common
>    - Total reach / impressions across platforms vs the previous day
>    - Anything queued for today I should review before it ships
>    - One concrete action you'd recommend
>
> Be concise — under 200 words total. Do not modify anything.

## What the AI does under the hood

```
1. list_flows_with_stats     → flow performance + error counts
2. get_analytics_overview    → cross-platform impressions / engagement
3. list_scheduled_posts      → today's queue
```

All three are read-only tools — no risk of accidental changes, no confirmation prompts, no destructive operations.

## Variations

| Tweak | Add to your prompt |
|---|---|
| Weekly instead of daily | "...for the last 7 days instead of 24 hours" |
| Per-platform | "Split the summary per platform — Instagram / Facebook / LinkedIn" |
| Cron-style | Put it in a 9am calendar invite that says "ask Claude" — same prompt |
| Slack-able | "Format the summary as a Slack message with emoji headings" |

## Cost

- **0 SociaHive AI credits** — all three tools are read-only metrics endpoints, not metered.
- Whatever your AI assistant charges for its own tokens (usually pennies per run with Claude Haiku or GPT-4o-mini).

## Why this beats the dashboard

The dashboard shows you data. The AI tells you what to *do* about it — which is what you actually wanted when you opened the dashboard at 9am.
