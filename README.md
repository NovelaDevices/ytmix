# ytmix

**ytmix** is an open-source command-line utility for converting long-form YouTube music mixes into properly tagged albums suitable for local music libraries.

Rather than treating a two- or three-hour mix as a single audio file, ytmix downloads the highest-quality Apple-compatible audio stream, extracts the published track list, splits the mix into individual songs without re-encoding, applies metadata and album artwork, and optionally imports the finished album into Apple Music (Music.app).

The goal is to make YouTube music mixes feel like professionally released albums.

---

## Why?

Many YouTube music channels publish excellent long-form mixes with timestamps in the video description.

Unfortunately, downloading these mixes typically leaves you with a single multi-hour audio file that is difficult to navigate, organize, or integrate into a local music library.

ytmix automates this workflow by transforming a continuous mix into a properly organized album.

---

## Design Philosophy

ytmix follows a few guiding principles:

* Preserve original media whenever possible.
* Never re-encode audio unless explicitly requested.
* Produce deterministic, repeatable results.
* Separate downloading, parsing, splitting, tagging, and importing into independent pipeline stages.
* Build a high-quality local music library rather than a collection of anonymous downloads.

---

## Features (Planned)

### Phase 1

* Download best Apple-compatible audio using yt-dlp
* Download thumbnail artwork
* Save video description
* Save YouTube metadata
* Create project directory

### Phase 2

* Parse timestamp track listings
* Support multiple timestamp formats
* Generate structured track metadata

### Phase 3

* Split audio into individual tracks using FFmpeg stream copy
* No quality loss
* Automatic filenames

### Phase 4

* Apply metadata
* Embed artwork
* Track numbering
* Album information

### Phase 5

* Import finished album into Apple Music (macOS)
* Optional manual output mode

### Future Ideas

* Support additional music sources
* Cue sheet export
* Playlist generation
* MusicBrainz lookup
* Discogs integration
* Library automation

---

## Pipeline

```text
YouTube URL
      │
      ▼
Acquire Source
      │
      ▼
Parse Track List
      │
      ▼
Split Audio
      │
      ▼
Tag Tracks
      │
      ▼
Import Album
```

---

## Example

```bash
ytmix https://www.youtube.com/watch?v=kQG9f_FKn3Y
```

Expected result:

```text
Sensual Jazz/

    source/
        audio.m4a
        description.txt
        info.json
        thumbnail.webp

    output/
        01 One Day in Your Life.m4a
        02 Long Time No See.m4a
        ...
```

---

## Requirements

* Python 3.11+
* yt-dlp
* FFmpeg
* mutagen

---

## Project Status

ytmix is currently under active development.

The initial focus is on creating a reliable acquisition and parsing pipeline before implementing audio splitting and metadata tagging.

---

## License

MIT License
