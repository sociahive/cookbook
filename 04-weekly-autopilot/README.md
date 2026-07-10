# 04 — Weekly Autopilot: generate → review → approve

**Persona:** Developer / power user
**Time:** 5 minutes (plus ~90s of generation)
**Code:** Python + Node, both runnable

## What you'll build

A script that runs SociaHive **Autopilot** end-to-end: it plans, writes,
designs (AI images), and schedules a full week of on-brand posts for your
connected accounts, lets you review the week, optionally steer it, and then
approves it to your real audience. Useful for solo creators and agencies who
want a hands-off weekly content engine instead of composing post-by-post.

The flow is deliberately two-phase: **generate is safe** (it produces a
reviewable draft batch), **approve is the go-live** (it schedules to your real
audience and is irreversible).

## The flow

```
GET  /autopilot/config    → current mode, weekly quota, this week's batch
POST /autopilot/generate  → 202 { week_start, batch_id, generating }
GET  /autopilot/config    → poll until generating:false (~90s), review posts
POST /autopilot/adjust    → (optional) { feedback } to steer, re-generates
POST /autopilot/approve   → { confirm: true } → schedules the week (IRREVERSIBLE)
```

Generation runs **asynchronously**: `/generate` returns `202` immediately with a
`batch_id`, and the week's posts (captions + images + optimal-time slots) fill
in over **~90 seconds**. Poll `GET /autopilot/config` and watch
`current_batch.generating` flip to `false`.

## Required scopes

| Endpoint | Scope |
|---|---|
| `GET /autopilot/config` | `autopilot:read` |
| `POST /autopilot/generate` | `autopilot:write` |
| `POST /autopilot/adjust` | `autopilot:write` |
| `POST /autopilot/approve` | `autopilot:write` |

Grant both on your key at
[Settings → API Keys](https://www.sociahive.com/settings?tab=api-keys).

## Run it (Python)

```bash
pip install requests
export SOCIAHIVE_API_KEY=sk_...
python main.py               # generate + review (safe: no go-live)
python main.py --approve     # ALSO approve → schedules to your real audience
```

## Run it (Node)

```bash
export SOCIAHIVE_API_KEY=sk_...
node main.mjs                # generate + review (safe: no go-live)
node main.mjs --approve      # ALSO approve → schedules to your real audience
```

Both scripts authenticate with the `X-API-Key` header against
`https://www.sociahive.com/api/v1`, poll for the ~90s generation, print the
planned week, and only go live when you pass `--approve`.

## ⚠️ Approve is an irreversible go-live

`POST /autopilot/approve` schedules every post in the batch to your **real
audience**. There is no un-approve. The API refuses to go live without explicit
confirmation:

```bash
# Missing confirm → 400, nothing scheduled:
curl -sS -X POST https://www.sociahive.com/api/v1/autopilot/approve \
  -H "X-API-Key: $SOCIAHIVE_API_KEY" \
  -H "Content-Type: application/json" -d '{}'
# → 400 { "code": "confirmation_required" }

# With confirm:true → schedules the week:
curl -sS -X POST https://www.sociahive.com/api/v1/autopilot/approve \
  -H "X-API-Key: $SOCIAHIVE_API_KEY" \
  -H "Content-Type: application/json" -d '{"confirm": true}'
```

Always **review the batch first** (step 3) before approving.

## Do it from your AI assistant (MCP)

Same flow, no code — talk to an MCP client connected to
`https://www.sociahive.com/api/mcp`:

> Run SociaHive Autopilot for this week: show me my autopilot status, generate
> the week, wait for it, and show me the planned posts. Don't approve yet — I
> want to review first.

Under the hood the AI calls, in order:

```
1. get_autopilot_status        → current mode + this week's batch
2. generate_autopilot_week     → enqueue (202, generating)
3. get_autopilot_status        → poll until the batch is ready (~90s)
4. adjust_autopilot_week       → (optional) { feedback } to steer
5. approve_autopilot_week      → { confirm: true } — only after you confirm
```

`approve_autopilot_week` requires `confirm: true` for the same reason the REST
route does — it's the irreversible go-live.

## Do it from the CLI

```bash
sociahive autopilot status
sociahive autopilot generate
sociahive autopilot adjust --feedback "Fewer product posts, more behind-the-scenes"
sociahive autopilot approve --yes     # --yes maps to confirm:true (irreversible)
```

Without `--yes`, `autopilot approve` prints the batch summary and exits without
scheduling.

## Error handling tips

- **`400 confirmation_required` on `/approve`** — you didn't send
  `confirm: true`. This is the intended guard, not a bug.
- **`409 week_exists` on `/generate`** — a batch already exists for this week.
  There is no regenerate in v1; review or approve the existing batch instead.
- **`403 feature_disabled`** — Autopilot isn't enabled on your account yet.
- **`403 insufficient_scope`** — add `autopilot:read` / `autopilot:write` to your
  API key.
- **Batch still `generating:true` after polling** — generation occasionally runs
  long; back off and re-poll `GET /autopilot/config`.

## Cost

- **$0 in AI credits** for the included weekly quota — planning, captions, and
  images are covered by your tier's Autopilot allowance (see
  [tier-limits docs](https://www.sociahive.com/mcp)).
- Posts **beyond your weekly quota** meter at **15 AI credits each**, charged at
  generation with a refund on failure (Autopilot pauses rather than auto-buying
  overage).
- Standard platform fees apply at publish time (none for organic posts).
