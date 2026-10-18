# 01: Auto-reply to Instagram comments mentioning "price"

**Persona:** AI user (Claude.ai, Claude Desktop, Cursor)
**Time:** 2 minutes
**Code:** none. You prompt your AI tool over MCP.

## What you'll build

A SociaHive automation flow that DMs anyone who comments "price", "cost", or
"how much" on your Instagram posts. You do it by *talking* to your AI
assistant.

## Prerequisites

- An MCP client connected to `https://www.sociahive.com/api/mcp`. See the
  [MCP setup guide](https://docs.sociahive.com/setup-guide).
- At least one Instagram account connected in SociaHive

## The prompt

Paste this verbatim into Claude/ChatGPT/Cursor:

> Using SociaHive, build me an Instagram comment auto-reply flow:
>
> 1. Trigger on comments containing "price", "cost", or "how much"
> 2. Reply publicly with "DMing you now! 📩"
> 3. Send the commenter a DM with our pricing link: https://example.com/pricing
> 4. Show me the flow and ask me before turning it on
>
> Use my first Instagram account.

## What the AI does under the hood

```
1. list_accounts                  → find your Instagram account
2. generate_flow                  → AI builds the entire flow graph
3. get_flow                       → show you the result
4. activate_flow                  → after you say yes
```

## Variations

| Tweak | Add to your prompt |
|---|---|
| Multiple keyword branches | "If they say 'price' send pricing; if they say 'demo' send a Calendly link" |
| AI-personalized replies | "Reply with an AI-generated message that matches my brand voice, using my knowledge base" |
| Tag the contact | "...and tag the contact with 'price-curious'" |
| Restrict to one post | "Only on Instagram post 18234567890123456" |

## Verify it worked

> Show me stats for the flow I just created.

The AI calls `get_flow_stats`. New flows start at 0 across the board.

## Cost

- **0 AI credits** to build the flow: `generate_flow` is free.
- **0 credits** per auto-reply when the messages are fixed text.
- **5 credits** per reply if you switch to AI-written replies.

See [pricing](https://www.sociahive.com/pricing) for monthly credit
allowances.
