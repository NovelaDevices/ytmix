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
