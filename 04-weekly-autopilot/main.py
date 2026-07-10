"""Weekly Autopilot: generate → review → approve, via the raw REST API.

Every week SociaHive can plan, write, design, and schedule a full week of
on-brand posts for your connected accounts. This script drives that flow
end-to-end against https://www.sociahive.com/api/v1 using the X-API-Key header.

Usage:
    pip install requests
    export SOCIAHIVE_API_KEY=sk_...
    python main.py                 # generate + review (safe: no go-live)
    python main.py --approve       # ALSO approve → schedules the week to your
                                   # real audience (IRREVERSIBLE)

Scopes required: autopilot:read (status) + autopilot:write (generate/adjust/approve)
"""

from __future__ import annotations

import os
import sys
import time

import requests

BASE_URL = "https://www.sociahive.com/api/v1"
POLL_INTERVAL_SECONDS = 10  # generation takes ~90s; poll config until it settles
POLL_MAX_ATTEMPTS = 18      # 18 * 10s = 3 min ceiling


def _session() -> requests.Session:
    api_key = os.environ.get("SOCIAHIVE_API_KEY")
    if not api_key:
        sys.exit("SOCIAHIVE_API_KEY env var required")
    s = requests.Session()
    s.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})
    return s


def get_config(s: requests.Session) -> dict:
    """GET /autopilot/config — current mode, quota, and this week's batch state."""
    r = s.get(f"{BASE_URL}/autopilot/config")
    r.raise_for_status()
    return r.json()


def generate_week(s: requests.Session) -> dict:
    """POST /autopilot/generate — enqueue the week. Returns 202 + a batch id."""
    r = s.post(f"{BASE_URL}/autopilot/generate")
    if r.status_code == 409:
        # A batch already exists for this week — there is no regenerate in v1.
        sys.exit("A batch already exists for this week (409 week_exists). "
                 "Review or approve the existing one instead.")
    r.raise_for_status()  # 202 on success
    return r.json()


def wait_for_batch(s: requests.Session) -> dict:
    """Poll /autopilot/config until the batch stops generating (~90s)."""
    for attempt in range(POLL_MAX_ATTEMPTS):
        config = get_config(s)
        batch = config.get("current_batch") or {}
        if not batch.get("generating", False) and batch.get("posts"):
            return config
        print(f"  …generating (attempt {attempt + 1}/{POLL_MAX_ATTEMPTS})")
        time.sleep(POLL_INTERVAL_SECONDS)
    sys.exit("Batch still generating after the poll ceiling — check again later.")


def adjust_week(s: requests.Session, feedback: str) -> dict:
    """POST /autopilot/adjust — steer the plan in plain language, re-generates."""
    r = s.post(f"{BASE_URL}/autopilot/adjust", json={"feedback": feedback})
    r.raise_for_status()
    return r.json()


def approve_week(s: requests.Session) -> dict:
    """POST /autopilot/approve — schedule the week to your REAL audience.

    IRREVERSIBLE go-live. The API requires confirm:true; without it, it returns
    400 confirmation_required and does nothing.
    """
    r = s.post(f"{BASE_URL}/autopilot/approve", json={"confirm": True})
    if r.status_code == 400 and r.json().get("code") == "confirmation_required":
        sys.exit("Refused: approve requires confirm:true (irreversible go-live).")
    r.raise_for_status()
    return r.json()


def main() -> None:
    approve = "--approve" in sys.argv[1:]
    s = _session()

    # 1. Show current state.
    config = get_config(s)
    print(f"mode={config.get('mode')} "
          f"quota={config.get('posts_per_week')}/wk "
          f"week_start={config.get('week_start')}")

    # 2. Enqueue the week.
    gen = generate_week(s)
    print(f"generating batch {gen['batch_id']} for week {gen['week_start']}")

    # 3. Wait for the ~90s generation to finish.
    config = wait_for_batch(s)
    posts = config["current_batch"]["posts"]
    print(f"planned {len(posts)} posts:")
    for post in posts:
        target = post["platforms"][0]["platform"]
        print(f"  {post['scheduled_at']}  {target}  {post['caption'][:60]}…")

    # 4. (Optional) steer it. Uncomment to adjust before approving.
    # config = adjust_week(s, "Fewer product posts, more behind-the-scenes.")
    # print("adjusted — re-review above")

    # 5. Approve → schedule to the real audience. IRREVERSIBLE.
    if not approve:
        print("\nDry run complete. Re-run with --approve to schedule the week "
              "to your real audience (irreversible go-live).")
        return
    result = approve_week(s)
    print(f"\napproved — {result['scheduled_count']} posts scheduled to your audience")


if __name__ == "__main__":
    main()
