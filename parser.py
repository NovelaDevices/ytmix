import re
from pathlib import Path


TIMESTAMP_LINE = re.compile(
    r"^\s*(?P<raw>(\d{1,2}:)?\d{1,2}:\d{2})\s*\]?\s*(?P<title>.+?)\s*$"
)


def timestamp_to_seconds(ts: str) -> int:
    parts = ts.split(":")
    parts = [int(p) for p in parts]

    if len(parts) == 2:
        m, s = parts
        return m * 60 + s
    elif len(parts) == 3:
        h, m, s = parts
        return h * 3600 + m * 60 + s

    raise ValueError(f"Invalid timestamp: {ts}")


def parse_description(description_path: Path):
    """
    Minimal Phase 2 parser:
    - extracts timestamp lines only
    - ignores everything else
    - returns structured track list
    """

    tracks = []

    text = description_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    index = 1

    for line in lines:
        match = TIMESTAMP_LINE.search(line)
        if not match:
            continue

        raw_ts = match.group("raw")
        title = match.group("title").strip()

        # normalize leading dash variants (Dataset 3 fix)
        title = re.sub(r"^\s*[—\-–]\s*", "", title).lstrip("]- ").strip()

        # very naive artist split (optional, best-effort only)
        artist = None

        # Only split on LAST " - " (this matches your dataset structure)
        if " - " in title:
            left, right = title.rsplit(" - ", 1)
            title = left.strip()
            artist = right.strip()

        tracks.append(
            {
                "index": index,
                "start": timestamp_to_seconds(raw_ts),
                "timestamp": raw_ts,
                "title": title,
                "artist": artist,
            }
        )

        index += 1

    return tracks


def write_tracks_json(tracks, output_path: Path):
    import json

    output_path.write_text(
        json.dumps(tracks, indent=2),
        encoding="utf-8"
    )
