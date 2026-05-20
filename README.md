# SociaHive Cookbook

Runnable recipes for the [SociaHive](https://www.sociahive.com) API and MCP server.

Each recipe is a self-contained folder with its own README, runnable code, and
example output. Pick the one that matches your job-to-be-done.

| # | Recipe | Persona | Surface |
|---|---|---|---|
| 01 | [Auto-reply to Instagram comments mentioning "price"](./01-auto-reply-instagram-comments/) | AI user | MCP via Claude/Cursor |
| 02 | [Schedule a week of posts from a CSV](./02-schedule-week-of-posts-from-csv/) | Developer | REST API, Python + Node |
| 03 | [Daily performance recap with Claude](./03-daily-performance-recap/) | Power user | MCP via Claude / Cursor |

## Conventions

- Every recipe folder has a `README.md` (what it does, when to use it, how to run it).
- Recipes that need code ship a runnable script (`main.py`, `main.ts`).
- Every recipe declares its **cost** (AI credits, API rate-limit impact) at the bottom.
- API key configuration is always via the `SOCIAHIVE_API_KEY` env var.

## Prerequisites

For all recipes:

- A SociaHive account with at least one connected social platform
- An API key from [Settings → API Keys](https://www.sociahive.com/settings?tab=api-keys)
- `export SOCIAHIVE_API_KEY=sk_...` in your shell

Per-recipe extras (Python deps, MCP client, etc.) are listed in each folder's
README.

## License

MIT
