#!/usr/bin/env python3
"""
Word-synced, joyful Dhruva voiceover + ElevenLabs SFX build for Ep4 LONG-FORM
(15 scenes). See docs/VOICEOVER.md and docs/SFX.md.

  cd tti-studio/episodes/ep04
  export ELEVENLABS_API_KEY="...(text_to_speech + sound-generation)..."
  /opt/anaconda3/bin/python3 sync_build.py
Then render composition_synced.html and mux audio_v2/main.aac.
"""
import base64, json, math, os, re, subprocess
from pathlib import Path
import requests

API   = os.environ["ELEVENLABS_API_KEY"]
VOICE = "7hshzsnMFQgQHNhu6yYM"
MODEL = "eleven_multilingual_v2"
VOICE_SETTINGS = {"stability": 0.30, "similarity_boost": 0.75,
                  "style": 0.65, "use_speaker_boost": True, "speed": 1.02}
EP    = Path(__file__).parent
CACHE = EP / "audio_v2"; CACHE.mkdir(exist_ok=True)
SFXD  = CACHE / "sfx"; SFXD.mkdir(exist_ok=True)
SRC_HTML = EP / "composition.html"
OUT_HTML = EP / "composition_synced.html"
COMP_ID  = "sdep04full"
LEAD, HEAD_BASE, STAGGER, TAIL_PAD = 0.25, 0.40, 0.40, 1.50

SCENES = [f"s{i}" for i in range(1, 16)]
OLD = {"s1":(0,35),"s2":(35,28),"s3":(63,32),"s4":(95,45),"s5":(140,42),
 "s6":(182,35),"s7":(217,50),"s8":(267,42),"s9":(309,38),"s10":(347,42),
 "s11":(389,38),"s12":(427,48),"s13":(475,35),"s14":(510,30),"s15":(540,30)}
HEAD_DUR = {"s1":1.0}

BEATS = {
 "s1":[
  ("Somewhere in Bangalore, a Swiggy engineer is staring at a dashboard.", ["s1k","s1t"]),
  ("Numbers are scrolling past — twelve thousand something, forty-five milliseconds, eight-twenty milliseconds, ninety-nine point nine nine percent.", ["s1-frame"]),
  ("To you and me, that's noise. To this engineer, it's the entire health of the system, at a glance.", ["s1-blocks"]),
  ("So what do these numbers actually mean, and how does one glance tell you if everything's fine, or about to fall over?", ["s1-person","s1sub"]),
 ],
 "s2":[
  ("Here's the trap: a single number, with no vocabulary around it, doesn't tell you anything.", ["s2k","s2t"]),
  ("\"820\" — is that good? Bad? Milliseconds? Requests? You can't tell.", ["s2-num"]),
  ("The vocabulary is what turns a number into a diagnosis. That's what this episode gives you.", ["s2-q","s2sub"]),
 ],
 "s3":[
  ("You already met two of these numbers last episode, so this is just a reminder, not a re-teach.", ["s3k","s3t"]),
  ("qps: how many requests the system handles every second.", ["s3-qps"]),
  ("p50 and p99: how long a request takes, for the typical user and for the unlucky one-in-a-hundred.", ["s3-p"]),
  ("Today we go one level deeper on both, and we add a third number that neither of them tells you.", ["s3sub"]),
 ],
 "s4":[
  ("First correction: \"a lakh people opened the app\" and \"the server is handling a lakh requests a second\" are not the same sentence.", ["s4k","s4t"]),
  ("A hundred thousand people can have Swiggy open right now.", ["s4-grid","s4-label1"]),
  ("But most of them are just staring at the menu, deciding between biryani and butter chicken. They're not hitting the server every second, they're idle, most of the time.", []),
  ("Only the ones actually tapping, searching, ordering, refreshing, generate real requests. That gap between \"people online\" and \"requests per second\" is called think time.", ["s4-dim","s4-server"]),
  ("So a hundred thousand concurrent users might only produce two thousand qps. Confusing the two is how people wildly overestimate, or underestimate, what a server actually needs to handle.", ["s4-conv","s4sub"]),
 ],
 "s5":[
  ("Second new idea: it's not enough to know your qps. What matters is how close you are to the edge.", ["s5k","s5t"]),
  ("If your system can handle ten thousand qps and you're sitting at two thousand, you have headroom, plenty of room before anything breaks.", ["s5-arc-green"]),
  ("At seventy-five hundred, you're getting close. Response times start creeping up even before you hit the ceiling.", ["s5-arc-amber"]),
  ("Cross the ceiling, and it's not a graceful slowdown, queues start forming, and things that used to take milliseconds start taking seconds.", ["s5-arc-red","s5sub"]),
 ],
 "s6":[
  ("Now the third number, the one from the cliffhanger. Engineers promise reliability using something called \"nines.\"", ["s6k","s6t"]),
  ("Ninety-nine percent uptime. Ninety-nine point nine. Ninety-nine point nine nine. Ninety-nine point nine nine nine.", ["s6-r1","s6-r2","s6-r3","s6-r4"]),
  ("Every extra nine sounds like a rounding error. It is absolutely not one, and here's why.", ["s6sub"]),
 ],
 "s7":[
  ("Let's translate percentages into something you can actually feel: minutes and hours a year.", ["s7k","s7t"]),
  ("Ninety-nine percent uptime sounds great, until you realize it allows three point six five days of downtime a year. That's a whole long weekend of \"the app is down,\" spread across the calendar.", ["s7-row1"]),
  ("Add one nine, ninety-nine point nine percent, and that shrinks to eight point seven six hours a year. Better, but still an entire workday of outages.", ["s7-row2"]),
  ("Add another nine and you're down to fifty-two minutes a year, total.", ["s7-row3"]),
  ("One more nine, and you're at five minutes a year. Five minutes, across the entire year, for every outage combined.", ["s7-row4"]),
  ("Each nine you add is roughly a ten-times reduction in allowed downtime.", ["s7sub"]),
 ],
 "s8":[
  ("Here's why this isn't just a trivia stat, because some systems literally cannot tolerate the outage a \"lower\" nine allows.", ["s8k","s8t"]),
  ("Every UPI payment in India, from paying an auto driver to a business settling lakhs, runs through this rail.", ["s8-flow"]),
  ("NPCI, the body that runs UPI, mandates ninety-nine point nine nine percent uptime for banks on the network. Not ninety-nine percent, that extra two nines is the difference between \"rare glitch\" and \"money stuck mid-transfer during peak hours, at scale.\"", ["s8-badge"]),
  ("Three point six five days of a payment rail being unreliable would be a national story. Fifty-two minutes a year is survivable. That gap is exactly why the nines matter here, they're a design requirement, not a stat you round off.", ["s8sub"]),
 ],
 "s9":[
  ("So why doesn't everyone just build for five nines? Because each extra nine gets brutally more expensive.", ["s9k","s9t"]),
  ("Going from ninety-nine to ninety-nine point nine might mean better monitoring and a faster on-call process. Going from ninety-nine point nine nine to five nines can mean an entire second data centre, standing by, just for the days everything else fails at once.", ["s9-curve"]),
  ("The reliability curve is steep at the top. Chasing the last nine is often the most expensive engineering work a company ever does.", ["s9-label","s9sub"]),
 ],
 "s10":[
  ("One more piece of vocabulary, because you'll hear these three constantly: SLA, SLO, and SLI.", ["s10k","s10t"]),
  ("SLA, service level agreement. The promise made externally, often with a penalty attached if it's broken.", ["s10-sla"]),
  ("SLO, service level objective. The internal bar the engineering team actually aims for, usually stricter than the SLA, so there's a safety margin.", ["s10-slo"]),
  ("SLI, service level indicator. The real number being measured right now, that tells you whether you're meeting the SLO.", ["s10-sli"]),
  ("The SLI is reality. The SLO is the internal goal. The SLA is what you promised the world.", ["s10sub"]),
 ],
 "s11":[
  ("Let's go back to that dashboard from the start of the episode, except now you can actually read it.", ["s11k","s11t"]),
  ("Twelve thousand qps, that's the load, and you now know to check it against the ceiling for headroom.", ["s11-qps"]),
  ("Forty-five milliseconds typical, eight-twenty for the unlucky one percent, that's the felt experience.", ["s11-lat"]),
  ("Ninety-nine point nine nine percent, that's the promise being kept, or broken.", ["s11-nines"]),
  ("Three numbers. Five seconds. The entire health of the system.", ["s11sub"]),
 ],
 "s12":[
  ("Let's put it to work. Same 8pm Swiggy rush from last episode, but now watch the numbers, not just the chaos.", ["s12k","s12t"]),
  ("qps climbs toward the ceiling, headroom is disappearing.", ["s12-qps"]),
  ("p99 latency, which was already the \"unlucky\" number, spikes hard, now even more people are having a bad time.", ["s12-p99"]),
  ("And because this outage is dragging on, the month's uptime number is dropping in real time, eating into the whole year's downtime budget in one evening.", ["s12-nines"]),
  ("An engineer watching this doesn't need to guess. The vocabulary tells them exactly what's happening and how bad it is, instantly.", ["s12-oncall","s12sub"]),
 ],
 "s13":[
  ("Here's the trade-off this episode lands on: more nines isn't free, and it isn't always worth it.", ["s13k","s13t"]),
  ("An internal analytics dashboard breaking for twenty minutes a month is annoying, not a crisis.", ["s13-left"]),
  ("A payment system breaking for the same twenty minutes is a headline. The right number of nines depends entirely on what breaks if you don't have them.", ["s13-right","s13sub"]),
 ],
 "s14":[
  ("Three numbers, one vocabulary.", ["s14k","s14t"]),
  ("qps: how much load the system is under, right now.", ["s14-qps"]),
  ("p50 and p99: how the request feels, for the typical user, and for the unlucky one.", ["s14-p"]),
  ("And nines: the promise being kept, measured in minutes of downtime a year.", ["s14-nines"]),
 ],
 "s15":[
  ("But here's the thing, knowing these numbers doesn't fix anything by itself. They just tell you that something's wrong.", ["s15k","s15t"]),
  ("So what do you actually do when the numbers say you're out of room?", ["s15-alert"]),
  ("Next episode: the load balancer, the waiter who decides which kitchen gets your order, so that no single cook ever gets buried.", ["s15-fork","s15sub"]),
 ],
}

# ---------------------------------------------------------------------------
def _post_tts(text):
    return requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
        headers={"xi-api-key": API, "Content-Type": "application/json"},
        json={"text": text, "model_id": MODEL, "voice_settings": VOICE_SETTINGS}, timeout=180)

def tts(text, name):
    mp3 = CACHE / f"{name}.mp3"; js = CACHE / f"{name}.align.json"
    if mp3.exists() and js.exists():
        return mp3, json.loads(js.read_text())
    print(f"  [tts] {name} ...")
    r = _post_tts(text)
    if r.status_code == 422 and "speed" in VOICE_SETTINGS:
        VOICE_SETTINGS.pop("speed"); r = _post_tts(text)
    r.raise_for_status(); d = r.json()
    mp3.write_bytes(base64.b64decode(d["audio_base64"])); js.write_text(json.dumps(d["alignment"]))
    return mp3, d["alignment"]

def sfx(prompt, name, duration):
    mp3 = SFXD / f"{name}.mp3"
    if mp3.exists(): return mp3
    print(f"  [sfx] {name} ...")
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation",
        headers={"xi-api-key": API, "Content-Type": "application/json"},
        json={"text": prompt, "duration_seconds": duration, "prompt_influence": 0.45}, timeout=180)
    r.raise_for_status(); mp3.write_bytes(r.content); return mp3

# 5-sound palette per docs/SFX.md: whoosh / zip / chime / riser / swell
SFX_KIT = {
 "whoosh": ("short subtle clean UI transition whoosh, soft quick swoosh, no music", 0.8, 0.16),
 "zip":    ("short soft digital data blip, quick electronic UI tick zip, subtle, no music", 0.7, 0.18),
 "chime":  ("soft positive confirmation chime, gentle success ding, warm short, no music", 0.9, 0.20),
 "riser":  ("rising tension synth swell, building pressure riser, subtle escalating whoosh, no drums, no music", 2.2, 0.14),
 "swell":  ("warm sustained ambient pad swell, soft resolution tone, gentle synth bloom, no drums, no music", 2.5, 0.12),
}

def ffdur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1",str(p)], capture_output=True, text=True, check=True).stdout.strip())

def beat_times(beats, al):
    cs = al["character_start_times_seconds"]; t, idx = [], 0
    for (txt,_) in beats:
        t.append(cs[min(idx,len(cs)-1)]); idx += len(txt)+1
    return t

def compute_reveals(beats, al):
    bt = beat_times(beats, al); rev = {}
    for k,(txt,sels) in enumerate(beats):
        base = HEAD_BASE if k==0 else max(bt[k]-LEAD, HEAD_BASE)
        for j,sel in enumerate(sels): rev[sel] = round(base + j*STAGGER, 3)
    return rev

def process():
    out = {}
    for sid in SCENES:
        text = " ".join(b[0] for b in BEATS[sid])
        mp3, al = tts(text, sid)
        out[sid] = {"reveal": compute_reveals(BEATS[sid], al), "clip_dur": ffdur(mp3)}
    return out

# ---------------------------------------------------------------------------
def f(n):
    n = round(float(n),3); return str(int(n)) if abs(n-round(n))<1e-9 else f"{n:g}"

def build_timeline(starts, durs, data):
    def R(sid, sel, fb=None):
        off = data[sid]["reveal"].get(sel)
        if off is None: off = fb if fb is not None else HEAD_BASE
        return starts[sid] + off
    L = ["      // === word-synced to Dhruva VO (generated by sync_build.py) ==="]
    def emit(s): L.append("      "+s)
    for sid in SCENES:
        s, d = starts[sid], durs[sid]; hd = HEAD_DUR.get(sid,0.9)
        L.append(f"\n      // {sid.upper()} ({s}-{s+d})")
        if sid != "s1": emit(f'sweep({f(s)});')
        emit(f'scene("#{sid}", {f(s)}, {f(d)});')
        emit(f'kick("#{sid}k", {f(R(sid,sid+"k"))}); head("#{sid}t", {f(R(sid,sid+"t"))}, {hd});')

        if sid=="s1":
            emit(f'pop("#s1-frame", {f(R("s1","s1-frame"))}, 0.6);')
            t1 = R("s1","s1-blocks")
            emit(f'tl.fromTo("#s1-blocks rect",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,stagger:0.25,duration:0.4,ease:"back.out(1.5)"}}, {f(t1)});')
            emit(f'tl.fromTo("#s1-blocks text",{{opacity:0}},{{opacity:1,stagger:0.25,duration:0.4}}, {f(t1+0.1)});')
            emit(f'pop("#s1-person", {f(R("s1","s1-person"))}, 0.6); breathe("#s1-blocks", {f(R("s1","s1-person")+3)}, 1.02, 1.6, 5);')
            emit(f'rise("#s1sub", {f(R("s1","s1sub"))}, 18);')
        elif sid=="s2":
            emit(f'pop("#s2-num", {f(R("s2","s2-num"))}, 0.6);')
            emit(f'fade("#s2-q", {f(R("s2","s2-q"))}, 0.6);')
            emit(f'rise("#s2sub", {f(R("s2","s2sub"))}, 18);')
        elif sid=="s3":
            emit(f'slideL("#s3-qps", {f(R("s3","s3-qps"))}, 0.6); slideR("#s3-p", {f(R("s3","s3-p"))}, 0.6);')
            emit(f'rise("#s3sub", {f(R("s3","s3sub"))}, 18);')
        elif sid=="s4":
            t4 = R("s4","s4-grid")
            emit(f'tl.fromTo(".s4dot",{{opacity:0,scale:0}},{{opacity:1,scale:1,stagger:0.006,duration:0.3,ease:"back.out(1.4)"}}, {f(t4)});')
            emit(f'fade("#s4-label1", {f(R("s4","s4-label1"))}, 0.5);')
            t4d = R("s4","s4-dim", fb=data["s4"]["reveal"].get("s4-server"))
            emit(f'tl.to(".s4dot",{{opacity:0.2,duration:0.4}}, {f(max(t4d-1,t4+2))});')
            active = [3,17,44,58,71,85,99,102]
            for i,idx in enumerate(active):
                emit(f'tl.to("#s4-dot{idx}",{{opacity:1,scale:1.3,duration:0.3,ease:"back.out(2)"}}, {f(max(t4d-1,t4+2)+3+idx*0.25)});')
            emit(f'pop("#s4-server", {f(R("s4","s4-server"))}, 0.6);')
            t4c = R("s4","s4-conv")
            emit(f'tl.fromTo("#s4-conv",{{opacity:0}},{{opacity:1,duration:0.6}}, {f(t4c)});')
            emit(f'rise("#s4sub", {f(R("s4","s4sub"))}, 18);')
        elif sid=="s5":
            tg = R("s5","s5-arc-green")
            emit(f'tl.to("#s5-arc-green",{{opacity:1,duration:0.5}}, {f(tg)});')
            emit(f'tl.to("#s5-needle",{{rotation:0,svgOrigin:"500 380",duration:0.6,ease:"power2.out"}}, {f(tg)});')
            ta = R("s5","s5-arc-amber")
            emit(f'tl.to("#s5-arc-amber",{{opacity:1,duration:0.5}}, {f(ta)});')
            emit(f'tl.to("#s5-needle",{{rotation:55,svgOrigin:"500 380",duration:0.8,ease:"power2.inOut"}}, {f(ta)});')
            emit(f'tl.call(()=>{{ document.getElementById("s5-readout").textContent = "7,500 / 10,000 qps"; }},null,{f(ta+0.4)});')
            tr = R("s5","s5-arc-red")
            emit(f'tl.to("#s5-arc-red",{{opacity:1,duration:0.5}}, {f(tr)});')
            emit(f'tl.to("#s5-needle",{{rotation:82,svgOrigin:"500 380",duration:0.8,ease:"power2.inOut"}}, {f(tr)});')
            emit(f'tl.call(()=>{{ document.getElementById("s5-readout").textContent = "10,200 / 10,000 qps"; }},null,{f(tr+0.4)});')
            emit(f'rise("#s5sub", {f(R("s5","s5sub"))}, 18);')
        elif sid=="s6":
            emit(f'rise("#s6-r1", {f(R("s6","s6-r1"))}, 20); rise("#s6-r2", {f(R("s6","s6-r2"))}, 20); rise("#s6-r3", {f(R("s6","s6-r3"))}, 20); rise("#s6-r4", {f(R("s6","s6-r4"))}, 20);')
            emit(f'rise("#s6sub", {f(R("s6","s6sub"))}, 18);')
        elif sid=="s7":
            emit(f'rise("#s7-row1", {f(R("s7","s7-row1"))}, 20); rise("#s7-row2", {f(R("s7","s7-row2"))}, 20); rise("#s7-row3", {f(R("s7","s7-row3"))}, 20);')
            t7 = R("s7","s7-row4")
            emit(f'pop("#s7-row4", {f(t7)}, 0.6); breathe("#s7-row4", {f(t7+3)}, 1.02, 1.6, 4);')
            emit(f'rise("#s7sub", {f(R("s7","s7sub"))}, 18);')
        elif sid=="s8":
            t8 = R("s8","s8-flow")
            emit(f'fade("#s8-flow", {f(t8)}, 0.6);')
            emit(f'fade("#s8-e1", {f(t8+1)}, 0.4); fade("#s8-e2", {f(t8+1.3)}, 0.4); fade("#s8-e3", {f(t8+1.6)}, 0.4);')
            emit(f'tl.set("#s8-coin",{{opacity:1}}, {f(t8+3)});')
            emit(f'tl.to("#s8-coin",{{attr:{{cx:610}},duration:0.7,ease:"power1.inOut"}}, {f(t8+3)});')
            emit(f'tl.to("#s8-coin",{{attr:{{cx:1110}},duration:0.7,ease:"power1.inOut"}}, {f(t8+4)});')
            emit(f'pop("#s8-badge", {f(R("s8","s8-badge"))}, 0.6);')
            emit(f'rise("#s8sub", {f(R("s8","s8sub"))}, 18);')
        elif sid=="s9":
            emit(f'tl.to("#s9-curve",{{opacity:1,duration:1.0,ease:"power2.out"}}, {f(R("s9","s9-curve"))});')
            emit(f'fade("#s9-label", {f(R("s9","s9-label"))}, 0.6);')
            emit(f'rise("#s9sub", {f(R("s9","s9sub"))}, 18);')
        elif sid=="s10":
            emit(f'pop("#s10-sla", {f(R("s10","s10-sla"))}, 0.6); pop("#s10-slo", {f(R("s10","s10-slo"))}, 0.6); pop("#s10-sli", {f(R("s10","s10-sli"))}, 0.6);')
            emit(f'rise("#s10sub", {f(R("s10","s10sub"))}, 18);')
        elif sid=="s11":
            emit(f'pop("#s11-qps", {f(R("s11","s11-qps"))}, 0.6); pop("#s11-lat", {f(R("s11","s11-lat"))}, 0.6); pop("#s11-nines", {f(R("s11","s11-nines"))}, 0.6);')
            tn = R("s11","s11-nines")
            emit(f'breathe("#s11-qps", {f(tn+2)}, 1.03, 1.2, 2); breathe("#s11-lat", {f(tn+2)}, 1.03, 1.2, 2); breathe("#s11-nines", {f(tn+2)}, 1.03, 1.2, 2);')
            emit(f'rise("#s11sub", {f(R("s11","s11sub"))}, 18);')
        elif sid=="s12":
            emit(f'pop("#s12-qps", {f(R("s12","s12-qps"))}, 0.6);')
            emit(f'pop("#s12-p99", {f(R("s12","s12-p99"))}, 0.6);')
            emit(f'pop("#s12-nines", {f(R("s12","s12-nines"))}, 0.6);')
            emit(f'pop("#s12-oncall", {f(R("s12","s12-oncall"))}, 0.6);')
            emit(f'rise("#s12sub", {f(R("s12","s12sub"))}, 18);')
        elif sid=="s13":
            emit(f'slideL("#s13-left", {f(R("s13","s13-left"))}, 0.7); slideR("#s13-right", {f(R("s13","s13-right"))}, 0.7);')
            emit(f'rise("#s13sub", {f(R("s13","s13sub"))}, 18);')
        elif sid=="s14":
            emit(f'pop("#s14-qps", {f(R("s14","s14-qps"))}, 0.6); pop("#s14-p", {f(R("s14","s14-p"))}, 0.6); pop("#s14-nines", {f(R("s14","s14-nines"))}, 0.6);')
        elif sid=="s15":
            t15 = R("s15","s15-alert")
            emit(f'pop("#s15-alert", {f(t15)}, 0.6); breathe("#s15-alert", {f(t15+2)}, 1.01, 1.2, 4);')
            emit(f'fade("#s15-fork", {f(R("s15","s15-fork"))}, 0.7);')
            emit(f'rise("#s15sub", {f(R("s15","s15sub"))}, 18);')
    return "\n".join(L) + "\n"

def sfx_cues(starts, data):
    def R(sid,sel): return starts[sid] + data[sid]["reveal"].get(sel, HEAD_BASE)
    g = {k:v[2] for k,v in SFX_KIT.items()}
    cues = [("whoosh", max(starts[sid]-0.2,0), g["whoosh"]) for sid in SCENES[1:]]
    # s1: whoosh on dashboard frame, zip x3 on number blocks, riser under final line
    cues.append(("whoosh", R("s1","s1-frame"), g["whoosh"]))
    t1b = R("s1","s1-blocks")
    cues += [("zip", t1b+i*0.3, g["zip"]) for i in range(3)]
    cues.append(("riser", R("s1","s1-person"), g["riser"]))
    # s2: zip on bare number
    cues.append(("zip", R("s2","s2-num"), g["zip"]))
    # s3: zip on each card
    cues.append(("zip", R("s3","s3-qps"), g["zip"])); cues.append(("zip", R("s3","s3-p"), g["zip"]))
    # s4: zip on users grid, zip x4 on active packets, chime on conv label
    cues.append(("zip", R("s4","s4-grid"), g["zip"]))
    t4d = starts["s4"] + data["s4"]["reveal"].get("s4-dim", data["s4"]["reveal"].get("s4-server", HEAD_BASE))
    cues += [("zip", t4d+2+i*0.25, g["zip"]) for i in range(4)]
    cues.append(("chime", R("s4","s4-conv"), g["chime"]))
    # s5: zip on gauge, riser green->amber, chime(sharp) into red
    cues.append(("zip", R("s5","s5-arc-green"), g["zip"]))
    cues.append(("riser", R("s5","s5-arc-amber"), g["riser"]))
    cues.append(("chime", R("s5","s5-arc-red"), g["chime"]))
    # s6: zip on each rung
    for sel in ["s6-r1","s6-r2","s6-r3","s6-r4"]: cues.append(("zip", R("s6",sel), g["zip"]))
    # s7: zip on rows 1-3, chime on row4, swell under glow
    for sel in ["s7-row1","s7-row2","s7-row3"]: cues.append(("zip", R("s7",sel), g["zip"]))
    cues.append(("chime", R("s7","s7-row4"), g["chime"]))
    cues.append(("swell", R("s7","s7-row4")+3, g["swell"]))
    # s8: zip on coin hops, chime on badge
    t8 = R("s8","s8-flow")
    cues.append(("zip", t8+3, g["zip"])); cues.append(("zip", t8+4, g["zip"]))
    cues.append(("chime", R("s8","s8-badge"), g["chime"]))
    # s9: zip on curve, chime on label
    cues.append(("zip", R("s9","s9-curve"), g["zip"]))
    cues.append(("chime", R("s9","s9-label"), g["chime"]))
    # s10: zip on each card, chime on nesting (sub line)
    for sel in ["s10-sla","s10-slo","s10-sli"]: cues.append(("zip", R("s10",sel), g["zip"]))
    cues.append(("chime", R("s10","s10sub"), g["chime"]))
    # s11: zip on each highlight, chime on makes-sense moment
    for sel in ["s11-qps","s11-lat","s11-nines"]: cues.append(("zip", R("s11",sel), g["zip"]))
    cues.append(("chime", R("s11","s11-nines")+2, g["chime"]))
    # s12: riser under qps climb, zip on p99 spike, chime(alarmed) on nines flicker
    cues.append(("riser", R("s12","s12-qps"), g["riser"]))
    cues.append(("zip", R("s12","s12-p99"), g["zip"]))
    cues.append(("chime", R("s12","s12-nines"), g["chime"]))
    # s13: zip on each panel, chime on payment-rail
    cues.append(("zip", R("s13","s13-left"), g["zip"])); cues.append(("zip", R("s13","s13-right"), g["zip"]))
    cues.append(("chime", R("s13","s13-right")+1, g["chime"]))
    # s14: zip on each recap card, swell under settle
    for sel in ["s14-qps","s14-p","s14-nines"]: cues.append(("zip", R("s14",sel), g["zip"]))
    cues.append(("swell", R("s14","s14-nines")+1, g["swell"]))
    # s15: whoosh on flatline, riser under fork (deliberately unresolved)
    cues.append(("whoosh", R("s15","s15-alert"), g["whoosh"]))
    cues.append(("riser", R("s15","s15-fork"), g["riser"]))
    return cues

def _ts(t):
    h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int(round((t-int(t))*1000))
    if ms==1000: ms=0; s+=1
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def build_srt(starts, out):
    idx, lines = 1, []
    for sid in SCENES:
        al = json.loads((CACHE/f"{sid}.align.json").read_text())
        chars = al["characters"]; cs = al["character_start_times_seconds"]; ce = al["character_end_times_seconds"]
        text = "".join(chars); base = starts[sid]
        for m in re.finditer(r'[^.?!]+[.?!]+|\S[^.?!]*$', text):
            si, ei = m.start(), m.end()-1
            while si < ei and text[si]==' ': si+=1
            seg = text[si:ei+1].strip()
            if not seg: continue
            st = base+cs[min(si,len(cs)-1)]; en = base+ce[min(ei,len(ce)-1)]
            lines += [str(idx), f"{_ts(st)} --> {_ts(en)}", seg, ""]; idx+=1
    Path(out).write_text("\n".join(lines)); print(f"  ✓ {out}  ({idx-1} cues)")

def transform(data):
    src = SRC_HTML.read_text()
    starts, durs, cur = {}, {}, 0
    for sid in SCENES:
        durs[sid] = math.ceil(data[sid]["clip_dur"] + TAIL_PAD); starts[sid] = cur; cur += durs[sid]
    total = cur
    src, n = re.subn(rf'(data-composition-id="{COMP_ID}" data-start="0" data-duration=)"\d+"', rf'\g<1>"{total}"', src)
    assert n==1, f"root dur n={n}"
    for sid in SCENES:
        os_, od_ = OLD[sid]
        src, n = re.subn(rf'(id="{sid}"[^>]*?data-start=)"{os_}"( data-duration=)"{od_}"', rf'\g<1>"{starts[sid]}"\g<2>"{durs[sid]}"', src)
        assert n==1, f"{sid} div n={n}"
    a = "      // 1: The dashboard nobody can read (0-35)"
    b = '      window.__timelines["sdep04full"] = tl;'
    si = src.index(a); ei = src.index(b)
    src = src[:si] + build_timeline(starts, durs, data) + "\n" + src[ei:]
    OUT_HTML.write_text(src); print(f"  ✓ {OUT_HTML.name}  total={total}s"); return starts, durs, total

def build_audio(starts, total, data, out):
    inputs = ["-f","lavfi","-t",str(total),"-i","anullsrc=r=44100:cl=stereo"]
    fp = ["[0:a]aformat=sample_rates=44100:channel_layouts=stereo[base]"]; mix=["[base]"]; idx=1
    for sid in SCENES:
        inputs += ["-i", str(CACHE/f"{sid}.mp3")]; ms = starts[sid]*1000
        fp.append(f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={ms}|{ms}[v{idx}]"); mix.append(f"[v{idx}]"); idx+=1
    for name,t,gain in sfx_cues(starts, data):
        inputs += ["-i", str(SFXD/f"{name}.mp3")]; ms=int(round(t*1000))
        fp.append(f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={gain},adelay={ms}|{ms}[x{idx}]"); mix.append(f"[x{idx}]"); idx+=1
    fp.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0[out]")
    subprocess.run(["ffmpeg","-y"]+inputs+["-filter_complex",";".join(fp),"-map","[out]","-c:a","aac","-b:a","192k","-t",str(total),out], check=True, capture_output=True)
    print(f"  ✓ {out}")

if __name__ == "__main__":
    print("Step 1: TTS ..."); data = process()
    print("\nStep 2: SFX ...")
    for name,(p,du,_g) in SFX_KIT.items(): sfx(p,name,du)
    print("\nStep 3: re-time + word-sync ..."); starts, durs, total = transform(data)
    print("\nStep 4: audio (voice + SFX) ..."); build_audio(starts, total, data, str(CACHE/"main.aac"))
    print("\nStep 5: captions ..."); build_srt(starts, str(EP/"script.srt"))
    print("\nScene map:")
    for s in SCENES: print(f"  {s:<4} start={starts[s]:>3} dur={durs[s]:>3} clip={data[s]['clip_dur']:.1f}")
    print(f"  TOTAL={total}s")
