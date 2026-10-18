<p align="center">
  <a href="https://www.sociahive.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/sociahive/.github/main/assets/brand/logo-dark.svg">
      <img alt="SociaHive" src="https://raw.githubusercontent.com/sociahive/.github/main/assets/brand/logo-light.svg" width="220">
    </picture>
  </a>
</p>

<p align="center">Run your social media from your AI tool: schedule posts, build DM and comment automations, and read analytics.</p>
<p align="center">Runnable recipes for the SociaHive API and MCP server.</p>

<p align="center">
  <a href="https://www.sociahive.com">Website</a> ·
  <a href="https://www.sociahive.com/connect-ai">Connect your AI</a> ·
  <a href="https://www.sociahive.com/developers">Developers</a> ·
  <a href="https://docs.sociahive.com">Docs</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue"></a>
</p>

# SociaHive cookbook

Runnable recipes for the [SociaHive](https://www.sociahive.com) API and MCP server. Some recipes run from your AI tool over MCP, others are short Python and Node scripts against the REST API.

Each recipe is a self-contained folder with its own README, runnable code, and
example output. Pick the one that matches the job you want done.

| # | Recipe | Persona | Surface |
|---|---|---|---|
| 01 | [Auto-reply to Instagram comments mentioning "price"](./01-auto-reply-instagram-comments/) | AI user | MCP via your AI tool |
| 02 | [Schedule a week of posts from a CSV](./02-schedule-week-of-posts-from-csv/) | Developer | REST API, Python + Node |
| 03 | [Daily performance recap from your AI tool](./03-daily-performance-recap/) | Power user | MCP via your AI tool |

## Conventions

- Every recipe folder has a `README.md` (what it does, when to use it, how to run it).
- Recipes that need code ship a runnable script (`main.py`, `main.mjs`).
- Every recipe declares its **cost** (AI credits, API rate-limit impact) at the bottom.
- API key configuration is always via the `SOCIAHIVE_API_KEY` env var.

## Prerequisites

For all recipes:

- A SociaHive account with at least one connected social platform
- An API key from [Settings > API keys](https://www.sociahive.com/settings?tab=api-keys)
- The 7-day trial or a paid plan (API and MCP access are not on the free plan)
- `export SOCIAHIVE_API_KEY=sk_...` in your shell

Per-recipe extras (Python deps, MCP client, etc.) are listed in each folder's
README.

## Works with your AI tool

The MCP recipes work in any AI tool that connects to the [SociaHive MCP server](https://www.sociahive.com/mcp).

<p align="center">
  <a href="https://www.sociahive.com/connect-ai/chatgpt"><img src="https://raw.githubusercontent.com/sociahive/.github/main/assets/agents/chatgpt.svg" alt="ChatGPT" title="ChatGPT" width="28"></a>&nbsp;&nbsp;
  <a href="https://www.sociahive.com/connect-ai/claude"><img src="https://raw.githubusercontent.com/sociahive/.github/main/assets/agents/claude.svg" alt="Claude" title="Claude" width="28"></a>&nbsp;&nbsp;
  <a href="https://www.sociahive.com/connect-ai/claude-code"><img src="https://raw.githubusercontent.com/sociahive/.github/main/assets/agents/claude-code.svg" alt="Claude Code" title="Claude Code" width="28"></a>&nbsp;&nbsp;
  <a href="https://www.sociahive.com/connect-ai/cursor"><img src="https://raw.githubusercontent.com/sociahive/.github/main/assets/agents/cursor.svg" alt="Cursor" title="Cursor" width="28"></a>&nbsp;&nbsp;
  <a href="https://www.sociahive.com/connect-ai/codex"><img src="https://raw.githubusercontent.com/sociahive/.github/main/assets/agents/codex.svg" alt="Codex" title="Codex" width="28"></a>&nbsp;&nbsp;
  <a href="https://www.sociahive.com/connect-ai/gemini"><img src="https://raw.githubusercontent.com/sociahive/.github/main/assets/agents/gemini.svg" alt="Gemini" title="Gemini" width="28"></a>&nbsp;&nbsp;
  <a href="https://www.sociahive.com/connect-ai/grok"><img src="https://raw.githubusercontent.com/sociahive/.github/main/assets/agents/grok.svg" alt="Grok" title="Grok" width="28"></a>&nbsp;&nbsp;
  <a href="https://www.sociahive.com/mcp"><img src="https://raw.githubusercontent.com/sociahive/.github/main/assets/agents/mcp.svg" alt="MCP" title="Any MCP client" width="28"></a>
</p>

## More

- [Node.js SDK](https://github.com/sociahive/sociahive-node) · [Python SDK](https://github.com/sociahive/sociahive-python) · [MCP server and plugins](https://github.com/sociahive/sociahive-mcp)
- [Developer docs](https://docs.sociahive.com)

## License

[MIT](LICENSE)
