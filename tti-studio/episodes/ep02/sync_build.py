#!/usr/bin/env python3
"""
Word-synced, joyful Dhruva voiceover + ElevenLabs SFX build for Ep2 LONG-FORM
(22 scenes, rich animated composition). See docs/VOICEOVER.md.

  cd tti-studio/episodes/ep02
  export ELEVENLABS_API_KEY="...(text_to_speech)..."
  /opt/anaconda3/bin/python3 sync_build.py
Then render composition_synced.html and mux audio_v2/main.aac.
"""
import base64, json, math, os, re, subprocess
from pathlib import Path
import requests

API   = os.environ["ELEVENLABS_API_KEY"]
VOICE = "7hshzsnMFQgQHNhu6yYM"
MODEL = "eleven_multilingual_v2"
VOICE_SETTINGS = {"stability": 0.40, "similarity_boost": 0.75,
                  "style": 0.50, "use_speaker_boost": True, "speed": 1.06}
EP    = Path(__file__).parent
CACHE = EP / "audio_v2"; CACHE.mkdir(exist_ok=True)
SFXD  = CACHE / "sfx"; SFXD.mkdir(exist_ok=True)
SRC_HTML = EP / "composition.html"
OUT_HTML = EP / "composition_synced.html"
COMP_ID  = "sdep02full"
LEAD, HEAD_BASE, STAGGER, TAIL_PAD = 0.25, 0.40, 0.40, 1.50

SCENES = [f"s{i}" for i in range(1, 23)]
OLD = {"s1":(0,40),"s2":(40,30),"s3":(70,40),"s4":(110,40),"s5":(150,40),
 "s6":(190,40),"s7":(230,45),"s8":(275,45),"s9":(320,50),"s10":(370,35),
 "s11":(405,40),"s12":(445,45),"s13":(490,60),"s14":(550,45),"s15":(595,40),
 "s16":(635,45),"s17":(680,50),"s18":(730,45),"s19":(775,45),"s20":(820,50),
 "s21":(870,55),"s22":(925,45)}
HEAD_DUR = {"s1":1.0,"s22":1.0}

BEATS = {
 "s1":[
  ("Hey, welcome back to The Tech Intern, system design. I'm Dhruva, and this is the show where we build huge apps from scratch, one box at a time.", ["s1k","s1t"]),
  ("Last time, we built a baby Instagram, and we found the big secret: every app is really just three pieces. A client, a server, and a database, passing a request back and forth.", ["s1_cli","s1_srv","s1_db"]),
  ("But I skipped something sneaky. When your phone sends that request out, how does it even find the right server? Out of billions of computers on the planet?", ["s1q"]),
  ("Tonight we crack those boxes open. What's actually inside client and server, and how they find and talk to each other. So let's order some food. Open Swiggy.", ["s1s"]),
 ],
 "s2":[
  ("Everything tonight answers just two questions.", ["s2k","s2t"]),
  ("One. What's really inside those words, client and server? Who does what, and where does your data actually live?", ["s2q1"]),
  ("Two. How do they find each other across the whole internet, and how do they talk once they do? Two questions. Let's go.", ["s2q2"]),
 ],
 "s3":[
  ("Here's the one picture to hold in your head all episode. A restaurant.", ["s3k","s3t"]),
  ("The dining room is the client. It's where you sit, read the menu, and place your order. Comfortable, friendly. But no food is actually cooked there.", ["s3cli"]),
  ("The kitchen is the server. That's where the cooking happens, where the recipes live, and where the pantry, your data, is guarded. You never see it. And the waiter carrying orders between them? We'll meet him soon.", ["s3srv","s3api"]),
 ],
 "s4":[
  ("So, the client. That's your phone, running the Swiggy app. The dining room.", ["s4k","s4t","s4phone"]),
  ("Its whole job is the stuff you see and touch. It shows you the screen. The restaurants, the photos, the buttons.", ["s4c1"]),
  ("It handles your taps and your typing. Scrolling, searching, animating.", ["s4c2"]),
  ("And when it needs something real, it asks the server. But notice: it holds no real data of its own. It's just showing you a copy.", ["s4c3"]),
 ],
 "s5":[
  ("Now the kitchen. The server. This is a powerful computer in a data centre, maybe a thousand kilometres away.", ["s5k","s5t","s5rack"]),
  ("It runs the actual logic. The brains of the whole thing.", ["s5b1"]),
  ("It enforces the rules. What's allowed, what isn't.", ["s5b2"]),
  ("And it owns the data. The database, where every restaurant, every order, every rupee actually lives. The real source of truth.", ["s5b3"]),
 ],
 "s6":[
  ("Which brings up the most important idea here. The database is always on the server side. Always.", ["s6k","s6t"]),
  ("Your phone only ever holds a temporary copy. Just what's on the screen this very second.", ["s6cli"]),
  ("The real, permanent data lives on the server. Pull to refresh, and the truth comes straight from the kitchen. Your phone is a window onto the data, not where it's kept.", ["s6arrow","s6srv","s6note"]),
 ],
 "s7":[
  ("And that leads to the golden rule of system design. Say it with me. Never trust the client.", ["s7k","s7t"]),
  ("Why? Because anyone can mess with their own phone. Picture a hacked app that claims this order costs one rupee.", ["s7cli","s7strike"]),
  ("The server doesn't just believe it. It re-checks against its own data. The real price is two ninety-nine. Even if you tampered with the app, the kitchen has the final say. Always.", ["s7srv","s7v","s7note"]),
 ],
 "s8":[
  ("So how do the dining room and the kitchen actually talk? Through a waiter. In tech, we call that waiter an A-P-I. It stands for Application Programming Interface. Long name, simple job. It's the agreed-on way the client asks, and the server answers.", ["s8k","s8t","s8gate"]),
  ("And here's the neat part. The same kitchen can serve many dining rooms.", ["s8c1","s8c2","s8c3"]),
  ("The iOS app, the Android app, the website. All different clients, all talking to one single backend, through that same API. Why build it this way? Three reasons. Security, so the rules live in one trusted place. Reuse, one backend for every app. And scale, so you can grow each side on its own.", ["s8srv","s8note"]),
 ],
 "s9":[
  ("Quick question, but an important one. Who actually draws the page you see? There are two answers.", ["s9k","s9t"]),
  ("Server-side rendering, S-S-R. The kitchen plates the whole dish and sends it out ready. The page shows up fast, and search engines love it. The catch: more work for the server every time.", ["s9ssr"]),
  ("Client-side rendering, C-S-R. The kitchen sends raw ingredients and a recipe, and your phone cooks the page itself. Slower to show that first screen, but buttery smooth after. Most big apps do both. First screen from the server, everything after on the phone. A trade-off, not a winner.", ["s9csr","s9note"]),
 ],
 "s10":[
  ("Okay, question two. Your phone wants Swiggy's kitchen. But there are billions of computers out there.", ["s10k","s10t","s10target"]),
  ("And all your phone has is a name. swiggy dot com. A name is easy for you to remember.", ["s10flip"]),
  ("But the network doesn't move data to names. It moves data to numbers. So we have a little translation problem.", ["s10note"]),
 ],
 "s11":[
  ("Because every server on the internet has a number. It's called an I-P address. I-P stands for Internet Protocol. Basically, it's a unique number that picks out one exact machine on the whole network.", ["s11k","s11t","s11card"]),
  ("Swiggy's might look like this. One-four-two, dot two-fifty, and so on.", []),
  ("Think of it as the server's phone number. This shape is called IPv4. The newer IPv6 ones are much longer, but the idea is the same. A number that points to one exact machine.", ["s11note"]),
 ],
 "s12":[
  ("So how do we get from the name to the number? With the internet's phonebook. It's called D-N-S. That's short for Domain Name System. A domain is just a name like swiggy dot com. So Domain Name System literally means the system that looks up domain names.", ["s12k","s12t"]),
  ("You type swiggy dot com, and DNS finds the matching number. Just like tapping a saved contact and letting your phone dial it.", ["s12r1","s12r2","s12r3"]),
  ("You remember the name. DNS remembers the number. You never have to.", ["s12sub"]),
 ],
 "s13":[
  ("But that lookup isn't one quick step. It's more like a relay race, handing a question down the line.", ["s13k","s13t"]),
  ("Your device checks first. Do I already have this saved? If not, it asks a helper called the resolver. That's just another computer whose whole job is doing the running around for you.", ["s13n1","s13n2"]),
  ("The resolver asks a root server, who says, I don't know, but ask the dot-com people. The dot-com server says, ask Swiggy's own server. And that last one, the authoritative server, finally knows the number.", ["s13n3","s13n4","s13n5"]),
  ("It races all the way back. Root and dot-com never knew the address. They just point you to whoever's next.", ["s13sub"]),
 ],
 "s14":[
  ("Now, do you run that whole race every single time? No. The first time, yes. After that, your device just remembers the number.", ["s14k","s14t","s14cache"]),
  ("So the second visit is basically instant.", []),
  ("But here's the question. How long should it remember before checking again? That's controlled by a setting called T-T-L. T-T-L stands for Time To Live. Basically, how long should this answer be trusted before we check again? And it's a trade-off. Set it long, and you save trips, but if the number ever changes, you're slow to find out. Set it short, you're always fresh, but you do more work. Oh, and one myth to kill. DNS only finds the address. It never loads the actual page.", ["s14ttl","s14note"]),
 ],
 "s15":[
  ("Right. We found the kitchen. Now the dining room and the kitchen need a shared language. That language is H-T-T-P. Short for HyperText Transfer Protocol. Fancy name, simple thing. It's just the agreed-on rules for how a client asks for something and how a server answers.", ["s15k","s15t","s15cli","s15srv"]),
  ("Your phone sends a request. Get me the restaurants. The server sends back a response. Two hundred, OK, here they are.", ["s15req","s15res"]),
  ("One ask, one answer. And then it forgets you completely. HTTP keeps no memory between requests. Hold that thought. It matters in a minute.", ["s15note"]),
 ],
 "s16":[
  ("Let's open up that request. Four parts.", ["s16k","s16t","s16env"]),
  ("The method. That's the verb, what you want done. The path. Which thing you want. The headers. Little labels attached to the request, like who you are or what format you can read. And the body. Any data you're sending up.", []),
  ("And the address itself, the URL, short for Uniform Resource Locator, packs a lot in. The scheme, how to talk, like https. The host, which server. The path, which page. And the query, extra options. Four colours, one line.", ["s16url"]),
 ],
 "s17":[
  ("Of all those methods, two do most of the work. GET and POST.", ["s17k","s17t"]),
  ("GET is for reading. Browsing the menu. It only looks, it changes nothing, and it's safe to do again and again. Its details ride right in the URL, so you can bookmark it.", ["s17get"]),
  ("POST is for writing. Placing the order. It changes something on the server, and its data rides hidden in the body, not the URL. One warning. Send a POST twice, and you might place two orders. We'll fix that double-tap problem in a later episode.", ["s17post","s17warn"]),
 ],
 "s18":[
  ("Remember how HTTP forgets you after every request? So how does the app keep you logged in? With a cookie. A cookie is just a tiny note your browser stores for a website. Think of it as an ID badge.", ["s18k","s18t","s18a"]),
  ("You log in once. The server hands your browser a little token. Set-Cookie.", ["s18b"]),
  ("From then on, every request you send quietly carries that cookie. And the server goes, ah, it's you again. Still logged in. That's all a session cookie is. A badge that says it's me.", ["s18c","s18d","s18note"]),
 ],
 "s19":[
  ("Every response also comes stamped with a status code. A quick number telling you how it went.", ["s19k","s19t","s19light"]),
  ("Two hundred is green. OK, here's what you asked for. Three-oh-one is a redirect. It moved, follow the arrow.", ["s19c1","s19c2"]),
  ("Four-oh-four. Not found. That page doesn't exist, and that one's on your side. Five hundred. Server error. The kitchen itself broke. Easy way to remember: four-something is your fault, five-something is the server's.", ["s19c3","s19c4","s19note"]),
 ],
 "s20":[
  ("One more letter. The S in H-T-T-P-S. It just stands for Secure. Plain HTTP is like a postcard. Anyone who handles it on the way can read it. Your card number, right there in the open.", ["s20k","s20t","s20post"]),
  ("HTTPS is a sealed envelope. Your phone and the server quietly agree on a secret, then scramble everything. To anyone in between, it's gibberish. That's the little padlock.", ["s20env"]),
  ("But careful. The padlock only means the line is encrypted. It does not mean the site is honest. Even scam sites can show a padlock.", ["s20note"]),
 ],
 "s21":[
  ("Let's run the whole thing, start to finish. You tap a restaurant on Swiggy.", ["s21k","s21t","s21_cli"]),
  ("First, DNS finds the server's number. Then your phone sends a sealed HTTPS request to that server, which checks the rules and pulls the real data from its database.", ["s21_dns","s21_srv","s21_db"]),
  ("The answer travels back, and the food appears on your screen. Find the address, knock politely in the right language, get your answer. That, honestly, is the whole web.", ["s21sub"]),
 ],
 "s22":[
  ("And that's it. You now know what's happening under every single tap.", ["s22k","s22t"]),
  ("A client and a server. The dining room and the kitchen. Never trust the client. DNS, the Domain Name System, turning names into numbers. HTTP, the HyperText Transfer Protocol, the shared language of request and response. And HTTPS, the sealed envelope.", ["s22r1","s22r2","s22r3","s22r4","s22r5"]),
  ("But notice. All of this took time. The request travelled, the relay raced, the data came back. So how do we measure fast? That's latency versus throughput, and that's next time. See you there.", ["s22next"]),
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

SFX_KIT = {
 "whoosh": ("short subtle clean UI transition whoosh, soft quick swoosh, no music", 0.8, 0.16),
 "zip":    ("short soft digital data blip, quick electronic UI tick zip, subtle, no music", 0.7, 0.18),
 "ping":   ("soft single UI ping, gentle notification blip, subtle, no music", 0.5, 0.16),
 "chime":  ("soft positive confirmation chime, gentle success ding, warm short, no music", 0.9, 0.20),
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
            emit(f'pop("#s1_cli", {f(R("s1","s1_cli"))}); draw("#s1_e1", 180, {f(R("s1","s1_srv")-0.2)}, 0.5); pop("#s1_srv", {f(R("s1","s1_srv"))}); draw("#s1_e2", 180, {f(R("s1","s1_db")-0.2)}, 0.5); pop("#s1_db", {f(R("s1","s1_db"))});')
            emit(f'packet("#s1pkt", 220,130,1340,130, {f(R("s1","s1_db")+0.6)}, 2.4, 3);')
            emit(f'pop("#s1q", {f(R("s1","s1q"))}); breathe("#s1q", {f(R("s1","s1q")+1.5)}, 1.12, 1.2, 8); rise("#s1s", {f(R("s1","s1s"))}, 18);')
        elif sid=="s2":
            emit(f'pop("#s2q1", {f(R("s2","s2q1"))}, 0.7); pop("#s2q2", {f(R("s2","s2q2"))}, 0.7);')
        elif sid=="s3":
            emit(f'pop("#s3cli", {f(R("s3","s3cli"))}, 0.7); pop("#s3srv", {f(R("s3","s3srv"))}, 0.7); pop("#s3api", {f(R("s3","s3api"))}, 0.7); breathe("#s3api", {f(R("s3","s3api")+1.5)}, 1.03, 2.2, 4);')
        elif sid=="s4":
            emit(f'pop("#s4phone", {f(R("s4","s4phone"))}, 0.7); floaty("#s4phone", {f(R("s4","s4phone")+1.5)}, -8, 2.6, 6);')
            emit(f'fade("#s4c1", {f(R("s4","s4c1"))}); fade("#s4c2", {f(R("s4","s4c2"))}); fade("#s4c3", {f(R("s4","s4c3"))});')
        elif sid=="s5":
            emit(f'pop("#s5rack", {f(R("s5","s5rack"))}, 0.7); fade("#s5b1", {f(R("s5","s5b1"))}); fade("#s5b2", {f(R("s5","s5b2"))}); fade("#s5b3", {f(R("s5","s5b3"))});')
        elif sid=="s6":
            emit(f'pop("#s6cli", {f(R("s6","s6cli"))}, 0.7); fade("#s6arrow", {f(R("s6","s6arrow"))}); pop("#s6srv", {f(R("s6","s6srv"))}, 0.7); rise("#s6note", {f(R("s6","s6note"))}, 18);')
        elif sid=="s7":
            emit(f'pop("#s7cli", {f(R("s7","s7cli"))}); fade("#s7strike", {f(R("s7","s7strike"))}); draw("#s7e", 180, {f(R("s7","s7srv")-0.3)}, 0.5); pop("#s7srv", {f(R("s7","s7srv"))});')
            emit(f'pop("#s7v", {f(R("s7","s7v"))}); breathe("#s7v", {f(R("s7","s7v")+1.5)}, 1.04, 1.6, 6); rise("#s7note", {f(R("s7","s7note"))}, 18);')
        elif sid=="s8":
            emit(f'pop("#s8c1", {f(R("s8","s8c1"))}); pop("#s8c2", {f(R("s8","s8c2"))}); pop("#s8c3", {f(R("s8","s8c3"))});')
            t8 = R("s8","s8c1")+1.0
            emit(f'draw("#s8e1", 340, {f(t8)}, 0.5); draw("#s8e2", 340, {f(t8+0.3)}, 0.5); draw("#s8e3", 340, {f(t8+0.6)}, 0.5); pop("#s8gate", {f(R("s8","s8gate"))});')
            emit(f'packet("#s8p1", 320,70,620,190, {f(t8+1.2)}, 1.4, 3); packet("#s8p2", 320,190,620,190, {f(t8+1.2)}, 1.4, 3); packet("#s8p3", 320,310,620,190, {f(t8+1.2)}, 1.4, 3);')
            emit(f'draw("#s8e4", 180, {f(R("s8","s8srv")-0.3)}, 0.5); pop("#s8srv", {f(R("s8","s8srv"))}); rise("#s8note", {f(R("s8","s8note"))}, 18);')
        elif sid=="s9":
            emit(f'pop("#s9ssr", {f(R("s9","s9ssr"))}, 0.7); tl.fromTo("#s9ssrbar",{{scaleX:0,transformOrigin:"left center"}},{{scaleX:1,duration:0.5,ease:"power2.out"}}, {f(R("s9","s9ssr")+0.5)});')
            emit(f'pop("#s9csr", {f(R("s9","s9csr"))}, 0.7); tl.fromTo("#s9csrbar",{{scaleX:0,transformOrigin:"left center"}},{{scaleX:1,duration:0.5,ease:"power2.out"}}, {f(R("s9","s9csr")+0.5)}); tl.to("#s9spin",{{rotation:360,duration:1.4,ease:"none",repeat:6,transformOrigin:"center"}}, {f(R("s9","s9csr"))});')
            emit(f'rise("#s9note", {f(R("s9","s9note"))}, 18);')
        elif sid=="s10":
            emit(f'pop("#s10target", {f(R("s10","s10target"))}); breathe("#s10target", {f(R("s10","s10target")+1.5)}, 1.06, 1.4, 8); fade("#s10flip", {f(R("s10","s10flip"))}); rise("#s10note", {f(R("s10","s10note"))}, 18);')
        elif sid=="s11":
            emit(f'pop("#s11card", {f(R("s11","s11card"))}, 0.8); floaty("#s11card", {f(R("s11","s11card")+1.5)}, -8, 2.4, 5); rise("#s11note", {f(R("s11","s11note"))}, 18);')
        elif sid=="s12":
            emit(f'fade("#s12r1", {f(R("s12","s12r1"))}); pop("#s12r2", {f(R("s12","s12r2"))}, 0.6); breathe("#s12r2", {f(R("s12","s12r2")+1.5)}, 1.02, 1.8, 5); fade("#s12r3", {f(R("s12","s12r3"))}); rise("#s12sub", {f(R("s12","s12sub"))}, 18);')
        elif sid=="s13":
            emit(f'pop("#s13n1", {f(R("s13","s13n1"))}); pop("#s13n2", {f(R("s13","s13n2"))}); pop("#s13n3", {f(R("s13","s13n3"))}); pop("#s13n4", {f(R("s13","s13n4"))}); pop("#s13n5", {f(R("s13","s13n5"))});')
            tb = R("s13","s13n5")+0.6
            emit(f'tl.to("#s13baton",{{opacity:1,duration:0.2}}, {f(tb)}); tl.to("#s13halo",{{opacity:0.5,duration:0.2}}, {f(tb)});')
            xs = [480,800,1120,1480]; rings=["#s13r2","#s13r3","#s13r4","#s13r5"]; t=tb+0.3
            for x,rg in zip(xs,rings):
                emit(f'tl.to("#s13baton",{{attr:{{cx:{x}}},duration:0.5,ease:"power2.inOut"}}, {f(t)}); tl.to("#s13halo",{{attr:{{cx:{x}}},duration:0.5,ease:"power2.inOut"}}, {f(t)}); tl.to("#s13prog",{{attr:{{d:"M150 210 H{x}"}},duration:0.5,ease:"power2.inOut"}}, {f(t)}); ring("{rg}", {f(t+0.4)});')
                t += 0.7
            emit(f'fade("#s13b3", {f(tb+1.3)}); fade("#s13b4", {f(tb+2.0)});')
            emit(f'fade("#s13res", {f(t+0.1)}); tl.to("#s13baton",{{opacity:0,duration:0.2}}, {f(t)}); tl.to("#s13halo",{{opacity:0,duration:0.2}}, {f(t)});')
            emit(f'rise("#s13sub", {f(R("s13","s13sub"))}, 18);')
        elif sid=="s14":
            emit(f'pop("#s14cache", {f(R("s14","s14cache"))}, 0.7); pop("#s14ttl", {f(R("s14","s14ttl"))}, 0.7); draw("#s14arc", 320, {f(R("s14","s14ttl")+0.4)}, 1.2); rise("#s14note", {f(R("s14","s14note"))}, 18);')
        elif sid=="s15":
            emit(f'pop("#s15cli", {f(R("s15","s15cli"))}); pop("#s15srv", {f(R("s15","s15srv"))});')
            tr = R("s15","s15req")
            emit(f'draw("#s15req", 820, {f(tr)}, 0.6); tl.set("#s15reqp",{{opacity:1}}, {f(tr+0.4)}); tl.fromTo("#s15reqp",{{x:-410}},{{x:410,duration:1.2,ease:"power1.inOut"}}, {f(tr+0.4)}); tl.set("#s15reqp",{{opacity:0}}, {f(tr+1.8)});')
            ts = R("s15","s15res")
            emit(f'draw("#s15res", 820, {f(ts)}, 0.6); tl.set("#s15resp",{{opacity:1}}, {f(ts+0.4)}); tl.fromTo("#s15resp",{{x:410}},{{x:-410,duration:1.2,ease:"power1.inOut"}}, {f(ts+0.4)}); tl.set("#s15resp",{{opacity:0}}, {f(ts+1.8)});')
            emit(f'rise("#s15note", {f(R("s15","s15note"))}, 18);')
        elif sid=="s16":
            emit(f'pop("#s16env", {f(R("s16","s16env"))}, 0.8); rise("#s16url", {f(R("s16","s16url"))}, 18);')
        elif sid=="s17":
            emit(f'pop("#s17get", {f(R("s17","s17get"))}, 0.7); pop("#s17post", {f(R("s17","s17post"))}, 0.7); rise("#s17warn", {f(R("s17","s17warn"))}, 18);')
        elif sid=="s18":
            emit(f'pop("#s18a", {f(R("s18","s18a"))}); draw("#s18e1", 140, {f(R("s18","s18b")-0.2)}, 0.4); pop("#s18b", {f(R("s18","s18b"))}); draw("#s18e2", 140, {f(R("s18","s18c")-0.2)}, 0.4); pop("#s18c", {f(R("s18","s18c"))}); pop("#s18d", {f(R("s18","s18d"))}); breathe("#s18d", {f(R("s18","s18d")+1.4)}, 1.06, 1.4, 5); rise("#s18note", {f(R("s18","s18note"))}, 18);')
        elif sid=="s19":
            emit(f'pop("#s19light", {f(R("s19","s19light"))});')
            emit(f'pop("#s19c1", {f(R("s19","s19c1"))}, 0.5); pop("#s19c2", {f(R("s19","s19c2"))}, 0.5);')
            emit(f'pop("#s19c3", {f(R("s19","s19c3"))}, 0.5); tl.fromTo("#s19y",{{fill:"#1B2A47"}},{{fill:"#6AA0FF",duration:0.3}}, {f(R("s19","s19c3"))}); pop("#s19c4", {f(R("s19","s19c4"))}, 0.5); tl.fromTo("#s19rd",{{fill:"#1B2A47"}},{{fill:"#FF6B6B",duration:0.3}}, {f(R("s19","s19c4"))});')
            emit(f'rise("#s19note", {f(R("s19","s19note"))}, 18);')
        elif sid=="s20":
            emit(f'pop("#s20post", {f(R("s20","s20post"))}, 0.7); pop("#s20env", {f(R("s20","s20env"))}, 0.7); breathe("#s20env", {f(R("s20","s20env")+1.5)}, 1.03, 2.0, 5); rise("#s20note", {f(R("s20","s20note"))}, 18);')
        elif sid=="s21":
            emit(f'pop("#s21_cli", {f(R("s21","s21_cli"))}); draw("#s21e1", 100, {f(R("s21","s21_dns")-0.2)}, 0.4); pop("#s21_dns", {f(R("s21","s21_dns"))}); draw("#s21e2", 100, {f(R("s21","s21_srv")-0.2)}, 0.4); pop("#s21_srv", {f(R("s21","s21_srv"))}); draw("#s21e3", 100, {f(R("s21","s21_db")-0.2)}, 0.4); pop("#s21_db", {f(R("s21","s21_db"))});')
            emit(f'packet("#s21pkt", 160,185,1430,185, {f(R("s21","s21_db")+0.5)}, 2.8, 8); rise("#s21sub", {f(R("s21","s21sub"))}, 18);')
        elif sid=="s22":
            emit(f'tl.to("#s22t .ac",{{opacity:0.72,duration:1.5,ease:"sine.inOut",repeat:4,yoyo:true}}, {f(R("s22","s22t")+3)});')
            emit(f'pop("#s22r1", {f(R("s22","s22r1"))}, 0.5); pop("#s22r2", {f(R("s22","s22r2"))}, 0.5); pop("#s22r3", {f(R("s22","s22r3"))}, 0.5); pop("#s22r4", {f(R("s22","s22r4"))}, 0.5); pop("#s22r5", {f(R("s22","s22r5"))}, 0.5);')
            emit(f'rise("#s22next", {f(R("s22","s22next"))}, 18);')
    return "\n".join(L) + "\n"

def sfx_cues(starts, data):
    def R(sid,sel): return starts[sid] + data[sid]["reveal"].get(sel, HEAD_BASE)
    g = {k:v[2] for k,v in SFX_KIT.items()}
    cues = [("whoosh", max(starts[sid]-0.2,0), g["whoosh"]) for sid in SCENES[1:]]
    cues.append(("zip", R("s1","s1_db")+0.6, g["zip"]))
    cues.append(("zip", R("s13","s13n5")+0.9, g["zip"]))
    cues.append(("zip", R("s15","s15req")+0.4, g["zip"]))
    cues.append(("ping", R("s15","s15res")+0.4, g["ping"]))
    cues.append(("zip", R("s21","s21_db")+0.5, g["zip"]))
    cues.append(("chime", R("s7","s7v"), g["chime"]))
    cues.append(("chime", R("s13","s13sub")-0.5, g["chime"]))
    cues.append(("ping", R("s18","s18d"), g["ping"]))
    cues.append(("chime", R("s22","s22r1"), g["chime"]))
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
        src, n = re.subn(rf'(id="{sid}" data-start=)"{os_}"( data-duration=)"{od_}"', rf'\g<1>"{starts[sid]}"\g<2>"{durs[sid]}"', src)
        assert n==1, f"{sid} div n={n}"
    a = "      // === DRAFT TIMELINE START ==="; b = "      // === DRAFT TIMELINE END ==="
    si = src.index(a); ei = src.index(b)
    src = src[:si] + build_timeline(starts, durs, data) + src[ei+len(b):]
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
