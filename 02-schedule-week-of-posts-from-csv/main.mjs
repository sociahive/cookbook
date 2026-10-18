// Schedule posts from a CSV using @sociahive/sdk, one create call per row.
//
// Usage:
//   npm install @sociahive/sdk
//   export SOCIAHIVE_API_KEY=sk_...
//   node main.mjs posts.csv
//
// CSV columns: text, platform, scheduled_at, image_url

import { readFileSync } from 'node:fs'
import { SociaHive, SociaHiveError } from '@sociahive/sdk'

// Writes are limited to 30 a minute per user, so pace the creates.
const PAUSE_MS = 2100
const MAX_RETRIES = 3

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

// Create one post; on a 429 wait for Retry-After (60s if the header is missing).
async function createWithRetry(sh, payload) {
  for (let attempt = 0; ; attempt++) {
    try {
      return await sh.posts.create(payload)
    } catch (err) {
      if (!(err instanceof SociaHiveError) || !err.isRateLimited || attempt >= MAX_RETRIES) throw err
      const waitSeconds = err.retryAfter ?? 60
      console.log(`rate limited, waiting ${waitSeconds}s`)
      await sleep(waitSeconds * 1000)
    }
  }
}

function parseCsv(text) {
  // Tiny CSV parser, good enough for the simple format above; not RFC 4180.
  // If your text fields contain commas, swap in `csv-parse` or `papaparse`.
  const [header, ...rows] = text.trim().split('\n')
  const cols = header.split(',')
  return rows.map((row) => {
    const cells = []
    let i = 0
    let cur = ''
    let inQuote = false
    while (i < row.length) {
      const ch = row[i]
      if (ch === '"' && row[i - 1] !== '\\') {
        inQuote = !inQuote
      } else if (ch === ',' && !inQuote) {
        cells.push(cur)
        cur = ''
      } else {
        cur += ch
      }
      i++
    }
    cells.push(cur)
    return Object.fromEntries(cols.map((c, idx) => [c, cells[idx] ?? '']))
  })
}

async function main() {
  const [, , csvPath] = process.argv
  if (!csvPath) {
    console.error('usage: node main.mjs <posts.csv>')
    process.exit(1)
  }

  const apiKey = process.env.SOCIAHIVE_API_KEY
  if (!apiKey) {
    console.error('SOCIAHIVE_API_KEY env var required')
    process.exit(1)
  }

  const sh = new SociaHive({ apiKey })
  const rows = parseCsv(readFileSync(csvPath, 'utf8'))

  // Cache account_id per platform.
  const accountCache = new Map()
  for (const platform of new Set(rows.map((r) => r.platform))) {
    const { data } = await sh.accounts.list(platform)
    if (!data.length) {
      console.error(`No connected account for ${platform}`)
      process.exit(1)
    }
    accountCache.set(platform, data[0].id)
  }

  for (const [i, row] of rows.entries()) {
    if (i > 0) await sleep(PAUSE_MS)
    const payload = buildPayload(row, accountCache.get(row.platform))
    const post = await createWithRetry(sh, payload)
    console.log(`scheduled ${post.id} on ${payload.platforms[0].platform}`)
  }
}

function buildPayload(row, accountId) {
  const payload = {
    text: row.text.replace(/^"|"$/g, ''),
    platforms: [{ platform: row.platform, account_id: accountId }],
    schedule_type: 'scheduled',
    scheduled_at: row.scheduled_at,
    timezone: 'UTC',
  }
  if (row.image_url) {
    payload.media = [{ type: 'image', url: row.image_url }]
  }
  return payload
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
