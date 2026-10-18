"""Schedule posts from a CSV using the sociahive Python SDK, one create call per row.

Usage:
    pip install sociahive
    export SOCIAHIVE_API_KEY=sk_...
    python main.py posts.csv

CSV columns: text, platform, scheduled_at, image_url
"""

from __future__ import annotations

import csv
import os
import sys
import time
from typing import Any

from sociahive import SociaHive, SociaHiveError

# Writes are limited to 30 a minute per user, so pace the creates.
PAUSE_SECONDS = 2.1
MAX_RETRIES = 3


def _create_with_retry(sh: SociaHive, payload: dict[str, Any]) -> dict[str, Any]:
    """Create one post; on a 429 wait for Retry-After (60s if the header is missing)."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            return sh.posts.create(**payload)
        except SociaHiveError as err:
            if not err.is_rate_limited or attempt == MAX_RETRIES:
                raise
            wait = getattr(err, "retry_after", None) or 60
            print(f"rate limited, waiting {wait}s")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def main(csv_path: str) -> None:
    sh = SociaHive(api_key=os.environ["SOCIAHIVE_API_KEY"])

    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))

    # Resolve account IDs once per distinct platform.
    account_cache: dict[str, str] = {}
    for platform in {row["platform"] for row in rows}:
        accounts = sh.accounts.list(platform=platform).get("data", [])
        if not accounts:
            sys.exit(f"No connected account for {platform}")
        account_cache[platform] = accounts[0]["id"]

    for i, row in enumerate(rows):
        if i > 0:
            time.sleep(PAUSE_SECONDS)
        payload = _build_payload(row, account_cache[row["platform"]])
        post = _create_with_retry(sh, payload)
        print(f"scheduled {post['id']} on {payload['platforms'][0]['platform']}")


def _build_payload(row: dict[str, str], account_id: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "text": row["text"],
        "platforms": [{"platform": row["platform"], "account_id": account_id}],
        "schedule_type": "scheduled",
        "scheduled_at": row["scheduled_at"],
        "timezone": "UTC",
    }
    if row.get("image_url"):
        payload["media"] = [{"type": "image", "url": row["image_url"]}]
    return payload


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python main.py <posts.csv>")
    main(sys.argv[1])
