#!/usr/bin/env python3
"""
Word-synced, joyful voiceover build for ep02.

1. Generate per-scene TTS with the Dhruva voice using EXPRESSIVE (joyful) settings
   AND character-level timestamps (/with-timestamps endpoint).
2. From the alignment, compute the exact time each narration "beat" begins, and
   pin every animation reveal to that moment (so transitions land ON the words).
3. Re-time each scene to its clip length, rewrite composition.html and the outro,
   and build the synced audio tracks.

Re-run is cheap: audio + alignment are cached under audio_v2/.
"""
import base64, json, math, os, re, subprocess
from pathlib import Path
import requests

API   = os.environ["ELEVENLABS_API_KEY"]
VOICE = "7hshzsnMFQgQHNhu6yYM"           # Dhruva (professional)
MODEL = "eleven_multilingual_v2"
# Joyful / conversational delivery: lower stability = more emotional range,
# higher style = more expressive. (vs the old strict 0.55/0.20.)
VOICE_SETTINGS = {"stability": 0.40, "similarity_boost": 0.75,
                  "style": 0.45, "use_speaker_boost": True}

EP    = Path(__file__).parent
CACHE = EP / "audio_v2"; CACHE.mkdir(exist_ok=True)

LEAD      = 0.25   # reveal this many s before the word, so it lands WITH the word
HEAD_BASE = 0.35   # headline appears just as the scene's voice starts
STAGGER   = 0.40   # micro-stagger between multiple reveals in one beat
TAIL_PAD  = 1.6    # quiet tail after last word before the scene exits

# ---------------------------------------------------------------------------
# BEATS: per scene, ordered (narration_text, [element ids that reveal here]).
# A beat with [] just advances the narration (talk-over, no new visual).
# ---------------------------------------------------------------------------
MAIN = {
 "s1": [
  ("Hey — welcome back to The Tech Intern! This is lesson two, and honestly, I'm kind of excited about this one.", ["s1k","s1t"]),
  ("Because today we're untangling four little words that trip up almost everybody: AI, Machine Learning, Deep Learning, and Generative AI.", ["s1s"]),
  ("You hear them everywhere, right? And by the time we're done here, you'll have this one simple picture in your head that just makes it all click. Let's get into it.", []),
 ],
 "s2": [
  ("Okay, quick experiment. Open LinkedIn right now and just scroll for thirty seconds. I'm serious, go ahead.", ["s2t"]),
  ("You'll find somebody — usually a super-confident founder — saying, we use AI for personalization.", ["s2m1"]),
  ("Then the next day, same company: we trained a Machine Learning model.", ["s2m2"]),
  ("Then a press release: our Deep Learning system.", ["s2m3"]),
  ("And on stage: it's all powered by Generative AI! Same product, four different words.", ["s2m4"]),
  ("And look, I'm not poking fun — even people deep in this field mix them up. But once I show you the right picture, trust me, you literally can't un-see it.", []),
 ],
 "s3": [
  ("Real quick, one sentence from last week — that's all we need.", ["s3t"]),
  ("AI is software that learns the pattern from examples, instead of being handed the rules. Rules versus patterns, remember?", ["s3strip"]),
  ("We're keeping that. Today we're just zooming in — because inside that pattern world, there are layers. And those layers? They're our four words.", ["s3s"]),
 ],
 "s4": [
  ("Alright, here's the move that fixes this for good. Watch this.", ["s4t"]),
  ("These four words aren't four separate things.", []),
  ("They're four boxes, tucked inside each other. The biggest one — that's AI.", ["s4-ai","s4-lai"]),
  ("Inside it, a little smaller, Machine Learning.", ["s4-ml","s4-lml"]),
  ("Inside that, smaller still, Deep Learning.", ["s4-dl","s4-ldl"]),
  ("And right in the middle, the tiniest doll — Generative AI.", ["s4-gen","s4-lgen"]),
  ("So every Generative AI is also Deep Learning, which is Machine Learning, which is AI. Like Russian dolls. The other way around? Not always. Get this picture, and honestly the rest is just details.", ["s4s"]),
 ],
 "s5": [
  ("Box one, the big one: AI. The simplest way to say it? Any time a computer does something that feels a bit human.", ["s5t"]),
  ("So that chess program that beat Kasparov back in 1997? That was AI.", ["s5b1"]),
  ("The spam filter quietly cleaning your inbox? Also AI.", ["s5b2"]),
  ("And yeah, ChatGPT? AI too.", ["s5b3"]),
  ("So AI is the whole field — the giant umbrella. Everything else we talk about lives inside it. Now let's go one box smaller, because that's where it gets fun.", ["s5s"]),
 ],
 "s6": [
  ("Box two, sitting inside AI: Machine Learning. And this one's simple — it's AI that learns from data, instead of following rules somebody typed out by hand.", ["s6t"]),
  ("Remember the Swiggy line drawn through that cloud of dots last episode? Yep — that was Machine Learning.", ["s6strip"]),
  ("So not all AI is ML — but almost everything exciting from the last decade? That's ML.", ["s6s"]),
 ],
 "s7": [
  ("Let me make this real, because examples stick. Picture this: you try to send fifty thousand rupees over UPI, at three in the morning, to a number you've never paid, from a city you've never been in.", ["s7phone","s7t"]),
  ("What happens? Blocked. Held. Or the app just flat-out says nope.", ["s7badge"]),
  ("Now here's the thing — nobody at NPCI sat down and wrote that exact rule.", ["s7b1"]),
  ("Instead, a model looked at billions of real transactions and figured out, all on its own, what fishy looks like.", ["s7b2"]),
  ("That's Machine Learning, living in your pocket, quietly saving your money every single day.", ["s7b3"]),
 ],
 "s8": [
  ("Box three, going a level deeper — literally: Deep Learning. It's just Machine Learning that uses one special tool to find the pattern — a neural network.", ["s8t"]),
  ("And don't stress, we've got a whole module on these later.", ["s8nn"]),
  ("But picture a giant web of tiny calculators,", ["s8b1"]),
  ("all wired up in layers,", ["s8b2"]),
  ("kind of like a little brain built out of math.", ["s8b3"]),
  ("Regular ML draws one neat line. Deep Learning can catch patterns so wild — your face in a crowd, your voice in a noisy room, a tumor on an X-ray — that the simpler stuff just can't keep up. That's the whole story.", []),
 ],
 "s9": [
  ("Quick aside, because everybody secretly wonders — why deep?", ["s9t"]),
  ("It's the layers. One layer is just a single sum.", ["s9l1"]),
  ("Three layers? We call that shallow.", ["s9l2"]),
  ("A hundred layers — now that's deep.", ["s9l3"]),
  ("And ChatGPT? Hundreds of layers, billions of connections.", ["s9l4"]),
  ("Deep doesn't mean smart or philosophical. It literally just means lots of layers stacked up. That's the whole name.", ["s9s"]),
 ],
 "s10": [
  ("Deep Learning example time. Grab your phone, open the camera, point it at a face. See that little box snap around it? Flip to portrait mode and boom — background goes dreamy and blurred, face stays sharp.", ["s10phone","s10t"]),
  ("How? Your phone is running a Deep Learning model right now, trained on millions and millions of photos.", ["s10b1"]),
  ("A neural network — running in your pocket — that just knows what a face is.", ["s10b2"]),
  ("Same exact tech helps farmers in Karnataka spot crop disease from a leaf, and helps doctors catch tumors a human eye might miss.", ["s10b3"]),
 ],
 "s11": [
  ("And box four — the smallest, the newest, and right now by far the loudest: Generative AI. It's Deep Learning that does one mind-bending thing — it creates brand new stuff.", ["s11t"]),
  ("New text,", ["s11m1"]),
  ("new images,", ["s11m2"]),
  ("new code,", ["s11m3"]),
  ("new music,", ["s11m4"]),
  ("new video.", ["s11m5"]),
  ("Here's why that's wild: until about 2022, almost every model just picked an answer from a menu. Generative AI flipped it — instead of picking, it makes. And every bit of it is still Deep Learning, which is ML, which is AI. All four boxes, nested.", ["s11s"]),
 ],
 "s12": [
  ("You know this one already — ChatGPT, Gemini, Claude.", ["s12phone","s12t"]),
  ("You type, write an email to my landlord about the leaking tap.", ["s12you"]),
  ("And a full, polite, perfectly-on-topic email just... appears.", ["s12ai","s12typing"]),
  ("That email did not exist five seconds ago. Nobody wrote it.", ["s12b1"]),
  ("The model painted it, one word at a time, by guessing what comes next.", ["s12b2"]),
  ("Same trick gives you images, code, even video. That's GenAI — the tiny box everyone's obsessed with. And honestly? Fair enough.", ["s12b3"]),
 ],
 "s13": [
  ("Okay — the whole map, one screen. This is the picture I want living in your head.", ["s13t"]),
  ("Outermost box, AI — any computer that seems clever, all the way back to that nineties chess program.", ["s13-ai","s13-lai","s13-eai"]),
  ("Inside it, Machine Learning — stuff that learned from data, like UPI fraud detection.", ["s13-ml","s13-lml","s13-eml"]),
  ("Inside that, Deep Learning — powered by neural networks, like your phone camera.", ["s13-dl","s13-ldl","s13-edl"]),
  ("And the smallest one, right in the middle, Generative AI — the part that creates new things, like ChatGPT.", ["s13-gen","s13-lgen","s13-egen"]),
  ("Four boxes, four examples, one mental model. That's the whole episode, really. You've got it.", []),
 ],
 "s14": [
  ("So here's your new little habit, starting today. Someone says, oh, we used AI to do this.", ["s14t"]),
  ("And now you get to gently ask — which box? Is it Machine Learning, learning from data? Deep Learning, with neural networks? Or Generative AI, actually making something new?", ["s14b"]),
  ("And nine times out of ten, the person who said AI... won't actually know. But now you do — and suddenly you're the calmest, clearest person in the room.", ["s14s"]),
 ],
 "s15": [
  ("Let's lock it in — four boxes, four sentences.", ["s15t"]),
  ("AI — computers doing something smart.", ["s15la","s15da"]),
  ("Machine Learning — AI that learns from data.", ["s15lb","s15db"]),
  ("Deep Learning — Machine Learning using neural networks.", ["s15lc","s15dc"]),
  ("And Generative AI — Deep Learning that creates new things.", ["s15ld","s15dd"]),
  ("Read those four lines to yourself once a week for a month, and they're yours for the rest of your career. Nice work.", []),
 ],
}

OUTRO = {
 "s16": [
  ("Next time, episode three: Data, Model, Prediction.", ["s16k","s16t"]),
  ("It's the three-step framework every single AI system on Earth runs on — Swiggy, ChatGPT, your phone camera, same three steps every time. We'll walk through it together.", ["s16card"]),
  ("If these four words finally clicked today, do me a tiny favour — send this to that one cousin who keeps mixing up AI and ChatGPT. They'll thank you, and you'll sound brilliant.", ["s16cta1","s16cta2"]),
  ("Hit subscribe so you catch the next one. See you there!", ["s16sign"]),
 ],
}

# Original scene starts/durations (to keep ambient loops relative to scene start)
OLD = {  # id: (old_start, old_dur)
 "s1":(0,30),"s2":(30,45),"s3":(75,35),"s4":(110,50),"s5":(160,55),"s6":(215,45),
 "s7":(260,55),"s8":(315,55),"s9":(370,30),"s10":(400,50),"s11":(450,55),
 "s12":(505,50),"s13":(555,45),"s14":(600,30),"s15":(630,30),
}

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
    """Return list of beat start-times (s) aligned to the spoken text."""
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    joined = " ".join(b[0] for b in beats)
    # sanity: alignment should match our text length closely
    times, idx = [], 0
    for k, (txt, _) in enumerate(beats):
        # char index of this beat's first character in `joined`
        ci = min(idx, len(starts)-1)
        times.append(starts[ci])
        idx += len(txt) + 1  # +1 for the joining space
    return times

def compute_reveals(beats, alignment):
    """Map each element id -> reveal time (s, relative to scene start)."""
    bt = beat_times(beats, alignment)
    reveal = {}
    for k, (txt, sels) in enumerate(beats):
        base = HEAD_BASE if k == 0 else max(bt[k] - LEAD, HEAD_BASE)
        for j, sel in enumerate(sels):
            reveal["#" + sel] = round(base + j * STAGGER, 3)
    return reveal

def process(beats_map):
    """Generate audio + return {id:{reveal, clip_dur}} for each scene."""
    out = {}
    for sid, beats in beats_map.items():
        text = " ".join(b[0] for b in beats)
        mp3, al = tts_with_timestamps(text, sid)
        out[sid] = {"reveal": compute_reveals(beats, al),
                    "clip_dur": ffdur(mp3), "mp3": str(mp3)}
    return out

# ---------------------------------------------------------------------------
def fmt(n):
    return str(int(round(n))) if abs(n-round(n))<1e-9 else f"{round(n,3):g}"

REVEAL_FUNCS = ("head","kick","rise","pop","cellL","cellR")
LOOP_FUNCS   = ("breathe","floaty")

def transform_line(line, sid, new_start, new_dur, reveal):
    """Rewrite timeline numbers in one source line for scene `sid`."""
    old_start, _ = OLD[sid]
    def rel(orig_t):  # keep ambient/loops relative to scene start
        return new_start + (float(orig_t) - old_start)

    # helper reveal funcs: FUNC("#sel", T, ...)
    def repl_helper(m):
        fn, sel, ws, t = m.group(1), m.group(2), m.group(3), m.group(4)
        if fn in REVEAL_FUNCS and ("#"+sel.lstrip("#")) in reveal:
            nt = new_start + reveal["#"+sel.lstrip("#")]
        elif fn in LOOP_FUNCS:
            nt = rel(t)
        else:
            nt = rel(t)  # unmapped reveal -> keep relative position
        return f'{fn}("{sel}",{ws}{fmt(nt)}'
    line = re.sub(r'\b(scene|kick|head|rise|pop|cellL|cellR|breathe|floaty)\("([^"]+)",(\s*)([\d.]+)',
                  repl_helper, line)

    # wipe(T) -> scene start (boundary transition)
    line = re.sub(r'\bwipe\((\s*)([\d.]+)\)',
                  lambda m: f'wipe({m.group(1)}{fmt(new_start)})', line)

    # tl.fromTo / tl.to / tl.set ("#sel", ..., POS)
    def repl_tl(m):
        head, sel, mid, pos, tail = m.groups()
        is_loop = "repeat:" in m.group(0)
        key = "#" + sel.lstrip("#")
        if (not is_loop) and key in reveal:
            nt = new_start + reveal[key]
        else:
            nt = rel(pos)
        return f'{head}{sel}{mid}{fmt(nt)}{tail}'
    line = re.sub(r'(tl\.(?:fromTo|to|set)\(")([^"]+)(".*?,\s*)([\d.]+)(\)\s*;)',
                  repl_tl, line)
    return line

def transform_main(data):
    src = (EP/"composition.html").read_text()
    starts, durs = {}, {}
    cur = 0
    for sid in MAIN:
        durs[sid] = math.ceil(data[sid]["clip_dur"] + TAIL_PAD)
        starts[sid] = cur; cur += durs[sid]
    total = cur

    src = src.replace('data-composition-id="ep02full" data-start="0" data-duration="660"',
                      f'data-composition-id="ep02full" data-start="0" data-duration="{total}"')
    for sid in MAIN:
        os_, od_ = OLD[sid]
        src, n = re.subn(rf'(id="{sid}" data-start=)"{os_}"( data-duration=)"{od_}"',
                         rf'\g<1>"{starts[sid]}"\g<2>"{durs[sid]}"', src)
        assert n == 1, f"{sid} div {n}"

    smark = "// ===================== SCENES ====================="
    emark = '\n      window.__timelines["ep02full"] = tl;'
    si, ei = src.index(smark), src.index(emark)
    region = src[si:ei]
    blocks = re.split(r'(\n\s*// \d+\. )', region)
    rebuilt = blocks[0]; idx = 1; n = 0
    for sid in MAIN:
        sep, body = blocks[idx], blocks[idx+1]
        n += 1
        body = "\n".join(transform_line(l, sid, starts[sid], durs[sid], data[sid]["reveal"])
                         for l in body.split("\n"))
        body = re.sub(rf'scene\("#{sid}",\s*[\d.]+,\s*[\d.]+\)',
                      f'scene("#{sid}", {starts[sid]}, {durs[sid]})', body, count=1)
        rebuilt += sep + body
        idx += 2
    src = src[:si] + rebuilt + src[ei:]
    (EP/"composition_synced.html").write_text(src)
    print(f"  ✓ composition_synced.html  total={total}s")
    return starts, durs, total

def transform_outro(data):
    sid = "s16"
    clip = data[sid]["clip_dur"]
    new_dur = math.ceil(clip + 2.0)
    reveal = data[sid]["reveal"]
    src = (EP/"composition-outro.html").read_text()
    src = src.replace('data-composition-id="ep02outro" data-start="0" data-duration="30"',
                      f'data-composition-id="ep02outro" data-start="0" data-duration="{new_dur}"')
    src = src.replace('id="s16" data-start="0" data-duration="30"',
                      f'id="s16" data-start="0" data-duration="{new_dur}"')

    def repl_tl(m):
        head, sel, mid, pos, tail = m.groups()
        body = m.group(0)
        is_loop = "repeat:" in body
        key = "#" + sel.lstrip("#")
        if sel == "#s16" and "y:-20" in body:        # scene exit
            nt = new_dur - 1.5
        elif sel == "#s16" and "opacity" in body:    # scene fade-in
            nt = 0.3
        elif (not is_loop) and key in reveal:
            nt = reveal[key]
        else:
            nt = float(pos)                          # keep (loops, channel badge, wipe)
        return f'{head}{sel}{mid}{fmt(nt)}{tail}'
    src = re.sub(r'(tl\.(?:fromTo|to|set)\(")([^"]+)(".*?,\s*)([\d.]+)(\)\s*;)',
                 repl_tl, src)
    (EP/"composition-outro_synced.html").write_text(src)
    print(f"  ✓ composition-outro_synced.html  dur={new_dur}s")
    return new_dur

def build_audio(ids_starts, total, out):
    inputs = ["-f","lavfi","-t",str(total),"-i","anullsrc=r=44100:cl=stereo"]
    fp = ["[0:a]aformat=sample_rates=44100:channel_layouts=stereo[base]"]; mix=["[base]"]
    for i,(mp3,start) in enumerate(ids_starts):
        inputs += ["-i", mp3]; d = start*1000
        fp.append(f"[{i+1}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={d}|{d}[d{i}]")
        mix.append(f"[d{i}]")
    fp.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0[out]")
    subprocess.run(["ffmpeg","-y"]+inputs+["-filter_complex",";".join(fp),
                    "-map","[out]","-c:a","aac","-b:a","192k","-t",str(total),out],
                   check=True, capture_output=True)
    print(f"  ✓ {out}")

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Step 1: TTS (joyful) + alignment ...")
    dmain = process(MAIN)
    dout  = process(OUTRO)

    print("\nStep 2: re-time + word-sync compositions ...")
    starts, durs, total = transform_main(dmain)
    outro_dur = transform_outro(dout)

    print("\nStep 3: build audio tracks ...")
    build_audio([(dmain[s]["mp3"], starts[s]) for s in MAIN], total,
                str(CACHE/"main.aac"))
    build_audio([(dout["s16"]["mp3"], 0.5)], outro_dur, str(CACHE/"outro.aac"))

    print("\nScene map (start, dur, clip):")
    for s in MAIN:
        print(f"  {s:<4} start={starts[s]:>3} dur={durs[s]:>3} clip={dmain[s]['clip_dur']:.1f}")
    print(f"  TOTAL={total}s   outro={outro_dur}s")
