# 02 — Schedule a week of posts from a CSV

**Persona:** Developer
**Time:** 5 minutes
**Code:** Python + Node, both runnable

## What you'll build

A script that reads `posts.csv` and schedules every row across your connected
platforms. Useful for content agencies, batch migrations, or anyone fed up
with the SociaHive UI for bulk operations.

## CSV format

Use the included `posts.csv` or roll your own:

```csv
text,platform,scheduled_at,image_url
"Monday motivation 💪",instagram,2026-06-01T09:00:00Z,https://cdn.example.com/mon.jpg
"Tuesday tip: keep it short",twitter,2026-06-02T09:00:00Z,
"Wednesday wisdom",linkedin,2026-06-03T09:00:00Z,
```

## Run it (Python)

```bash
pip install sociahive       # or: pip install requests if you prefer raw fetch
export SOCIAHIVE_API_KEY=sk_...
python main.py posts.csv
```

## Run it (Node)

```bash
npm install @sociahive/sdk
export SOCIAHIVE_API_KEY=sk_...
node main.mjs posts.csv
```

Both scripts:

- Resolve the right `account_id` per platform once and cache it (don't re-fetch)
- Use the batch endpoint for runs >10 rows
- Print scheduled IDs as they confirm

## Verify

```bash
sociahive posts list --status scheduled --limit 20
```

…or open the calendar view in the web dashboard.

## Error handling tips

- **`413` on `/posts/bulk`** — batch cap is 100 rows. Chunk your CSV.
- **`400 platform_user_id required`** — your account-id lookup matched the
  wrong account. Pass `platform_user_id` explicitly.
- **`429`** — default rate limit is 1000 req/hr per API key. The batch
  endpoint counts as one request.

## Cost

- **$0 in AI credits** — pure REST API, no AI calls.
- Standard platform fees apply at publish time (none for organic posts).
