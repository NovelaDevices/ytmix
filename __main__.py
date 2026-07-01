import sys
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from ytmix.downloader import download_youtube_assets
from ytmix.parser import parse_description, write_tracks_json

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
    # -------------------
    # Phase 0
    # -------------------
    if project_dir.exists():
        print(f"Project already exists: {project_dir}")
    else:
        print(f"Creating project: {project_dir}")
        create_project_structure(project_dir)

    print("\nPhase 0 complete.")
    print(f"URL: {url}")
    print(f"Project directory: {project_dir}")
    # -------------------
    # Phase 1 
    # -------------------
    print("\nStarting Phase 1: Acquisition...\n")

    try:
        download_youtube_assets(url, project_dir / "source")
    except subprocess.CalledProcessError:
        print("Error: yt-dlp download failed")
        sys.exit(1)

    print("\nPhase 1 complete.")
    print(f"Assets stored in: {project_dir / 'source'}")
    # -------------------
    # Phase 2 
    # -------------------
    print("\nStarting Phase 2: Parsing...\n")

    description_file = project_dir / "source" / "description.txt"

    tracks = parse_description(description_file)

    tracks_file = project_dir / "tracks.json"
    write_tracks_json(tracks, tracks_file)

    print(f"Found {len(tracks)} tracks")
    print(f"Tracks written to: {tracks_file}")

    print("\nPhase 2 complete.")


if __name__ == "__main__":
    main()
