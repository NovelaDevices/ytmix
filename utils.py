from pathlib import Path
import glob


def find_latest_file(folder: Path, pattern: str) -> Path | None:
    files = list(folder.glob(pattern))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)
