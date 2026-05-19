"""Bulk-schedule posts from a CSV using the sociahive Python SDK.

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
from typing import Any

from sociahive import SociaHive

BATCH_THRESHOLD = 10  # use /posts/bulk when a CSV has more than this many rows


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

    payloads = [_build_payload(row, account_cache[row["platform"]]) for row in rows]

    if len(payloads) > BATCH_THRESHOLD:
        result = sh.posts.bulk(payloads)
        for post in result.get("data", []):
            print(f"scheduled {post['id']} on {post['platforms'][0]['platform']}")
    else:
        for payload in payloads:
            post = sh.posts.create(**payload)
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
