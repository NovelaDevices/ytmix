import subprocess
from pathlib import Path


def download_youtube_assets(url: str, output_dir: Path) -> None:
    """
    Phase 1 acquisition layer using yt-dlp.

    Downloads:
      - best AAC audio (preferred: 140)
      - metadata json
      - description
      - thumbnail
    """

    output_template = str(output_dir / "%(title)s.%(ext)s")

    cmd = [
        "yt-dlp",
        url,

        # Audio selection (Apple-friendly AAC preferred)
        "-f", "140",

        # Metadata artifacts
        "--write-info-json",
        "--write-description",
        "--write-thumbnail",

        # Extract audio only
        "--extract-audio",
        "--audio-format", "m4a",

        # Output template
        "-o", output_template,
    ]

    subprocess.run(cmd, check=True)

from .utils import find_latest_file
import shutil

def normalize_downloads(output_dir: Path) -> None:
    """
    Rename yt-dlp outputs into clean canonical filenames.
    """

    # Audio (m4a)
    audio = find_latest_file(output_dir, "*.m4a")
    if audio:
        audio.rename(output_dir / "audio.m4a")

    # Info JSON
    info = find_latest_file(output_dir, "*.info.json")
    if info:
        info.rename(output_dir / "info.json")

    # Description
    desc = find_latest_file(output_dir, "*.description")
    if desc:
        desc.rename(output_dir / "description.txt")

    # Thumbnail (varies: webp/jpg/png)
    thumb = (
        find_latest_file(output_dir, "*.webp")
        or find_latest_file(output_dir, "*.jpg")
        or find_latest_file(output_dir, "*.png")
    )
    if thumb:
        suffix = thumb.suffix
        thumb.rename(output_dir / f"thumbnail{suffix}")

normalize_downloads(output_dir)
