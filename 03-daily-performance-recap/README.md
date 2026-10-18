# 03: Daily performance recap from your AI tool

**Persona:** Power user / agency operator
**Time:** 2 minutes
**Code:** none. You prompt your AI tool over MCP.

## What you'll build

A short brief from your AI assistant: which flows underperformed yesterday, which posts did well, what is queued to publish today, and what to do next.

## Prerequisites

An MCP client connected to SociaHive. See the [MCP setup guide](https://docs.sociahive.com/setup-guide).

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
> Be concise: under 200 words total. Do not modify anything.

## What the AI does under the hood

```
1. list_flows_with_stats     → flow performance + error counts
2. get_analytics_overview    → cross-platform impressions / engagement
3. list_scheduled_posts      → today's queue
```

All three tools only read data, so nothing in your account changes.

## Variations

| Tweak | Add to your prompt |
|---|---|
| Weekly instead of daily | "...for the last 7 days instead of 24 hours" |
| Per-platform | "Split the summary per platform: Instagram, Facebook, LinkedIn" |
| Slack-able | "Format the summary as a Slack message with emoji headings" |

## Cost

- **0 SociaHive AI credits**: all three tools only read metrics.
- Your AI tool's own usage, as your AI provider bills it.
- Three read requests against your [rate limits](https://docs.sociahive.com/rate-limits).
