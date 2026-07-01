import sys
import os
import re
from pathlib import Path
from urllib.parse import urlparse


YOUTUBE_REGEX = re.compile(
    r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
)


def is_valid_url(url: str) -> bool:
    return bool(YOUTUBE_REGEX.match(url))


def safe_folder_name(url: str) -> str:
    """
    Create a simple deterministic folder name from the URL.
    Phase 0 version: just use video ID if present, else fallback hash-like string.
    """
    parsed = urlparse(url)

    if "youtu.be" in parsed.netloc:
        return parsed.path.strip("/")

    if "youtube.com" in parsed.netloc:
        query = parsed.query
        for part in query.split("&"):
            if part.startswith("v="):
                return part.split("=", 1)[1]

    return "ytmix_output"


def create_project_structure(base_dir: Path) -> None:
    (base_dir / "source").mkdir(parents=True, exist_ok=True)
    (base_dir / "output").mkdir(parents=True, exist_ok=True)


def main():
    if len(sys.argv) != 2:
        print("Usage: ytmix <youtube-url>")
        sys.exit(1)

    url = sys.argv[1]

    if not is_valid_url(url):
        print("Error: Invalid YouTube URL")
        sys.exit(1)

    folder_name = safe_folder_name(url)
    project_dir = Path.cwd() / folder_name

    if project_dir.exists():
        print(f"Project already exists: {project_dir}")
    else:
        print(f"Creating project: {project_dir}")
        create_project_structure(project_dir)

    print("\nPhase 0 complete.")
    print(f"URL: {url}")
    print(f"Project directory: {project_dir}")


if __name__ == "__main__":
    main()
