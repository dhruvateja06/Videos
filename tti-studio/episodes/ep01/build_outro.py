#!/usr/bin/env python3
"""
Build the Ep1 ~20s OUTRO: voiced + word-synced end card.
Generates Dhruva TTS, writes composition-outro.html timed to the read, and
builds audio_v2/outro.aac (voice + a soft chime). Render + mux per VOICEOVER.md.

    cd tti-studio/episodes/ep01
    export ELEVENLABS_API_KEY=...
    /opt/anaconda3/bin/python3 build_outro.py
"""
import base64, json, math, os, subprocess
from pathlib import Path
import requests

API   = os.environ["ELEVENLABS_API_KEY"]
VOICE = "7hshzsnMFQgQHNhu6yYM"
MODEL = "eleven_multilingual_v2"
VOICE_SETTINGS = {"stability": 0.40, "similarity_boost": 0.75,
                  "style": 0.50, "use_speaker_boost": True, "speed": 1.06}
EP    = Path(__file__).parent
CACHE = EP / "audio_v2"; CACHE.mkdir(exist_ok=True)
SFXD  = CACHE / "sfx"
OUT   = EP / "composition-outro.html"
COMP  = "sdep01outro"
LEAD, HEAD_BASE, STAGGER, TAIL = 0.25, 0.40, 0.40, 1.6

# ordered (text, [element ids revealed here])
BEATS = [
 ("If that made system design finally click, do me a favour and subscribe.", ["ok","ot"]),
 ("We're building this whole thing, one box at a time.", ["osub"]),
 ("Next up: how your phone actually finds the server, out of the entire internet. That's DNS and HTTP.", ["onext"]),
 ("See you in episode two.", ["oend"]),
]

def tts(text, name):
    mp3 = CACHE / f"{name}.mp3"; js = CACHE / f"{name}.align.json"
    if mp3.exists() and js.exists():
        return mp3, json.loads(js.read_text())
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
        headers={"xi-api-key": API, "Content-Type": "application/json"},
        json={"text": text, "model_id": MODEL, "voice_settings": VOICE_SETTINGS}, timeout=180)
    r.raise_for_status(); d = r.json()
    mp3.write_bytes(base64.b64decode(d["audio_base64"])); js.write_text(json.dumps(d["alignment"]))
    return mp3, d["alignment"]

def ffdur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1",str(p)], capture_output=True, text=True, check=True).stdout.strip())

def f(n):
    n = round(float(n), 3); return str(int(n)) if abs(n-round(n))<1e-9 else f"{n:g}"

def reveals(align):
    starts = align["character_start_times_seconds"]; t, idx, out = [], 0, {}
    for (txt,_) in BEATS:
        t.append(starts[min(idx,len(starts)-1)]); idx += len(txt)+1
    for k,(txt,sels) in enumerate(BEATS):
        base = HEAD_BASE if k==0 else max(t[k]-LEAD, HEAD_BASE)
        for j,sel in enumerate(sels): out[sel] = round(base+j*STAGGER,3)
    return out

HTML = """<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<script src="../../assets/vendor/gsap.min.js"></script>
<style>
@font-face{{font-family:"Fraunces";font-weight:600;src:url("../../assets/fonts/fraunces-latin-600-normal.woff2") format("woff2");}}
@font-face{{font-family:"Inter";font-weight:600;src:url("../../assets/fonts/inter-latin-600-normal.woff2") format("woff2");}}
@font-face{{font-family:"Inter";font-weight:700;src:url("../../assets/fonts/inter-latin-700-normal.woff2") format("woff2");}}
@font-face{{font-family:"JetBrains Mono";font-weight:400;src:url("../../assets/fonts/jetbrains-mono-latin-400-normal.woff2") format("woff2");}}
:root{{--paper:#0F1729;--panel:#16223C;--ink:#E6ECF5;--soft:#B7C2D6;--muted:#7B8AA5;--hair:rgba(123,138,165,.22);--accent:#3B7BFF;--accent-bright:#6AA0FF;--accent-soft:rgba(59,123,255,.14);}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1920px;height:1080px;overflow:hidden;}} body{{font-family:"Inter",sans-serif;background:var(--paper);}}
#root{{position:relative;width:1920px;height:1080px;background:var(--paper);color:var(--ink);}}
#bg{{position:absolute;inset:0;overflow:hidden;z-index:0;}}
#bggrid{{position:absolute;left:-140px;top:-140px;width:2300px;height:1400px;background-image:linear-gradient(rgba(123,138,165,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(123,138,165,.07) 1px,transparent 1px);background-size:72px 72px;}}
.glow{{position:absolute;border-radius:50%;filter:blur(70px);}}
#glow1{{width:900px;height:900px;left:980px;top:-260px;background:radial-gradient(circle,rgba(59,123,255,.20),rgba(59,123,255,0) 70%);}}
#glow2{{width:820px;height:820px;left:-300px;top:560px;background:radial-gradient(circle,rgba(106,160,255,.14),rgba(106,160,255,0) 70%);}}
.hud{{position:absolute;left:64px;right:64px;top:52px;display:flex;justify-content:space-between;align-items:center;z-index:7;font-family:"JetBrains Mono";font-size:22px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);}}
.hud .l span{{color:var(--accent);}}
#hudline{{position:absolute;left:64px;right:64px;top:94px;height:1px;background:var(--hair);z-index:7;transform-origin:left;}}
.bracket{{position:absolute;width:34px;height:34px;z-index:7;}}
#brTL{{left:30px;top:30px;border-left:2px solid var(--hair);border-top:2px solid var(--hair);}}
#brTR{{right:30px;top:30px;border-right:2px solid var(--hair);border-top:2px solid var(--hair);}}
#brBL{{left:30px;bottom:30px;border-left:2px solid var(--hair);border-bottom:2px solid var(--hair);}}
#brBR{{right:30px;bottom:30px;border-right:2px solid var(--hair);border-bottom:2px solid var(--hair);}}
.scene{{position:absolute;inset:0;z-index:2;padding:172px 130px 120px 130px;display:flex;flex-direction:column;justify-content:center;}}
.kick{{font-family:"JetBrains Mono";font-size:27px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);margin-bottom:26px;}}
.kick:before{{content:"// ";color:var(--muted);}}
h1{{font-family:"Fraunces";font-weight:600;color:var(--ink);line-height:1.04;letter-spacing:-.012em;font-size:104px;max-width:1300px;}}
.ac{{color:var(--accent);}}
.osub{{font-family:"JetBrains Mono";font-size:30px;letter-spacing:.12em;color:var(--soft);margin-top:34px;opacity:0;}}
.onext{{margin-top:44px;background:var(--accent-soft);border:1px solid rgba(59,123,255,.45);border-radius:18px;padding:30px 38px;opacity:0;align-self:flex-start;}}
.onext .nm{{font-family:"JetBrains Mono";font-size:24px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);}}
.onext .hd{{font-family:"Fraunces";font-weight:600;font-size:48px;color:#fff;margin-top:10px;}}
.oend{{font-family:"Fraunces";font-style:italic;font-size:44px;color:var(--soft);margin-top:46px;opacity:0;}}
.oend .ac{{font-style:normal;}}
</style></head>
<body>
<div id="root" data-composition-id="{comp}" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
  <div id="bg"><div id="bggrid"></div><div class="glow" id="glow1"></div><div class="glow" id="glow2"></div></div>
  <div class="hud"><div class="l">THE TECH INTERN <span>// SYSTEM DESIGN</span></div><div class="r">S1 · E01</div></div>
  <div id="hudline"></div>
  <div class="bracket" id="brTL"></div><div class="bracket" id="brTR"></div><div class="bracket" id="brBL"></div><div class="bracket" id="brBR"></div>
  <div class="scene clip" id="o" data-start="0" data-duration="{total}" data-track-index="0">
    <div class="kick" id="ok">that's a wrap</div>
    <h1 id="ot">Subscribe — we build it <span class="ac">one box at a time.</span></h1>
    <div class="osub" id="osub">THE TECH INTERN &nbsp;//&nbsp; SYSTEM DESIGN, FROM DAY ONE</div>
    <div class="onext" id="onext"><div class="nm">Next &middot; Episode 02</div><div class="hd">How your phone finds the server &mdash; DNS &amp; HTTP</div></div>
    <div class="oend" id="oend">See you in <span class="ac">episode two.</span></div>
  </div>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
tl.from("#hudline", {{ scaleX:0, duration:1.0, ease:"power2.out" }}, 0);
tl.fromTo(".hud", {{ opacity:0 }}, {{ opacity:1, duration:1.0 }}, 0.2);
tl.fromTo(".bracket", {{ opacity:0 }}, {{ opacity:1, duration:1.2, stagger:0.1 }}, 0.3);
tl.to("#bggrid", {{ x:-72, y:-50, duration:60, ease:"sine.inOut", repeat:2, yoyo:true }}, 0);
tl.to("#glow1", {{ x:-160, y:120, scale:1.2, duration:40, ease:"sine.inOut", repeat:2, yoyo:true }}, 0);
tl.to("#glow2", {{ x:140, y:-110, scale:1.2, duration:46, ease:"sine.inOut", repeat:2, yoyo:true }}, 0);
function head(sel,t,d){{ tl.fromTo(sel,{{opacity:0,y:60,scale:0.95}},{{opacity:1,y:0,scale:1,duration:(d||0.9),ease:"back.out(1.25)"}},t); }}
function kick(sel,t){{ tl.fromTo(sel,{{opacity:0,x:-26}},{{opacity:1,x:0,duration:0.6,ease:"power2.out"}},t); }}
function rise(sel,t,dy,d){{ tl.fromTo(sel,{{opacity:0,y:(dy==null?24:dy)}},{{opacity:1,y:0,duration:(d||0.6),ease:"power3.out"}},t); }}
function pop(sel,t,d){{ tl.fromTo(sel,{{opacity:0,y:24,scale:0.9}},{{opacity:1,y:0,scale:1,duration:(d||0.55),ease:"back.out(1.5)",transformOrigin:"center"}},t); }}
function breathe(sel,t,to,dur,n){{ tl.to(sel,{{scale:to,duration:dur,ease:"sine.inOut",repeat:n,yoyo:true,transformOrigin:"center"}},t); }}
{timeline}
window.__timelines["{comp}"] = tl;
</script></body></html>
"""

def main():
    mp3, al = tts(" ".join(b[0] for b in BEATS), "outro")
    clip = ffdur(mp3); total = math.ceil(clip + TAIL)
    R = reveals(al)
    def r(sel): return R.get(sel, HEAD_BASE)
    tlines = [
      f'kick("#ok", {f(r("ok"))}); head("#ot", {f(r("ot"))}, 1.0);',
      f'tl.to("#ot .ac", {{ opacity:0.72, duration:1.5, ease:"sine.inOut", repeat:3, yoyo:true }}, {f(r("ot")+2.5)});',
      f'rise("#osub", {f(r("osub"))}, 16);',
      f'pop("#onext", {f(r("onext"))}, 0.7); breathe("#onext", {f(r("onext")+1.6)}, 1.02, 2.4, 3);',
      f'rise("#oend", {f(r("oend"))}, 18);',
    ]
    timeline = "\n".join("      " + ln for ln in tlines)
    OUT.write_text(HTML.format(comp=COMP, total=total, timeline=timeline))
    print(f"  ✓ {OUT.name}  total={total}s (clip {clip:.1f})")

    # audio: voice + a soft chime at the EP02 reveal
    chime = SFXD / "chime.mp3"
    inputs = ["-f","lavfi","-t",str(total),"-i","anullsrc=r=44100:cl=stereo",
              "-i", str(mp3)]
    fp = ["[0:a]aformat=sample_rates=44100:channel_layouts=stereo[base]",
          "[1:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay=0|0[v]"]
    mix = ["[base]","[v]"]
    if chime.exists():
        inputs += ["-i", str(chime)]
        ms = int(round(r("onext")*1000))
        fp.append(f"[2:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=0.20,adelay={ms}|{ms}[c]")
        mix.append("[c]")
    fp.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0[out]")
    out = str(CACHE / "outro.aac")
    subprocess.run(["ffmpeg","-y"]+inputs+["-filter_complex",";".join(fp),
                   "-map","[out]","-c:a","aac","-b:a","192k","-t",str(total),out],
                   check=True, capture_output=True)
    print(f"  ✓ {out}")

if __name__ == "__main__":
    main()
