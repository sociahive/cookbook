# 02: Schedule a week of posts from a CSV

**Persona:** Developer
**Time:** 5 minutes
**Code:** Python + Node, both runnable

## What you'll build

A script that reads `posts.csv` and schedules every row on your connected
accounts. Useful for content agencies and batch migrations.

## CSV format

Use the included `posts.csv` or roll your own. `scheduled_at` must be in the
future, so change the example dates if they have passed:

```csv
text,platform,scheduled_at,image_url
"Monday motivation 💪",instagram,2027-03-01T09:00:00Z,https://cdn.example.com/mon.jpg
"Tuesday tip: keep it short",twitter,2027-03-02T09:00:00Z,
"Wednesday wisdom",linkedin,2027-03-03T09:00:00Z,
```

## Run it (Python)

```bash
pip install sociahive
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

- Resolve the `account_id` per platform once and cache it
- Create one post per row, about 2 seconds apart (writes are limited to 30 a minute)
- Wait for `Retry-After` and retry when the API answers `429`
- Print scheduled IDs as they confirm

`POST /posts/bulk` acts only on posts that already exist (schedule, delete or
change status), so it is not used here. To load a CSV as drafts instead and
schedule them later, use `POST /posts/import` or `sociahive posts import`.

## Verify

With the SociaHive CLI (its key needs the `agent:execute` scope):

```bash
npm install -g sociahive
export SOCIAHIVE_API_KEY=sk_...
sociahive posts list --status scheduled --limit 20
```

Or open the calendar in the web dashboard.

## Error handling tips

- **`400` with a validation message**: check the row's platform name and that
  `scheduled_at` is an ISO 8601 time in the future.
- **`429`**: limits are per user, across all your keys: 30 writes and 120
  reads a minute, and 1,000 requests a day. The scripts wait for `Retry-After`.
  See [rate limits](https://docs.sociahive.com/rate-limits).

## Cost

- **0 AI credits**: plain REST calls, no AI.
- One write request per row, plus one read per platform.
