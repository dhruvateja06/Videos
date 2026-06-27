#!/usr/bin/env python3
"""
Word-synced, joyful Dhruva voiceover build for the Ep1 3-min VERTICAL SHORT.

This is the short-format sibling of docs/VOICEOVER.md's reference pipeline
(episodes/ep02/sync_build.py on the AI branch). It:

1. Generates per-scene TTS with the Dhruva voice using EXPRESSIVE (joyful)
   settings AND character-level timestamps (/with-timestamps endpoint).
2. From the alignment, computes the exact time each narration "beat" begins and
   pins every animation reveal to that moment (transitions land ON the words).
3. Re-times each scene to its clip length, regenerates the GSAP timeline, writes
   short-3min_synced.html, and builds the synced audio track audio_v2/short.aac.

Re-run is cheap: audio + alignment are cached under audio_v2/.

Run (on a machine where api.elevenlabs.io is reachable — e.g. local Mac):
    cd tti-studio/episodes/ep01
    export ELEVENLABS_API_KEY="sk_...   (needs text_to_speech permission)"
    python3 sync_build.py
Then render short-3min_synced.html and mux audio_v2/short.aac (see VOICEOVER.md).
"""
import base64, json, math, os, re, subprocess
from pathlib import Path
import requests

API   = os.environ["ELEVENLABS_API_KEY"]
VOICE = "7hshzsnMFQgQHNhu6yYM"           # Dhruva (professional clone)
MODEL = "eleven_multilingual_v2"
# Joyful / conversational delivery (matches docs/VOICEOVER.md — NOT the strict 0.55/0.20).
VOICE_SETTINGS = {"stability": 0.40, "similarity_boost": 0.75,
                  "style": 0.45, "use_speaker_boost": True}

EP    = Path(__file__).parent
CACHE = EP / "audio_v2"; CACHE.mkdir(exist_ok=True)
SRC_HTML  = EP / "short-3min.html"
OUT_HTML  = EP / "short-3min_synced.html"
COMP_ID   = "sdep01short"

LEAD      = 0.25   # reveal this many s before the word, so it lands WITH the word
HEAD_BASE = 0.35   # headline appears just as the scene's voice starts
STAGGER   = 0.40   # micro-stagger between multiple reveals in one beat
TAIL_PAD  = 1.40   # quiet tail after last word before the scene exits

# Scene order + ORIGINAL (silent-draft) starts/durations, used to keep the
# background loops sane and to find each scene div for rewriting.
SCENES = ["s1","s2","s3","s4","s5","s6","s7","s8","s9"]
OLD = {  # id: (old_start, old_dur)
 "s1":(0,22),"s2":(22,15),"s3":(37,20),"s4":(57,14),"s5":(71,15),
 "s6":(86,19),"s7":(105,15),"s8":(120,16),"s9":(136,15),
}

# ---------------------------------------------------------------------------
# BEATS: per scene, ordered (narration_text, [element ids that reveal here]).
# A beat with [] just advances the narration (talk-over). Multiple ids in one
# beat micro-stagger by STAGGER. Text MUST concatenate (in order, space-joined)
# to the exact narration sent to TTS for that scene.
# ---------------------------------------------------------------------------
BEATS = {
 "s1": [
  ("It's 8pm. You open Swiggy. So does half your city, all at once.", ["s1k","s1t"]),
  ("And the app doesn't crash. It doesn't even lag. It just works. Ever wonder how? That's system design.", []),
  ("And the best way to get it? Build it yourself. So let's design a tiny app. A baby Instagram.", ["s1card"]),
  ("You post a photo, your friends see it.", ["s1tag"]),
 ],
 "s2": [
  ("So what is it?", ["s2k","s2t"]),
  ("System design is just planning your app's pieces, and how they connect, before you write any code.", []),
  ("Code is laying bricks.", ["s2c1"]),
  ("System design is the blueprint. So before we build, we plan.", ["s2c2"]),
 ],
 "s3": [
  ("Here's the trick. Almost every app is really just three things.", ["s3k","s3t"]),
  ("Your phone, the client.", ["m_cli"]),
  ("The app, on a computer somewhere, the server.", ["m_e1","m_srv"]),
  ("And where your photos live, the database.", ["m_e2","m_db"]),
  ("You post a photo: your phone asks, the server answers.", ["m_p1"]),
  ("That's a request, and a response. Every app, ever.", ["s3s"]),
 ],
 "s4": [
  ("And to design one, engineers always follow the same four steps.", ["s4k","s4t"]),
  ("Requirements.", ["s4a"]),
  ("High level design.", ["s4b"]),
  ("Core components.", ["s4c"]),
  ("Then scale. Let's run all four on baby Instagram.", ["s4d"]),
 ],
 "s5": [
  ("Step one, requirements. What should it do?", ["s5k","s5t"]),
  ("Post a photo,", ["s5b1"]),
  ("and see your friends' feed.", ["s5b2"]),
  ("But here's what beginners skip. For how many people?", []),
  ("Ten friends,", ["s5n1","s5vs"]),
  ("or ten million? Completely different problems.", ["s5n2"]),
 ],
 "s6": [
  ("Now, scaling. Ten friends? One server is fine.", ["s6k","s6t"]),
  ("But ten million at 9pm? That server melts.", ["sc_cl"]),
  ("So we add more servers to share the crowd. That's scaling out.",
     ["sc_e1","sc_s1","sc_e2","sc_s2","sc_e3","sc_s3"]),
  ("And we keep the popular photos nearby, in a cache.", ["sc_e4","sc_cache"]),
  ("More users, more boxes. Same idea.", ["s6s"]),
 ],
 "s7": [
  ("Two words you'll hear everywhere.", ["s7k","s7t"]),
  ("The boxes we drew? That's high level design. HLD.", ["s7c1"]),
  ("The code inside one box? Low level design. LLD. Same job, two zoom levels.", ["s7c2"]),
 ],
 "s8": [
  ("And this is real.", ["s8k","s8t"]),
  ("When Hotstar streamed the 2023 World Cup final, fifty nine million people were watching, at the same moment.",
     ["s8big"]),
  ("The same request and response. Just a lot more boxes.", ["s8s"]),
 ],
 "s9": [
  ("And that's it. You just designed an app.", ["s9k","s9t"]),
  ("Decide the pieces, connect them, keep it fast and standing as it grows. That's system design.", []),
  ("Follow along, and we'll build the whole thing, one box at a time.", ["s9s"]),
 ],
}

# Static visual params copied from short-3min.html (these never change).
DRAW_LEN = {"m_e1":130,"m_e2":130,"sc_e1":360,"sc_e2":300,"sc_e3":360,"sc_e4":220}

# ---------------------------------------------------------------------------
def tts_with_timestamps(text, name):
    """Generate (or load cached) audio + char alignment for one scene."""
    mp3 = CACHE / f"{name}.mp3"
    js  = CACHE / f"{name}.align.json"
    if mp3.exists() and js.exists():
        return mp3, json.loads(js.read_text())
    print(f"  [tts] {name} ...")
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
        headers={"xi-api-key": API, "Content-Type": "application/json"},
        json={"text": text, "model_id": MODEL, "voice_settings": VOICE_SETTINGS},
        timeout=180)
    r.raise_for_status()
    d = r.json()
    mp3.write_bytes(base64.b64decode(d["audio_base64"]))
    al = d["alignment"]
    js.write_text(json.dumps(al))
    return mp3, al

def ffdur(path):
    return float(subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration",
         "-of","default=nk=1:nw=1",str(path)],
        capture_output=True, text=True, check=True).stdout.strip())

def beat_times(beats, alignment):
    """Start time (s) of each beat, from char-level alignment."""
    starts = alignment["character_start_times_seconds"]
    times, idx = [], 0
    for (txt, _) in beats:
        ci = min(idx, len(starts) - 1)
        times.append(starts[ci])
        idx += len(txt) + 1   # +1 for the space joining beats
    return times

def compute_reveals(beats, alignment):
    """Map element id -> reveal OFFSET (s, relative to scene start)."""
    bt = beat_times(beats, alignment)
    reveal = {}
    for k, (txt, sels) in enumerate(beats):
        base = HEAD_BASE if k == 0 else max(bt[k] - LEAD, HEAD_BASE)
        for j, sel in enumerate(sels):
            reveal[sel] = round(base + j * STAGGER, 3)
    return reveal

def process():
    """TTS every scene -> {sid: {reveal, clip_dur, mp3}}."""
    out = {}
    for sid in SCENES:
        text = " ".join(b[0] for b in BEATS[sid])
        mp3, al = tts_with_timestamps(text, sid)
        out[sid] = {"reveal": compute_reveals(BEATS[sid], al),
                    "clip_dur": ffdur(mp3), "mp3": str(mp3)}
    return out

# ---------------------------------------------------------------------------
def f(n):
    n = round(float(n), 3)
    return str(int(n)) if abs(n - round(n)) < 1e-9 else f"{n:g}"

def build_timeline(starts, durs, data):
    """Regenerate the scene-call section of the GSAP timeline, word-pinned."""
    def R(sid, sel, fallback=None):
        off = data[sid]["reveal"].get(sel)
        if off is None:
            off = fallback if fallback is not None else HEAD_BASE
        return starts[sid] + off

    L = []
    L.append("      // === word-synced to Dhruva VO (generated by sync_build.py) ===")
    for sid in SCENES:
        s, d = starts[sid], durs[sid]
        L.append(f"\n      // {sid.upper()} ({s}-{s+d})")
        if sid != "s1":
            L.append(f"      sweep({f(s)});")
        L.append(f'      scene("#{sid}", {f(s)}, {f(d)});')
        L.append(f'      kick("#{sid}k", {f(R(sid, sid+"k"))}); '
                 f'head("#{sid}t", {f(R(sid, sid+"t"))}, 0.9);')

        if sid == "s1":
            L.append(f'      tl.to("#s1t .cy", {{ opacity:0.72, duration:1.6, ease:"sine.inOut", repeat:4, yoyo:true }}, {f(R("s1","s1t")+4.3)});')
            L.append(f'      pop("#s1card", {f(R("s1","s1card"))}, 0.7); breathe("#s1card", {f(R("s1","s1card")+1.6)}, 1.02, 2.4, 4);')
            L.append(f'      pop("#s1tag", {f(R("s1","s1tag"))}, 0.7); breathe("#s1tag", {f(R("s1","s1tag")+1.4)}, 1.04, 1.4, 2);')
        elif sid == "s2":
            L.append(f'      pop("#s2c1", {f(R("s2","s2c1"))}, 0.7); pop("#s2c2", {f(R("s2","s2c2"))}, 0.7);')
        elif sid == "s3":
            L.append(f'      pop("#m_cli", {f(R("s3","m_cli"))}); draw("#m_e1", {DRAW_LEN["m_e1"]}, {f(R("s3","m_e1"))}, 0.6); pop("#m_srv", {f(R("s3","m_srv"))});')
            L.append(f'      draw("#m_e2", {DRAW_LEN["m_e2"]}, {f(R("s3","m_e2"))}, 0.6); pop("#m_db", {f(R("s3","m_db"))});')
            L.append(f'      packet("#m_p1", 320, 170, 320, 600, {f(R("s3","m_p1"))}, 1.8, 2);')
            L.append(f'      rise("#s3s", {f(R("s3","s3s"))}, 18);')
        elif sid == "s4":
            L.append(f'      pop("#s4a", {f(R("s4","s4a"))}, 0.6); pop("#s4b", {f(R("s4","s4b"))}, 0.6); '
                     f'pop("#s4c", {f(R("s4","s4c"))}, 0.6); pop("#s4d", {f(R("s4","s4d"))}, 0.6);')
        elif sid == "s5":
            L.append(f'      rise("#s5b1", {f(R("s5","s5b1"))}, 18); rise("#s5b2", {f(R("s5","s5b2"))}, 18);')
            L.append(f'      pop("#s5n1", {f(R("s5","s5n1"))}, 0.6); pop("#s5vs", {f(R("s5","s5vs"))}, 0.5); pop("#s5n2", {f(R("s5","s5n2"))}, 0.7);')
            L.append(f'      tl.to("#s5n2", {{ scale:1.04, duration:1.4, ease:"sine.inOut", repeat:1, yoyo:true, transformOrigin:"left center" }}, {f(R("s5","s5n2")+1.5)});')
        elif sid == "s6":
            L.append(f'      pop("#sc_cl", {f(R("s6","sc_cl"))});')
            L.append(f'      draw("#sc_e1", {DRAW_LEN["sc_e1"]}, {f(R("s6","sc_e1"))}, 0.6); '
                     f'draw("#sc_e2", {DRAW_LEN["sc_e2"]}, {f(R("s6","sc_e2"))}, 0.6); '
                     f'draw("#sc_e3", {DRAW_LEN["sc_e3"]}, {f(R("s6","sc_e3"))}, 0.6);')
            L.append(f'      pop("#sc_s1", {f(R("s6","sc_s1"))}); pop("#sc_s2", {f(R("s6","sc_s2"))}); pop("#sc_s3", {f(R("s6","sc_s3"))});')
            L.append(f'      draw("#sc_e4", {DRAW_LEN["sc_e4"]}, {f(R("s6","sc_e4"))}, 0.6); pop("#sc_cache", {f(R("s6","sc_cache"))});')
            L.append(f'      rise("#s6s", {f(R("s6","s6s"))}, 18);')
        elif sid == "s7":
            L.append(f'      pop("#s7c1", {f(R("s7","s7c1"))}, 0.7); pop("#s7c2", {f(R("s7","s7c2"))}, 0.7);')
        elif sid == "s8":
            t0 = R("s8","s8big")
            L.append(f'      pop("#s8big", {f(t0)}, 0.8);')
            L.append(f'      var hc = {{ v:59 }};')
            L.append(f'      tl.set(hc, {{ v:0 }}, {f(t0+0.5)});')
            L.append('      tl.to(hc, { v:59, duration:2.4, ease:"power1.out", onUpdate:function(){ var e=document.getElementById(\'s8num\'); if(e) e.textContent = Math.round(hc.v); } }, ' + f(t0+0.7) + ');')
            L.append(f'      breathe("#s8big", {f(t0+2.4)}, 1.03, 2.0, 2);')
            L.append(f'      rise("#s8s", {f(R("s8","s8s"))}, 18);')
        elif sid == "s9":
            L.append(f'      tl.to("#s9t .cy", {{ opacity:0.72, duration:1.5, ease:"sine.inOut", repeat:3, yoyo:true }}, {f(R("s9","s9t")+2.6)});')
            L.append(f'      rise("#s9s", {f(R("s9","s9s"))}, 18);')
    return "\n".join(L) + "\n"

def transform(data):
    src = SRC_HTML.read_text()

    # 1. new scene starts/durations
    starts, durs, cur = {}, {}, 0
    for sid in SCENES:
        durs[sid] = math.ceil(data[sid]["clip_dur"] + TAIL_PAD)
        starts[sid] = cur
        cur += durs[sid]
    total = cur

    # 2. root duration
    src, n = re.subn(rf'(data-composition-id="{COMP_ID}" data-start="0" data-duration=)"\d+"',
                     rf'\g<1>"{total}"', src)
    assert n == 1, f"root duration replace n={n}"

    # 3. each scene div data-start / data-duration
    for sid in SCENES:
        os_, od_ = OLD[sid]
        src, n = re.subn(rf'(id="{sid}" data-start=)"{os_}"( data-duration=)"{od_}"',
                         rf'\g<1>"{starts[sid]}"\g<2>"{durs[sid]}"', src)
        assert n == 1, f"{sid} scene div replace n={n}"

    # 4. swap the scene-call section of the timeline (keep bg loops + helper defs)
    start_anchor = "      // 1. HOOK"
    end_anchor   = '\n      window.__timelines["' + COMP_ID + '"] = tl;'
    si = src.index(start_anchor)
    ei = src.index(end_anchor)
    src = src[:si] + build_timeline(starts, durs, data) + src[ei+1:]

    OUT_HTML.write_text(src)
    print(f"  ✓ {OUT_HTML.name}  total={total}s")
    return starts, durs, total

def build_audio(starts, total, out):
    inputs = ["-f","lavfi","-t",str(total),"-i","anullsrc=r=44100:cl=stereo"]
    fp = ["[0:a]aformat=sample_rates=44100:channel_layouts=stereo[base]"]; mix=["[base]"]
    for i, sid in enumerate(SCENES):
        inputs += ["-i", str(CACHE / f"{sid}.mp3")]
        d = starts[sid] * 1000
        fp.append(f"[{i+1}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={d}|{d}[d{i}]")
        mix.append(f"[d{i}]")
    fp.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0[out]")
    subprocess.run(["ffmpeg","-y"]+inputs+["-filter_complex",";".join(fp),
                    "-map","[out]","-c:a","aac","-b:a","192k","-t",str(total),out],
                   check=True, capture_output=True)
    print(f"  ✓ {out}")

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Step 1: TTS (joyful Dhruva) + alignment ...")
    data = process()

    print("\nStep 2: re-time + word-sync composition ...")
    starts, durs, total = transform(data)

    print("\nStep 3: build audio track ...")
    build_audio(starts, total, str(CACHE / "short.aac"))

    print("\nScene map (start, dur, clip):")
    for s in SCENES:
        print(f"  {s:<4} start={starts[s]:>3} dur={durs[s]:>3} clip={data[s]['clip_dur']:.1f}")
    print(f"  TOTAL={total}s")
    print("\nNext: render short-3min_synced.html, then mux audio_v2/short.aac "
          "-> short-3min-voiced.mp4 (see docs/VOICEOVER.md).")
