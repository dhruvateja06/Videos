# The Tech Intern — Voiceover & Word-Level Sync

> **The locked-in process for adding voiceover to an episode.** Render silent
> first (per `PIPELINE.md`), then run this. The result is a fully-voiced MP4 where
> **every animation and transition lands ON the spoken words**, not just per-scene.
> This is now a standard production phase — follow it every episode.

## What changed (and why)

The channel started as "render silent, creator records voiceover later." We now
generate the voiceover with the creator's **own ElevenLabs voice** and sync the
visuals to it automatically. A naïve overlay (voice on top of the fixed-timing
video) leaves dead air in short scenes and clips long ones, and the animations
fire early. The fix is **word-level sync**: re-time each scene to its narration
and pin every reveal to the exact moment its words are spoken.

## The voice (non-negotiable)

| Setting | Value |
|---|---|
| Voice | **Dhruva** (the creator's professional voice) |
| `voice_id` | `7hshzsnMFQgQHNhu6yYM` |
| `model_id` | `eleven_multilingual_v2` |
| Tone | **joyful, conversational, "delighted lecturer"** — never strict/formal |
| `voice_settings` | `stability 0.40, similarity_boost 0.75, style 0.45, use_speaker_boost true` |

> The old strict-sounding settings (stability 0.55 / style 0.20) were explicitly
> rejected. Lower stability = more emotional range; higher style = more expressive.

**API key:** provided per session as the `ELEVENLABS_API_KEY` env var. It **must
have the `text_to_speech` permission** enabled (a key that can only list voices
will 401 on synthesis).

## How word-sync works

1. **Beats.** Break each scene's narration into ordered beats — each beat is
   `(text, [element ids that reveal here])`. A beat with no ids is pure talk-over.
2. **Timestamps.** Generate per-scene TTS via the ElevenLabs
   `/v1/text-to-speech/{voice_id}/with-timestamps` endpoint. It returns
   `alignment` with character-level start times. The time a beat begins = the
   start time of its first character in the scene's text.
3. **Re-time scenes.** `new_dur = ceil(clip_dur + ~1.6s tail)`; scene starts are
   the cumulative sum. (Episodes get shorter/longer than the silent draft — that's
   expected; the joyful read is a touch quicker.)
4. **Pin reveals.** Rewrite the composition's GSAP timeline:
   - **Discrete reveals** (`head/kick/rise/pop/cellL/cellR`, reveal `tl.fromTo`) →
     `scene_start + beat_time − 0.25s lead` (so the element lands *with* the word).
     Multiple reveals in one beat micro-stagger by 0.4s.
   - **Ambient loops** (`breathe/floaty`, any `tl.to` with `repeat:`) stay relative
     to scene start — they keep the frame alive and must not be word-pinned.
   - **Wipes** snap to the scene boundary.
5. **Re-render** the re-timed composition, then **mux** the synced audio.

## The reference implementation

`episodes/ep02/sync_build.py` is the canonical, re-runnable pipeline (TTS +
timestamps → re-time → rewrite GSAP → build audio). **Copy it as the starting kit
for any new episode** and replace the `MAIN` / `OUTRO` beat maps and the `OLD`
scene table with the new episode's numbers. It caches audio under `audio_v2/`
(gitignored) so re-runs are cheap.

## Commands (per episode)

```bash
cd tti-studio/episodes/epNN
export PATH="/opt/homebrew/bin:$PATH"
export ELEVENLABS_API_KEY="<key with text_to_speech permission>"

# 1. Generate joyful TTS + timestamps, re-time + word-sync both compositions,
#    build the synced audio tracks (audio_v2/main.aac, audio_v2/outro.aac)
python3 sync_build.py

# 2. Render the re-timed compositions (silent) — from the project root
cd ../..
npx --yes hyperframes@0.7.5 render . -c episodes/epNN/composition_synced.html \
   -o renders/epNN-v2.mp4 --fps 24 --quality standard --workers 4
npx --yes hyperframes@0.7.5 render . -c episodes/epNN/composition-outro_synced.html \
   -o renders/epNN-outro-v2.mp4 --fps 24 --quality standard --workers 2

# 3. Mux voice + compress near-lossless to the voiced deliverables
ffmpeg -y -i renders/epNN-v2.mp4 -i episodes/epNN/audio_v2/main.aac \
   -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 20 -preset medium \
   -movflags +faststart -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest \
   episodes/epNN/video-voiced.mp4
ffmpeg -y -i renders/epNN-outro-v2.mp4 -i episodes/epNN/audio_v2/outro.aac \
   -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 20 -preset medium \
   -movflags +faststart -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest \
   episodes/epNN/outro-voiced.mp4
```

## Outputs & naming (keep this convention)

| File | What |
|---|---|
| `composition.html` / `composition-outro.html` | original **silent** sources (deck-validated) — leave untouched |
| `composition_synced.html` / `composition-outro_synced.html` | **re-timed, word-synced** render sources |
| `sync_build.py` | the per-episode voiceover pipeline |
| `audio_v2/` | TTS clips + alignment + intermediate audio (**gitignored** cache) |
| `video-voiced.mp4` / `outro-voiced.mp4` | **final voiced deliverables** |

## QA before delivery

- Duration: voiced MP4 length == audio length (no truncation).
- Voice energy present at every scene start (`ffmpeg ... volumedetect`, ~−22 to −28 dB).
- Spot-check word-sync visually: grab a frame just **before** and **after** a known
  reveal time and confirm the element appears on cue.
- Confirm the tone sounds joyful, not strict.

## Fresh-clone toolchain

A fresh clone has none of the renderer toolchain. Install once:

```bash
brew install node ffmpeg
npx --yes hyperframes@0.7.5 browser ensure   # uses system Chrome if present
```

(HyperFrames runs via `npx hyperframes@0.7.5`; no global install needed.)
