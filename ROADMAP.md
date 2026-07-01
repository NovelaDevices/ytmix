# ytmix Roadmap

This document defines the planned architecture and development stages of ytmix.

It is treated as a **living execution guide**. Each phase should be completed in order unless explicitly re-scoped.

---

# Status Legend

* [ ] Not started
* [~] In progress
* [x] Completed
* [!] Blocked / needs decision

---

# Core Pipeline

ytmix is structured as a linear pipeline:

```text
Acquire → Parse → Split → Tag → Import
```

Each phase must produce artifacts that are:

* reproducible
* independent
* inspectable

---

# Phase 0 — Project Bootstrap

Status: [x]

* [x] Create GitHub repository
* [x] Apply MIT license
* [ ] Initialize Python package structure
* [ ] Create CLI entry point (`ytmix`)
* [ ] Verify ffmpeg + yt-dlp availability

Output:

* Runnable CLI that accepts a URL and prints system status

---

# Phase 1 — Acquisition Layer

Status: [ ] Not started

Goal: reliably download all source materials from YouTube.

Tasks:

* [ ] Download best available AAC audio stream (preferred: `-f 140`)
* [ ] Save video metadata (`.info.json`)
* [ ] Save video description (`.description`)
* [ ] Save thumbnail image
* [ ] Create deterministic project folder structure

Output:

```
project/
  source/
    audio.m4a
    info.json
    description.txt
    thumbnail.webp
```

---

# Phase 2 — Track List Parsing

Status: [ ] Not started

Goal: convert YouTube timestamp descriptions into structured data.

Tasks:

* [ ] Extract timestamp section from description
* [ ] Support multiple formats:

  * `00:00 Title`
  * `[00:00] Title`
  * `00:00 Artist - Title`
* [ ] Normalize into Track objects
* [ ] Compute track end times

Output:

* `tracks.json`

---

# Phase 3 — Audio Splitting

Status: [ ] Not started

Goal: split long audio into individual tracks without re-encoding.

Tasks:

* [ ] Implement FFmpeg stream copy splitting
* [ ] Generate filenames using track metadata
* [ ] Verify boundary accuracy
* [ ] Handle last-track edge case

Output:

```
output/
  01 Track Name.m4a
  02 Track Name.m4a
```

---

# Phase 4 — Tagging & Metadata

Status: [ ] Not started

Goal: turn raw audio files into a structured music album.

Tasks:

* [ ] Embed ID3/M4A tags using mutagen
* [ ] Set:

  * Title
  * Artist
  * Album
  * Track number
* [ ] Embed album artwork
* [ ] Preserve original source attribution in comments

Output:

* Fully tagged album folder

---

# Phase 5 — Library Integration

Status: [ ] Not started

Goal: integrate output into Apple Music (Music.app).

Tasks:

* [ ] Optional auto-import via AppleScript
* [ ] Manual import mode (default)
* [ ] Folder-based album export

---

# Phase 6 — Parser Hardening

Status: [ ] Not started

Goal: make parsing robust across real-world YouTube formats.

Tasks:

* [ ] Expand regex coverage
* [ ] Handle malformed timestamps
* [ ] Handle missing artists
* [ ] Handle multi-line descriptions
* [ ] Add parser test suite

---

# Design Constraints

* Never overwrite source files
* Never re-encode unless explicitly requested
* Always preserve original metadata files
* All pipeline stages must be independently rerunnable
* Prefer determinism over automation complexity

---

# Future Extensions (Non-Core)

* MusicBrainz tagging
* Playlist generation
* Bandcamp support
* SoundCloud support
* Cue sheet export
* Integration with offline music recommendation engine

---

# Current Focus

We are currently in:

> Phase 0 → Project Bootstrap

Next milestone:

* First working CLI that accepts a URL and builds a folder structure
