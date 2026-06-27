# Ep1 Short — run the Dhruva voiceover on a local Mac

> **Why local:** the cloud container's network policy blocks `api.elevenlabs.io`
> (confirmed: every TTS call returns `403`). On your Mac there's no such block,
> so the ElevenLabs voice works. Everything is pre-built — this is copy-paste.

The pipeline (`sync_build.py`) generates the joyful Dhruva voiceover with
character-level timestamps, **re-times every scene to the spoken words**, writes
`short-3min_synced.html`, and builds `audio_v2/short.aac`. Then you render + mux.
Full background: `tti-studio/docs/VOICEOVER.md`.

---

## 0. One-time toolchain (Mac)

```bash
# Homebrew (skip if you have it): https://brew.sh
brew install node ffmpeg python3
python3 -m pip install --user requests
```

## 1. Clone the repo + check out this branch

```bash
git clone https://github.com/dhruvateja06/videos.git
cd videos
git checkout claude/eager-shannon-i79f3n
git pull origin claude/eager-shannon-i79f3n
```

## 2. Set your ElevenLabs key (needs `text_to_speech` permission)

```bash
export ELEVENLABS_API_KEY="sk_...your key..."
```

> A key that can only *list voices* will 401 on synthesis. Make sure the key has
> Text-to-Speech enabled in the ElevenLabs dashboard.

## 3. Generate voiceover + word-synced composition

```bash
cd tti-studio/episodes/ep01
python3 sync_build.py
```

This prints a scene map and produces:
- `short-3min_synced.html` — re-timed, word-pinned render source
- `audio_v2/short.aac` — the synced narration track (gitignored cache)
- `audio_v2/sN.mp3` + `sN.align.json` — per-scene audio + alignment (cached;
  delete a scene's two files to force it to re-synthesize)

## 4. Render the synced composition (silent), from the project root

```bash
cd ../..                                  # -> tti-studio/
npx --yes hyperframes@0.7.5 browser ensure   # first time only; uses system Chrome
npx --yes hyperframes@0.7.5 render . \
  -c episodes/ep01/short-3min_synced.html \
  -o renders/short-3min-v2.mp4 \
  --fps 30 --quality standard --workers 4
```

## 5. Mux voice + compress to the deliverable

```bash
ffmpeg -y -i renders/short-3min-v2.mp4 -i episodes/ep01/audio_v2/short.aac \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 20 -preset medium \
  -movflags +faststart -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 -shortest \
  episodes/ep01/short-3min-voiced.mp4
```

## 6. QA before committing (from `docs/VOICEOVER.md`)

```bash
# duration: voiced length == audio length (no truncation)
ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 \
  episodes/ep01/short-3min-voiced.mp4
ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 \
  episodes/ep01/audio_v2/short.aac

# voice energy present near a scene start (expect ~ -22 to -28 dB, not silence)
ffmpeg -ss 40 -t 3 -i episodes/ep01/short-3min-voiced.mp4 -af volumedetect -f null - 2>&1 | grep mean_volume
```

Also eyeball it: scrub to a known reveal (e.g. the "59M" counter in scene 8) and
confirm the number animates **as** "fifty-nine million" is spoken. Confirm the
tone sounds joyful, not strict.

## 7. Commit + push

```bash
cd ../..   # repo root (videos/)
git add tti-studio/episodes/ep01/short-3min_synced.html \
        tti-studio/episodes/ep01/short-3min-voiced.mp4
git commit -m "Ep1 short: word-synced Dhruva voiceover (local render)"
git push origin claude/eager-shannon-i79f3n
```

---

### If a scene's sync feels off

The reveal-to-word mapping lives in the `BEATS` dict in `sync_build.py`. Each
entry is `("narration text", [element ids that should appear here])`. Move an id
to a different beat to change *when* it lands, then re-run step 3–5. The cached
audio is reused, so iteration is fast (only the HTML + audio mux rebuild).

### Tunable knobs (top of `sync_build.py`)

| Const | Default | Effect |
|---|---|---|
| `LEAD` | 0.25 | reveal lands this many seconds *before* the word |
| `STAGGER` | 0.40 | gap between multiple reveals in one beat |
| `TAIL_PAD` | 1.40 | quiet hold after the last word before the scene exits |
| `VOICE_SETTINGS` | 0.40/0.75/0.45 | stability / similarity / style (joyful) |
