// Weekly Autopilot: generate → review → approve, via the raw REST API.
//
// Every week SociaHive can plan, write, design, and schedule a full week of
// on-brand posts for your connected accounts. This script drives that flow
// end-to-end against https://www.sociahive.com/api/v1 using the X-API-Key header.
//
// Usage:
//   export SOCIAHIVE_API_KEY=sk_...
//   node main.mjs                 # generate + review (safe: no go-live)
//   node main.mjs --approve       # ALSO approve → schedules the week to your
//                                 # real audience (IRREVERSIBLE)
//
// Scopes required: autopilot:read (status) + autopilot:write (generate/adjust/approve)

const BASE_URL = 'https://www.sociahive.com/api/v1'
const POLL_INTERVAL_MS = 10_000 // generation takes ~90s; poll config until it settles
const POLL_MAX_ATTEMPTS = 18 // 18 * 10s = 3 min ceiling

function headers() {
  const apiKey = process.env.SOCIAHIVE_API_KEY
  if (!apiKey) {
    console.error('SOCIAHIVE_API_KEY env var required')
    process.exit(1)
  }
  return { 'X-API-Key': apiKey, 'Content-Type': 'application/json' }
}

async function api(method, path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: headers(),
    body: body ? JSON.stringify(body) : undefined,
  })
  const data = await res.json().catch(() => ({}))
  return { status: res.status, data }
}

// GET /autopilot/config — current mode, quota, and this week's batch state.
async function getConfig() {
  const { data } = await api('GET', '/autopilot/config')
  return data
}

// POST /autopilot/generate — enqueue the week. Returns 202 + a batch id.
async function generateWeek() {
  const { status, data } = await api('POST', '/autopilot/generate')
  if (status === 409) {
    // A batch already exists for this week — there is no regenerate in v1.
    console.error('A batch already exists for this week (409 week_exists). '
      + 'Review or approve the existing one instead.')
    process.exit(1)
  }
  return data
}

// Poll /autopilot/config until the batch stops generating (~90s).
async function waitForBatch() {
  for (let attempt = 0; attempt < POLL_MAX_ATTEMPTS; attempt++) {
    const config = await getConfig()
    const batch = config.current_batch ?? {}
    if (!batch.generating && batch.posts?.length) return config
    console.log(`  …generating (attempt ${attempt + 1}/${POLL_MAX_ATTEMPTS})`)
    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS))
  }
  console.error('Batch still generating after the poll ceiling — check again later.')
  process.exit(1)
}

// POST /autopilot/adjust — steer the plan in plain language, re-generates.
async function adjustWeek(feedback) {
  const { data } = await api('POST', '/autopilot/adjust', { feedback })
  return data
}

// POST /autopilot/approve — schedule the week to your REAL audience.
// IRREVERSIBLE go-live. The API requires confirm:true; without it, it returns
// 400 confirmation_required and does nothing.
async function approveWeek() {
  const { status, data } = await api('POST', '/autopilot/approve', { confirm: true })
  if (status === 400 && data.code === 'confirmation_required') {
    console.error('Refused: approve requires confirm:true (irreversible go-live).')
    process.exit(1)
  }
  return data
}

async function main() {
  const approve = process.argv.slice(2).includes('--approve')

  // 1. Show current state.
  let config = await getConfig()
  console.log(`mode=${config.mode} quota=${config.posts_per_week}/wk `
    + `week_start=${config.week_start}`)

  // 2. Enqueue the week.
  const gen = await generateWeek()
  console.log(`generating batch ${gen.batch_id} for week ${gen.week_start}`)

  // 3. Wait for the ~90s generation to finish.
  config = await waitForBatch()
  const posts = config.current_batch.posts
  console.log(`planned ${posts.length} posts:`)
  for (const post of posts) {
    const target = post.platforms[0].platform
    console.log(`  ${post.scheduled_at}  ${target}  ${post.caption.slice(0, 60)}…`)
  }

  // 4. (Optional) steer it. Uncomment to adjust before approving.
  // config = await adjustWeek('Fewer product posts, more behind-the-scenes.')
  // console.log('adjusted — re-review above')

  // 5. Approve → schedule to the real audience. IRREVERSIBLE.
  if (!approve) {
    console.log('\nDry run complete. Re-run with --approve to schedule the week '
      + 'to your real audience (irreversible go-live).')
    return
  }
  const result = await approveWeek()
  console.log(`\napproved — ${result.scheduled_count} posts scheduled to your audience`)
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
