from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any

import requests
import streamlit as st

HN_API = "https://hacker-news.firebaseio.com/v0"
ITEM_URL = HN_API + "/item/{id}.json"
TOP_STORIES_URL = HN_API + "/topstories.json"
HN_DISCUSS_URL = "https://news.ycombinator.com/item?id={id}"


# ----------------------------
# Data layer
# ----------------------------


@st.cache_data(show_spinner=False, ttl=60)
def get_top_story_ids(limit: int = 100) -> list[int]:
    """Fetch top story IDs from the official Hacker News Firebase API."""
    resp = requests.get(TOP_STORIES_URL, timeout=20)
    resp.raise_for_status()
    ids = resp.json() or []
    return ids[:limit]


@st.cache_data(show_spinner=False, ttl=300)
def get_item(item_id: int) -> dict[str, Any]:
    """Fetch a single HN item (story) by ID."""
    r = requests.get(ITEM_URL.format(id=item_id), timeout=20)
    r.raise_for_status()
    return r.json() or {}


def fetch_items_concurrently(
    ids: list[int], max_workers: int = 24
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        futures = {exe.submit(get_item, i): i for i in ids}
        for fut in as_completed(futures):
            try:
                data = fut.result()
                if data and data.get("type") == "story":
                    results.append(data)
            except Exception:
                # Skip failed items quietly; optionally log with st.debug in the future
                pass
    # Keep the original top order
    order = {id_: idx for idx, id_ in enumerate(ids)}
    results.sort(key=lambda x: order.get(x.get("id", 0), 10**9))
    return results


# ----------------------------
# UI helpers
# ----------------------------


def time_ago(ts: int | None) -> str:
    if not ts:
        return ""
    now = datetime.now(timezone.utc)
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    diff = (now - dt).total_seconds()
    mins = int(diff // 60)
    hours = int(mins // 60)
    days = int(hours // 24)
    if diff < 60:
        return "just now"
    if mins < 60:
        return f"{mins}m ago"
    if hours < 24:
        return f"{hours}h ago"
    return f"{days}d ago"


# ----------------------------
# Sidebar controls
# ----------------------------

st.divider()
st.sidebar.title("Hacker News Controls")
limit = st.sidebar.slider(
    "How many stories?", min_value=10, max_value=100, value=100, step=10
)
show_table = st.sidebar.checkbox("Show table view", value=False)
max_workers = st.sidebar.slider("Parallel fetch workers", 1, 8, 4, step=1)

if st.sidebar.button("Refresh now", icon=":material/refresh:"):
    get_top_story_ids.clear()
    get_item.clear()
    st.rerun()

st.title("🗞️ Hacker News — Top 100")
st.caption(
    "Powered by the official Hacker News Firebase API. Cached for speed; use the refresh button to force update."
)

# ----------------------------
# Fetch and render
# ----------------------------

with st.spinner("Fetching top stories..."):
    ids = get_top_story_ids(limit)
    stories = fetch_items_concurrently(ids, max_workers=max_workers)

# Quick search filter (client-side)
q = st.text_input(
    "Filter by title/author/domain",
    value="",
    placeholder="e.g. postgres, LLM, rust, cloudflare",
)
q_lower = q.strip().lower()

if q_lower:

    def match(s: dict[str, Any]) -> bool:
        title = (s.get("title") or "").lower()
        by = (s.get("by") or "").lower()
        url = s.get("url") or ""
        domain = url.split("/")[2] if "/" in url else url
        return q_lower in title or q_lower in by or q_lower in domain.lower()

    stories = [s for s in stories if match(s)]

left, right = st.columns([3, 1])
left.subheader(f"Showing {len(stories)} stor{'ies' if len(stories) > 1 else 'y'}")
right.write("")
right.metric("Last updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# list view
for idx, s in enumerate(stories, start=1):
    title = s.get("title") or "(no title)"
    url = s.get("url")
    story_id = s.get("id")
    discuss_url = HN_DISCUSS_URL.format(id=story_id)
    link = url or discuss_url

    score = s.get("score", 0)
    by = s.get("by", "?")
    descendants = s.get("descendants", 0)
    created = time_ago(s.get("time"))

    with st.container(border=True):
        st.markdown(f"### {idx}. [{title}]({link})")
        c1, c2, c3, c4, c5 = st.columns([1.1, 1, 1, 1.4, 2])
        c1.write(f":material/thumb_up: **{score}** points")
        c2.write(f":material/comment: **{descendants or 0}** comments")
        c3.write(f":material/person: {by}")
        c4.write(f":material/timelapse: {created}")
        c5.markdown(f"[Discuss on HN]({discuss_url})")

# Optional table view
if show_table:
    import pandas as pd

    table_rows = []
    for s in stories:
        url = s.get("url")
        table_rows.append(
            {
                "id": s.get("id"),
                "title": s.get("title"),
                "points": s.get("score", 0),
                "comments": s.get("descendants", 0),
                "author": s.get("by"),
                "time": datetime.fromtimestamp(s.get("time", 0)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if s.get("time")
                else "",
                "link": url or HN_DISCUSS_URL.format(id=s.get("id")),
                "domain": (url.split("/")[2] if (url and "/" in url) else ""),
            }
        )
    df = pd.DataFrame(table_rows)
    st.dataframe(df, width="stretch", hide_index=True)
