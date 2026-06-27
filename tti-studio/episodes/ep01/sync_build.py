#!/usr/bin/env python3
"""
Word-synced, joyful Dhruva voiceover + ElevenLabs SFX build for the Ep1 LONG-FORM.

Pipeline (see docs/VOICEOVER.md):
1. Per-scene TTS with the Dhruva voice (expressive/joyful) AND char-level
   timestamps (/with-timestamps). From the alignment we pin every animation
   reveal to the moment its words are spoken.
2. SFX: generate a small kit via ElevenLabs /v1/sound-generation (whoosh on
   wipes, a data-zip on the request packet, a riser on the "melt", a swell on
   the 59M counter, a soft chime on resolves). Mixed UNDER the voice at the
   exact transition/animation times.
3. Re-time each scene to its clip length, regenerate the GSAP timeline,
   write composition_synced.html, build audio_v2/main.aac (voice + SFX).

Re-runs are cheap: TTS, alignment and SFX are cached under audio_v2/.

Run (where api.elevenlabs.io is reachable, e.g. local Mac):
    cd tti-studio/episodes/ep01
    export ELEVENLABS_API_KEY="...   (needs text_to_speech permission)"
    python3 sync_build.py
Then render composition_synced.html and mux audio_v2/main.aac (see VOICEOVER.md).
"""
import base64, json, math, os, re, subprocess
from pathlib import Path
import requests

API   = os.environ["ELEVENLABS_API_KEY"]
VOICE = "7hshzsnMFQgQHNhu6yYM"           # Dhruva (professional clone)
MODEL = "eleven_multilingual_v2"
# Joyful / conversational, with a touch of briskness (speed > 1).
VOICE_SETTINGS = {"stability": 0.40, "similarity_boost": 0.75,
                  "style": 0.50, "use_speaker_boost": True, "speed": 1.06}

EP    = Path(__file__).parent
CACHE = EP / "audio_v2"; CACHE.mkdir(exist_ok=True)
SFXD  = CACHE / "sfx"; SFXD.mkdir(exist_ok=True)
SRC_HTML  = EP / "composition.html"
OUT_HTML  = EP / "composition_synced.html"
COMP_ID   = "sdep01full"

LEAD      = 0.25   # reveal this many s before the word, so it lands WITH the word
HEAD_BASE = 0.40   # headline appears just as the scene's voice starts
STAGGER   = 0.40   # micro-stagger between multiple reveals in one beat
TAIL_PAD  = 1.50   # quiet tail after last word before the scene exits

SCENES = [f"s{i}" for i in range(1, 16)]
OLD = {  # id: (old_start, old_dur) -- the draft timings in composition.html
 "s1":(0,40),"s2":(40,30),"s3":(70,40),"s4":(110,35),"s5":(145,45),
 "s6":(190,45),"s7":(235,60),"s8":(295,40),"s9":(335,45),"s10":(380,45),
 "s11":(425,45),"s12":(470,60),"s13":(530,35),"s14":(565,45),"s15":(610,45),
}
HEAD_DUR = {"s1":1.0, "s15":1.0}  # default 0.9

# ---------------------------------------------------------------------------
# BEATS: per scene, ordered (narration_text, [element ids that reveal here]).
# Text MUST concatenate (space-joined, in order) to the scene's narration.
# ---------------------------------------------------------------------------
BEATS = {
 "s1": [
  ("It's 8pm. You flop onto your bed, pull out your phone, and open your favourite app. And here's the wild part. At that same second, half your city is doing the exact same thing. Millions of taps, all at once. And the app? It just works. No crash, no spinning wheel. Ever stopped to wonder how that's even possible? Stick around, because by the end of this video you'll understand it completely. Not by memorising anything. By building one yourself.", ["s1k","s1t"]),
  ("Meet our project for the whole series. A tiny photo app. We'll call it baby Instagram.", ["s1card"]),
  ("It does two things. You post a photo. Your friends see it. That's the entire app. And it's all we need to learn how the big ones work.", ["s1tag"]),
 ],
 "s2": [
  ("Hold on to that 8pm picture. A whole city, tapping at once. And nothing breaks. That isn't luck, and it certainly isn't magic. Somebody sat down, long before launch, and planned for that crowd.", ["s2k","s2t"]),
  ("That invisible plan is system design. And it might be the most useful thing you'll ever learn as an engineer.", ["s2s"]),
 ],
 "s3": [
  ("So let's get the definition out of the way, in plain English. System design is planning how the pieces of your app fit together, before you write a single line of code. The easiest way to picture it is building a house.", ["s3k","s3t"]),
  ("Writing code is laying the bricks. It's the actual construction.", ["s3c1"]),
  ("System design is the blueprint. Where do the rooms go? Where do the pipes run? You draw that first, because nobody builds a house and figures out the bathroom afterwards.", ["s3c2"]),
 ],
 "s4": [
  ("Right. Let's actually design our baby Instagram. And we're keeping it tiny on purpose.", ["s4k","s4t"]),
  ("One simple screen. A feed, and a button to post. Here's the secret: the small version teaches you the exact same ideas as the giant version, just without the headache.", ["s4card"]),
  ("So, two jobs. One, post a photo. Two, see your friends' feed.", ["s4f1","s4f2"]),
 ],
 "s5": [
  ("Now the big idea. The one that, once it clicks, you'll start seeing everywhere. Almost every app you have ever used is really just three pieces, talking to each other.", ["s5k","s5t"]),
  ("The first piece is the client. That's a fancy word for your phone.", ["s5_cli"]),
  ("The second is the server. That's the app's brain, running on a powerful computer in some data centre, maybe a thousand kilometres away.", ["s5_srv"]),
  ("The third is the database. Picture a giant, very organised filing cabinet, where every photo actually lives.", ["s5_db"]),
  ("Client, server, database. Hold on to those three, every episode after this is built on them.", ["s5s"]),
 ],
 "s6": [
  ("So what do they actually do all day? One thing, again and again.", ["s6k","s6t"]),
  ("Your phone asks for something. Show me the latest photos. That little ask has a name. It's called a request.", ["s6_e1","s6_e2","s6_lreq"]),
  ("The server hears it, gets what's needed, and sends it back. That return trip is a response. Picture asking a librarian for a book. You ask. They walk to the shelf. They bring it back. You're the client, the librarian is the server, and the shelf is the database.", ["s6_p","s6_r1","s6_r2","s6_lres"]),
  ("One request, one response. That's quite literally every app you've ever opened.", ["s6s"]),
 ],
 "s7": [
  ("Let's slow it right down and follow one single tap.", ["s7k","s7t"]),
  ("You tap to open your feed. Your phone sends a request to the server. That's the first hop.", ["s7_e1","s7_t1"]),
  ("The server doesn't keep the photos itself, so it fetches them from the database. Second hop.", ["s7_e2","s7_t2"]),
  ("Then it all travels back. Database, to server, to your screen. All in a fraction of a second.", ["s7_p","s7_t3"]),
  ("And this is the heart of the whole episode. That exact path is hiding inside every app you use. Once you've seen it, you can't unsee it.", ["s7s"]),
 ],
 "s8": [
  ("So how do real engineers design this? Do they just start typing? Not a chance. They follow the same four steps, every time.", ["s8k","s8t"]),
  ("Step one, requirements. What are we building, and who for?", ["s8a"]),
  ("Step two, high-level design. The big boxes.", ["s8b"]),
  ("Step three, core components. Zooming into each box.", ["s8c"]),
  ("Step four, scale. Surviving a crowd.", ["s8d"]),
  ("And here's the fun part. We're going to run all four, right now, on baby Instagram.", ["s8s"]),
 ],
 "s9": [
  ("Step one. Requirements. A serious-sounding word for a simple question: what should the app do?", ["s9k","s9t"]),
  ("It should let you post a photo.", ["s9b1"]),
  ("And see your friends' feed. Easy so far. But here's the bit beginners rush past. For how many people?", ["s9b2"]),
  ("Because ten friends", ["s9n1","s9vs"]),
  ("and ten million users are not the same project. Not even close.", ["s9n2"]),
  ("Same app on the screen, completely different problem underneath. One's a footbridge. The other's a national highway.", ["s9s"]),
 ],
 "s10": [
  ("Step two. High-level design. Big name, gentle idea. You draw the boxes, and connect them.", ["s10k","s10t"]),
  ("Here's our phone, the client.", ["s10_cli"]),
  ("Here's the server.", ["s10_srv","s10_e1"]),
  ("And the database, all wired together.", ["s10_db","s10_e2"]),
  ("That's the whole move. This bird's-eye picture is your high-level design.", ["s10_brk","s10_blab","s10s"]),
 ],
 "s11": [
  ("Step three. Core components. Now we zoom inside one box.", ["s11k","s11t"]),
  ("The boxes and how they connect, that wide view, is high-level design. HLD. The map.", ["s11c1"]),
  ("But how one single photo gets stored inside the database, that close-up, is low-level design. LLD. The street view.", ["s11c2"]),
  ("Same system, two zoom levels. Today, we're staying up on the map.", ["s11s"]),
 ],
 "s12": [
  ("And now, step four. Scale. This is where it gets really fun.", ["s12k","s12t"]),
  ("Picture ten million people opening baby Instagram at 9pm. That one little server? It melts. Think of one ticket counter facing an entire stadium.", ["s12_cl","s12_spk","s12_spklab"]),
  ("So we add more servers. A whole row of them, splitting the crowd. That trick is called scaling out.", ["s12_e1","s12_s1","s12_e2","s12_s2","s12_e3","s12_s3"]),
  ("And the photos everyone wants? We keep copies close by, in a cache, so we're not bothering the database every time.", ["s12_e4","s12_cache"]),
  ("More servers, plus a cache. And just like that, green lights. We're healthy again.", ["s12s"]),
 ],
 "s13": [
  ("But here's the move that makes you sound like a real engineer. You don't build all of that on day one.", ["s13k","s13t"]),
  ("Start simple. One server. Ship it. Watch what real people actually do with it.", ["s13c1"]),
  ("Then add a new piece only when something actually breaks. Not a second sooner. You wouldn't pour a six-lane highway for a street with three houses.", ["s13c2"]),
 ],
 "s14": [
  ("And if part of you is thinking sure, but this is just a toy example, it really isn't.", ["s14k","s14t"]),
  ("When Hotstar streamed the 2023 World Cup final, fifty-nine million people were watching at the very same moment.", ["s14big"]),
  ("Fifty-nine million. And it held. The exact same request and response you just learned. There were simply a lot more boxes behind the scenes.", ["s14s"]),
 ],
 "s15": [
  ("And that's it. I mean it, you just designed an app. Let's lock in what you know.", ["s15k","s15t"]),
  ("Every app is a client, a server, and a database.", ["s15r1"]),
  ("They talk in one request, one response.", ["s15r2"]),
  ("Engineers design in four steps, every time.", ["s15r3"]),
  ("And you scale only when something breaks.", ["s15r4"]),
  ("But one question is left hanging. Your phone asked the server, so how did it even find that server, out of the entire internet? That's DNS and HTTP, and that's where we pick up next time.", ["s15next"]),
 ],
}

# Static visual params copied from composition.html (never change).
DRAW_LEN = {"s6_e1":190,"s6_e2":190,"s6_r1":190,"s6_r2":190,
            "s7_e1":190,"s7_e2":190,"s10_e1":190,"s10_e2":190,
            "s12_e1":360,"s12_e2":480,"s12_e3":360,"s12_e4":470}

# ---------------------------------------------------------------------------
def _post_tts(text):
    return requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
        headers={"xi-api-key": API, "Content-Type": "application/json"},
        json={"text": text, "model_id": MODEL, "voice_settings": VOICE_SETTINGS},
        timeout=180)

def tts_with_timestamps(text, name):
    mp3 = CACHE / f"{name}.mp3"; js = CACHE / f"{name}.align.json"
    if mp3.exists() and js.exists():
        return mp3, json.loads(js.read_text())
    print(f"  [tts] {name} ...")
    r = _post_tts(text)
    if r.status_code == 422 and "speed" in VOICE_SETTINGS:
        print("    (speed unsupported -> retrying without it)")
        VOICE_SETTINGS.pop("speed")
        r = _post_tts(text)
    r.raise_for_status()
    d = r.json()
    mp3.write_bytes(base64.b64decode(d["audio_base64"]))
    al = d["alignment"]; js.write_text(json.dumps(al))
    return mp3, al

def sfx(prompt, name, duration):
    """Generate (or load cached) a sound effect via ElevenLabs."""
    mp3 = SFXD / f"{name}.mp3"
    if mp3.exists():
        return mp3
    print(f"  [sfx] {name} ...")
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation",
        headers={"xi-api-key": API, "Content-Type": "application/json"},
        json={"text": prompt, "duration_seconds": duration, "prompt_influence": 0.45},
        timeout=180)
    r.raise_for_status()
    mp3.write_bytes(r.content)
    return mp3

# SFX kit: (name, prompt, duration_seconds, mix_gain)
# Gains kept low/subtle so SFX sit UNDER the voice (whoosh was hot at 0.32).
SFX_KIT = {
 "whoosh": ("short subtle clean UI transition whoosh, soft quick swoosh, futuristic interface, no music", 0.8, 0.16),
 "zip":    ("short soft digital data blip, quick electronic UI tick zip, subtle, no music", 0.7, 0.18),
 "riser":  ("short tension riser, low rising hum building stress, subtle ominous swell, no music", 2.0, 0.20),
 "swell":  ("rising ticking count-up swell, digital counter climbing quickly, subtle electronic, no music", 2.6, 0.22),
 "chime":  ("soft positive confirmation chime, gentle success ding, warm short, no music", 0.9, 0.20),
}

def ffdur(path):
    return float(subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration",
         "-of","default=nk=1:nw=1",str(path)],
        capture_output=True, text=True, check=True).stdout.strip())

def beat_times(beats, alignment):
    starts = alignment["character_start_times_seconds"]
    times, idx = [], 0
    for (txt, _) in beats:
        ci = min(idx, len(starts) - 1)
        times.append(starts[ci])
        idx += len(txt) + 1
    return times

def compute_reveals(beats, alignment):
    bt = beat_times(beats, alignment)
    reveal = {}
    for k, (txt, sels) in enumerate(beats):
        base = HEAD_BASE if k == 0 else max(bt[k] - LEAD, HEAD_BASE)
        for j, sel in enumerate(sels):
            reveal[sel] = round(base + j * STAGGER, 3)
    return reveal

def process():
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
    def R(sid, sel, fb=None):
        off = data[sid]["reveal"].get(sel)
        if off is None:
            off = fb if fb is not None else HEAD_BASE
        return starts[sid] + off
    DL = DRAW_LEN
    L = ["      // === word-synced to Dhruva VO (generated by sync_build.py) ==="]
    for sid in SCENES:
        s, d = starts[sid], durs[sid]
        hd = HEAD_DUR.get(sid, 0.9)
        L.append(f"\n      // {sid.upper()} ({s}-{s+d})")
        if sid != "s1":
            L.append(f"      sweep({f(s)});")
        L.append(f'      scene("#{sid}", {f(s)}, {f(d)});')
        L.append(f'      kick("#{sid}k", {f(R(sid,sid+"k"))}); head("#{sid}t", {f(R(sid,sid+"t"))}, {hd});')

        if sid == "s1":
            L.append(f'      tl.to("#s1t .ac", {{ opacity:0.72, duration:1.6, ease:"sine.inOut", repeat:6, yoyo:true }}, {f(R("s1","s1t")+5)});')
            L.append(f'      pop("#s1card", {f(R("s1","s1card"))}, 0.7); breathe("#s1card", {f(R("s1","s1card")+1.6)}, 1.02, 2.6, 5);')
            L.append(f'      pop("#s1tag", {f(R("s1","s1tag"))}, 0.7); floaty("#s1tag", {f(R("s1","s1tag")+1.4)}, -10, 2.2, 4);')
        elif sid == "s2":
            L.append(f'      rise("#s2s", {f(R("s2","s2s"))}, 20);')
        elif sid == "s3":
            L.append(f'      pop("#s3c1", {f(R("s3","s3c1"))}, 0.7); pop("#s3c2", {f(R("s3","s3c2"))}, 0.7);')
        elif sid == "s4":
            L.append(f'      pop("#s4card", {f(R("s4","s4card"))}, 0.7); breathe("#s4card", {f(R("s4","s4card")+1.6)}, 1.02, 2.6, 4);')
            L.append(f'      pop("#s4f1", {f(R("s4","s4f1"))}, 0.6); pop("#s4f2", {f(R("s4","s4f2"))}, 0.6);')
        elif sid == "s5":
            L.append(f'      pop("#s5_cli", {f(R("s5","s5_cli"))}); pop("#s5_srv", {f(R("s5","s5_srv"))}); pop("#s5_db", {f(R("s5","s5_db"))});')
            L.append(f'      rise("#s5s", {f(R("s5","s5s"))}, 18);')
        elif sid == "s6":
            L.append(f'      draw("#s6_e1", {DL["s6_e1"]}, {f(R("s6","s6_e1"))}, 0.5); draw("#s6_e2", {DL["s6_e2"]}, {f(R("s6","s6_e2"))}, 0.5); fade("#s6_lreq", {f(R("s6","s6_lreq"))});')
            L.append(f'      packet("#s6_p", 200, 150, 1400, 150, {f(R("s6","s6_p"))}, 2.2, 2);')
            L.append(f'      draw("#s6_r1", {DL["s6_r1"]}, {f(R("s6","s6_r1"))}, 0.5); draw("#s6_r2", {DL["s6_r2"]}, {f(R("s6","s6_r2"))}, 0.5); fade("#s6_lres", {f(R("s6","s6_lres"))});')
            L.append(f'      rise("#s6s", {f(R("s6","s6s"))}, 18);')
        elif sid == "s7":
            L.append(f'      draw("#s7_e1", {DL["s7_e1"]}, {f(R("s7","s7_e1"))}, 0.5); fade("#s7_t1", {f(R("s7","s7_t1"))});')
            L.append(f'      draw("#s7_e2", {DL["s7_e2"]}, {f(R("s7","s7_e2"))}, 0.5); fade("#s7_t2", {f(R("s7","s7_t2"))});')
            L.append(f'      packet("#s7_p", 200, 170, 1400, 170, {f(R("s7","s7_p"))}, 2.6, 20); fade("#s7_t3", {f(R("s7","s7_t3"))});')
            L.append(f'      rise("#s7s", {f(R("s7","s7s"))}, 18);')
        elif sid == "s8":
            L.append(f'      pop("#s8a", {f(R("s8","s8a"))}, 0.6); pop("#s8b", {f(R("s8","s8b"))}, 0.6); pop("#s8c", {f(R("s8","s8c"))}, 0.6); pop("#s8d", {f(R("s8","s8d"))}, 0.6);')
            L.append(f'      rise("#s8s", {f(R("s8","s8s"))}, 16);')
        elif sid == "s9":
            L.append(f'      rise("#s9b1", {f(R("s9","s9b1"))}, 18); rise("#s9b2", {f(R("s9","s9b2"))}, 18);')
            L.append(f'      pop("#s9n1", {f(R("s9","s9n1"))}, 0.6); pop("#s9vs", {f(R("s9","s9vs"))}, 0.5); pop("#s9n2", {f(R("s9","s9n2"))}, 0.7);')
            L.append(f'      tl.to("#s9n2", {{ scale:1.04, duration:1.4, ease:"sine.inOut", repeat:1, yoyo:true, transformOrigin:"left center" }}, {f(R("s9","s9n2")+1.5)});')
            L.append(f'      rise("#s9s", {f(R("s9","s9s"))}, 16);')
        elif sid == "s10":
            L.append(f'      pop("#s10_cli", {f(R("s10","s10_cli"))});')
            L.append(f'      pop("#s10_srv", {f(R("s10","s10_srv"))}); draw("#s10_e1", {DL["s10_e1"]}, {f(R("s10","s10_e1"))}, 0.5);')
            L.append(f'      pop("#s10_db", {f(R("s10","s10_db"))}); draw("#s10_e2", {DL["s10_e2"]}, {f(R("s10","s10_e2"))}, 0.5);')
            L.append(f'      fade("#s10_brk", {f(R("s10","s10_brk"))}); fade("#s10_blab", {f(R("s10","s10_blab"))});')
            L.append(f'      rise("#s10s", {f(R("s10","s10s"))}, 18);')
        elif sid == "s11":
            L.append(f'      pop("#s11c1", {f(R("s11","s11c1"))}, 0.7); pop("#s11c2", {f(R("s11","s11c2"))}, 0.7);')
            L.append(f'      rise("#s11s", {f(R("s11","s11s"))}, 16);')
        elif sid == "s12":
            L.append(f'      pop("#s12_cl", {f(R("s12","s12_cl"))}); fade("#s12_spk", {f(R("s12","s12_spk"))}); fade("#s12_spklab", {f(R("s12","s12_spklab"))});')
            L.append(f'      draw("#s12_e1", {DL["s12_e1"]}, {f(R("s12","s12_e1"))}, 0.6); draw("#s12_e2", {DL["s12_e2"]}, {f(R("s12","s12_e2"))}, 0.6); draw("#s12_e3", {DL["s12_e3"]}, {f(R("s12","s12_e3"))}, 0.6);')
            L.append(f'      pop("#s12_s1", {f(R("s12","s12_s1"))}); pop("#s12_s2", {f(R("s12","s12_s2"))}); pop("#s12_s3", {f(R("s12","s12_s3"))});')
            L.append(f'      draw("#s12_e4", {DL["s12_e4"]}, {f(R("s12","s12_e4"))}, 0.6); pop("#s12_cache", {f(R("s12","s12_cache"))});')
            L.append(f'      rise("#s12s", {f(R("s12","s12s"))}, 18);')
        elif sid == "s13":
            L.append(f'      pop("#s13c1", {f(R("s13","s13c1"))}, 0.7); pop("#s13c2", {f(R("s13","s13c2"))}, 0.7);')
        elif sid == "s14":
            t0 = R("s14","s14big")
            L.append(f'      pop("#s14big", {f(t0)}, 0.8);')
            L.append(f'      var hc = {{ v:59 }};')
            L.append(f'      tl.set(hc, {{ v:0 }}, {f(t0+0.5)});')
            L.append('      tl.to(hc, { v:59, duration:2.6, ease:"power1.out", onUpdate:function(){ var e=document.getElementById(\'s14num\'); if(e) e.textContent = Math.round(hc.v); } }, ' + f(t0+0.7) + ');')
            L.append(f'      breathe("#s14big", {f(t0+2.4)}, 1.03, 2.2, 4);')
            L.append(f'      rise("#s14s", {f(R("s14","s14s"))}, 18);')
        elif sid == "s15":
            L.append(f'      tl.to("#s15t .ac", {{ opacity:0.72, duration:1.5, ease:"sine.inOut", repeat:4, yoyo:true }}, {f(R("s15","s15t")+3)});')
            L.append(f'      pop("#s15r1", {f(R("s15","s15r1"))}, 0.5); pop("#s15r2", {f(R("s15","s15r2"))}, 0.5); pop("#s15r3", {f(R("s15","s15r3"))}, 0.5); pop("#s15r4", {f(R("s15","s15r4"))}, 0.5);')
            L.append(f'      rise("#s15next", {f(R("s15","s15next"))}, 18);')
    return "\n".join(L) + "\n"

def sfx_cues(starts, data):
    """List of (sfx_name, time_s, gain) placed at transition/animation moments."""
    def R(sid, sel): return starts[sid] + data[sid]["reveal"].get(sel, HEAD_BASE)
    cues = []
    g = {k: v[2] for k, v in SFX_KIT.items()}
    for sid in SCENES[1:]:                      # whoosh on every scene wipe
        cues.append(("whoosh", max(starts[sid] - 0.2, 0), g["whoosh"]))
    cues.append(("zip",   R("s6","s6_p"),   g["zip"]))     # request packet
    cues.append(("zip",   R("s7","s7_p"),   g["zip"]))     # journey packet
    cues.append(("riser", R("s12","s12_cl"), g["riser"]))  # the melt
    cues.append(("swell", R("s14","s14big") + 0.5, g["swell"]))  # 59M counter
    cues.append(("chime", R("s12","s12s"),  g["chime"]))   # healthy again
    cues.append(("chime", R("s15","s15r1"), g["chime"]))   # recap
    return cues

# ---------------------------------------------------------------------------
def transform(data):
    src = SRC_HTML.read_text()
    starts, durs, cur = {}, {}, 0
    for sid in SCENES:
        durs[sid] = math.ceil(data[sid]["clip_dur"] + TAIL_PAD)
        starts[sid] = cur; cur += durs[sid]
    total = cur

    src, n = re.subn(rf'(data-composition-id="{COMP_ID}" data-start="0" data-duration=)"\d+"',
                     rf'\g<1>"{total}"', src)
    assert n == 1, f"root duration replace n={n}"
    for sid in SCENES:
        os_, od_ = OLD[sid]
        src, n = re.subn(rf'(id="{sid}" data-start=)"{os_}"( data-duration=)"{od_}"',
                         rf'\g<1>"{starts[sid]}"\g<2>"{durs[sid]}"', src)
        assert n == 1, f"{sid} scene div replace n={n}"

    start_anchor = "      // === DRAFT TIMELINE START ==="
    end_anchor   = "      // === DRAFT TIMELINE END ==="
    si = src.index(start_anchor); ei = src.index(end_anchor)
    src = src[:si] + build_timeline(starts, durs, data) + src[ei+len(end_anchor):]
    OUT_HTML.write_text(src)
    print(f"  ✓ {OUT_HTML.name}  total={total}s")
    return starts, durs, total

def _ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000: ms = 0; s += 1
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def build_srt(starts, out):
    """Sentence-level captions from cached char alignment, offset by scene start."""
    idx, lines = 1, []
    for sid in SCENES:
        al = json.loads((CACHE / f"{sid}.align.json").read_text())
        chars = al["characters"]
        cs = al["character_start_times_seconds"]; ce = al["character_end_times_seconds"]
        text = "".join(chars); base = starts[sid]
        for m in re.finditer(r'[^.?!]+[.?!]+|\S[^.?!]*$', text):
            s_i, e_i = m.start(), m.end() - 1
            while s_i < e_i and text[s_i] == ' ': s_i += 1
            seg = text[s_i:e_i+1].strip()
            if not seg: continue
            st = base + cs[min(s_i, len(cs)-1)]
            en = base + ce[min(e_i, len(ce)-1)]
            lines += [str(idx), f"{_ts(st)} --> {_ts(en)}", seg, ""]; idx += 1
    Path(out).write_text("\n".join(lines))
    print(f"  ✓ {out}  ({idx-1} cues)")

def build_audio(starts, total, data, out):
    # voice scenes + SFX, mixed (SFX low gain, normalize off so voice stays full)
    inputs = ["-f","lavfi","-t",str(total),"-i","anullsrc=r=44100:cl=stereo"]
    fp = ["[0:a]aformat=sample_rates=44100:channel_layouts=stereo[base]"]
    mix = ["[base]"]; idx = 1
    for sid in SCENES:                          # voice
        inputs += ["-i", str(CACHE / f"{sid}.mp3")]
        ms = starts[sid] * 1000
        fp.append(f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={ms}|{ms}[v{idx}]")
        mix.append(f"[v{idx}]"); idx += 1
    for name, t, gain in sfx_cues(starts, data):  # sfx
        inputs += ["-i", str(SFXD / f"{name}.mp3")]
        ms = int(round(t * 1000))
        fp.append(f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={gain},adelay={ms}|{ms}[x{idx}]")
        mix.append(f"[x{idx}]"); idx += 1
    fp.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0[out]")
    subprocess.run(["ffmpeg","-y"]+inputs+["-filter_complex",";".join(fp),
                    "-map","[out]","-c:a","aac","-b:a","192k","-t",str(total),out],
                   check=True, capture_output=True)
    print(f"  ✓ {out}")

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Step 1: TTS (joyful Dhruva) + alignment ...")
    data = process()

    print("\nStep 2: generate SFX kit ...")
    for name, (prompt, dur, _g) in SFX_KIT.items():
        sfx(prompt, name, dur)

    print("\nStep 3: re-time + word-sync composition ...")
    starts, durs, total = transform(data)

    print("\nStep 4: build audio track (voice + SFX) ...")
    build_audio(starts, total, data, str(CACHE / "main.aac"))

    print("\nStep 5: build captions ...")
    build_srt(starts, str(EP / "script.srt"))

    print("\nScene map (start, dur, clip):")
    for s in SCENES:
        print(f"  {s:<4} start={starts[s]:>3} dur={durs[s]:>3} clip={data[s]['clip_dur']:.1f}")
    print(f"  TOTAL={total}s")
    print("\nNext: render composition_synced.html, then mux audio_v2/main.aac "
          "-> video-voiced.mp4 (see docs/VOICEOVER.md).")
