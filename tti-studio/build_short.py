#!/usr/bin/env python3
"""
build_short.py — vertical (1080×1920, 9:16) ~90s recap Shorts for ep01/ep02/ep03/ep04.

Each Short covers the whole episode briskly, word-synced TTS, brand SFX.
Reuses SFX cache from episodes/ep01/audio_v2/sfx/.
Output: episodes/ep{N}/short/short.mp4

Usage:
    export ELEVENLABS_API_KEY="..."
    /opt/anaconda3/bin/python3 build_short.py --ep 3
    /opt/anaconda3/bin/python3 build_short.py --ep all
"""
import argparse, base64, json, math, os, re, subprocess, sys
from pathlib import Path
import requests

# ── Voice & API ──────────────────────────────────────────────────────────────
VOICE = "7hshzsnMFQgQHNhu6yYM"
MODEL = "eleven_multilingual_v2"
VOICE_SETTINGS = {
    "stability": 0.30, "similarity_boost": 0.75,
    "style": 0.65, "use_speaker_boost": True, "speed": 1.02,
}
API = os.environ.get("ELEVENLABS_API_KEY", "")
LEAD, HEAD_BASE, STAGGER, TAIL_PAD = 0.25, 0.40, 0.22, 1.0

STUDIO = Path(__file__).parent
SFX_SRC = STUDIO / "episodes/ep01/audio_v2/sfx"  # pre-generated SFX cache

# ── Scripts (full episode in ~90s) ───────────────────────────────────────────
SCRIPTS = {
"ep01": (
    "You open Swiggy. So does half your city. It doesn't even lag. How? "
    "Every app — every single one — is built from three things. "
    "A client: your phone, the thing that asks. "
    "A server: the brain that answers. "
    "A database: the shelf where everything's stored. "
    "When you tap order, your phone sends a request to the server. "
    "Think of it like asking a librarian for a book. "
    "The server finds it, asks the database to fetch it, and sends the answer back. "
    "That whole loop is system design. "
    "But here's where it gets interesting. When you're building for ten users, one server is fine. "
    "Now imagine ten million people walking into the library at the same time. "
    "That's when you need more servers, smarter databases, and a whole new set of tools — caching, load balancing, CDNs. "
    "Disney+ Hotstar held 59 million concurrent viewers during the 2023 World Cup final. "
    "Same three pieces — client, server, database — just engineered at a scale most people never think about. "
    "That's system design. And it starts with one request."
),
"ep02": (
    "You type swiggy.com. In under a second, your phone finds the exact server — out of billions on the internet. Here's how. "
    "Step one: your phone doesn't know where swiggy.com lives. It only knows names, not addresses. "
    "So it asks a DNS resolver — the internet's phonebook. "
    "The resolver checks its cache, asks the root server, asks the TLD server, and finally gets the answer: the IP address. "
    "Now your phone knows where to go. "
    "Step two: HTTP. Your phone sends a request — a method, a path, headers. "
    "GET /restaurants — show me the list. "
    "The server reads it, does the work, and sends back a response with a status code. "
    "200: here it is. 404: not found. 500: the server crashed — that's not your fault. "
    "And that S in HTTPS? It means the whole conversation is encrypted. "
    "Every message sealed in an envelope. "
    "The padlock means encrypted — not that the website is trustworthy. Important difference. "
    "Name to IP. Request to response. "
    "That's the whole journey — every time you tap anything on the internet."
),
"ep03": (
    "It's 8pm. Half of Mumbai just opened Swiggy at the same time. "
    "The server slows down — and it's slow can mean three completely different things. "
    "One: Latency. How long does one single request take, end to end? "
    "You tap order, it hits the server, hits the database, comes back. Total: 65 milliseconds. "
    "That's latency. When it's high, you watch a spinner. "
    "Two: Throughput. How many requests can the system handle per second? "
    "One cook in a kitchen makes one dish at a time — that's low throughput. "
    "Four cooks, four dishes simultaneously. Engineers measure this in qps — queries per second. "
    "Three: Bandwidth. The size of the pipe. "
    "The IPL final on Hotstar — 32 million streams at once, 4 megabits each — that's 128 terabits per second. "
    "You can't serve that from one building. "
    "Here's the trap: latency and throughput aren't the same thing. "
    "The Western Express Highway at 8pm — thousands of cars moving, but each one stuck in traffic. "
    "High throughput, terrible latency. "
    "And engineers track this with two numbers: p50 and p99. "
    "The p99 is the one that matters — one in a hundred users, sitting there for nearly a second. "
    "On 10,000 requests per second, that's 100 people having a bad time. Every. Single. Second. "
    "Three numbers. Three different problems. Three different fixes."
),
"ep04": (
    "A Swiggy engineer in Bangalore stares at a dashboard. "
    "Numbers everywhere — but which ones actually matter? "
    "Two you already know: qps, and p50 versus p99. "
    "But here's a mistake almost everyone makes — a lakh users online isn't a lakh requests a second. "
    "Most people are just staring at the menu. "
    "What actually matters is headroom — how close you are to the ceiling before everything breaks. "
    "Two thousand out of ten thousand qps? Plenty of room. "
    "Cross that ceiling, and it's not graceful — queues form, and milliseconds turn into seconds. "
    "Then there's a third number: nines. "
    "Ninety-nine percent uptime sounds great — until you realize that's three point six five days of downtime a year. "
    "Add one nine — ninety-nine point nine nine percent — and that drops to fifty-two minutes. "
    "That's why UPI can't run on fewer nines. "
    "Money stuck mid-transfer isn't a rounding error. "
    "It's a national story. "
    "More nines isn't always worth it, either. "
    "An internal dashboard breaking for twenty minutes is annoying. "
    "A payment system doing the same is a headline. "
    "Now go back to that dashboard. "
    "qps for the load. p50 and p99 for the feel. Nines for the promise being kept. "
    "But knowing the numbers doesn't fix anything by itself. "
    "That's next time — with the load balancer, the waiter who picks the kitchen."
),
}

# ── Beats: (narration_text, [element_ids_to_reveal]) ─────────────────────────
# Elements in the same list stagger 0.22s apart — still word-synced.
# Tag + headline always grouped together so the scene never flashes up half-empty.
BEATS = {
"ep01": [
    ("You open Swiggy. So does half your city. It doesn't even lag. How?", ["hook_big", "hook_label"]),
    ("Every app — every single one — is built from three things.", ["three_tag", "three_headline"]),
    ("A client: your phone, the thing that asks.", ["n_client"]),
    ("A server: the brain that answers.", ["n_arr1", "n_server"]),
    ("A database: the shelf where everything's stored.", ["n_arr2", "n_db"]),
    ("When you tap order, your phone sends a request to the server.", ["req_tag", "req_headline"]),
    ("Think of it like asking a librarian for a book.", ["req_card"]),
    ("The server finds it, asks the database to fetch it, and sends the answer back.", ["req_cycle"]),
    ("That whole loop is system design.", ["req_label"]),
    ("But here's where it gets interesting. When you're building for ten users, one server is fine.", ["scale_tag", "scale_small"]),
    ("Now imagine ten million people walking into the library at the same time.", ["scale_large"]),
    ("That's when you need more servers, smarter databases, and a whole new set of tools — caching, load balancing, CDNs.", ["scale_tools"]),
    ("Disney+ Hotstar held 59 million concurrent viewers during the 2023 World Cup final.", ["hotstar_num", "hotstar_sub"]),
    ("Same three pieces — client, server, database — just engineered at a scale most people never think about.", ["hotstar_card"]),
    ("That's system design. And it starts with one request.", ["cta"]),
],
"ep02": [
    ("You type swiggy.com. In under a second, your phone finds the exact server — out of billions on the internet. Here's how.", ["hook_url", "hook_stat"]),
    ("Step one: your phone doesn't know where swiggy.com lives. It only knows names, not addresses.", ["dns_tag", "dns_headline"]),
    ("So it asks a DNS resolver — the internet's phonebook.", ["dns_resolver"]),
    ("The resolver checks its cache, asks the root server, asks the TLD server, and finally gets the answer: the IP address.", ["dns_chain", "dns_ip"]),
    ("Now your phone knows where to go.", ["dns_done"]),
    ("Step two: HTTP. Your phone sends a request — a method, a path, headers.", ["http_tag", "http_headline"]),
    ("GET /restaurants — show me the list.", ["http_get"]),
    ("The server reads it, does the work, and sends back a response with a status code.", ["http_resp"]),
    ("200: here it is. 404: not found. 500: the server crashed — that's not your fault.", ["http_200", "http_404", "http_500"]),
    ("And that S in HTTPS? It means the whole conversation is encrypted.", ["https_tag", "https_headline"]),
    ("Every message sealed in an envelope.", ["https_card"]),
    ("The padlock means encrypted — not that the website is trustworthy. Important difference.", ["https_caveat"]),
    ("Name to IP. Request to response.", ["recap_main"]),
    ("That's the whole journey — every time you tap anything on the internet.", ["recap_sub", "cta"]),
],
"ep03": [
    ("It's 8pm. Half of Mumbai just opened Swiggy at the same time.", ["hook_time", "hook_label"]),
    ("The server slows down — and it's slow can mean three completely different things.", ["hook_server", "hook_three"]),
    ("One: Latency. How long does one single request take, end to end?", ["lat_tag", "lat_headline"]),
    ("You tap order, it hits the server, hits the database, comes back. Total: 65 milliseconds.", ["lat_n1", "lat_a1", "lat_n2", "lat_a2", "lat_n3", "lat_ms"]),
    ("That's latency. When it's high, you watch a spinner.", ["lat_card"]),
    ("Two: Throughput. How many requests can the system handle per second?", ["tp_tag", "tp_headline"]),
    ("One cook in a kitchen makes one dish at a time — that's low throughput.", ["tp_low"]),
    ("Four cooks, four dishes simultaneously. Engineers measure this in qps — queries per second.", ["tp_high", "tp_qps"]),
    ("Three: Bandwidth. The size of the pipe.", ["bw_tag", "bw_headline"]),
    ("The IPL final on Hotstar — 32 million streams at once, 4 megabits each — that's 128 terabits per second.", ["bw_calc", "bw_num"]),
    ("You can't serve that from one building.", ["bw_card"]),
    ("Here's the trap: latency and throughput aren't the same thing.", ["trap_title", "trap_sub"]),
    ("The Western Express Highway at 8pm — thousands of cars moving, but each one stuck in traffic.", ["trap_hi"]),
    ("High throughput, terrible latency.", ["trap_lo"]),
    ("And engineers track this with two numbers: p50 and p99.", ["nums_tag", "nums_p50"]),
    ("The p99 is the one that matters — one in a hundred users, sitting there for nearly a second.", ["nums_p99"]),
    ("On 10,000 requests per second, that's 100 people having a bad time. Every. Single. Second.", ["nums_impact"]),
    ("Three numbers. Three different problems. Three different fixes.", ["cta"]),
],
"ep04": [
    ("A Swiggy engineer in Bangalore stares at a dashboard.", ["hook_eng"]),
    ("Numbers everywhere — but which ones actually matter?", ["hook_q"]),
    ("Two you already know: qps, and p50 versus p99.", ["recap_tag", "recap_headline"]),
    ("But here's a mistake almost everyone makes — a lakh users online isn't a lakh requests a second.", ["recap_mistake"]),
    ("Most people are just staring at the menu.", ["recap_sub"]),
    ("What actually matters is headroom — how close you are to the ceiling before everything breaks.", ["head_tag", "head_headline"]),
    ("Two thousand out of ten thousand qps? Plenty of room.", ["head_room"]),
    ("Cross that ceiling, and it's not graceful — queues form, and milliseconds turn into seconds.", ["head_break"]),
    ("Then there's a third number: nines.", ["nine_tag", "nine_headline"]),
    ("Ninety-nine percent uptime sounds great — until you realize that's three point six five days of downtime a year.", ["nine_99"]),
    ("Add one nine — ninety-nine point nine nine percent — and that drops to fifty-two minutes.", ["nine_9999"]),
    ("That's why UPI can't run on fewer nines.", ["upi_tag", "upi_card"]),
    ("Money stuck mid-transfer isn't a rounding error.", ["upi_no"]),
    ("It's a national story.", ["upi_story"]),
    ("More nines isn't always worth it, either.", ["trade_tag", "trade_headline"]),
    ("An internal dashboard breaking for twenty minutes is annoying.", ["trade_lo"]),
    ("A payment system doing the same is a headline.", ["trade_hi"]),
    ("Now go back to that dashboard.", ["final_tag"]),
    ("qps for the load. p50 and p99 for the feel. Nines for the promise being kept.", ["final_headline", "final_card"]),
    ("But knowing the numbers doesn't fix anything by itself.", ["final_caveat"]),
    ("That's next time — with the load balancer, the waiter who picks the kitchen.", ["cta"]),
],
}

# ── TTS ───────────────────────────────────────────────────────────────────────
def _post_tts(text, vs):
    return requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
        headers={"xi-api-key": API, "Content-Type": "application/json"},
        json={"text": text, "model_id": MODEL, "voice_settings": vs,
              "output_format": "mp3_44100_128"},
        timeout=300)

def tts(ep, out_dir):
    mp3 = out_dir / "voice.mp3"; js = out_dir / "voice.align.json"
    if mp3.exists() and js.exists():
        print(f"  [tts] {ep} — cached"); return mp3, json.loads(js.read_text())
    text = SCRIPTS[ep]
    print(f"  [tts] {ep} — {len(text)} chars ...")
    vs = dict(VOICE_SETTINGS)
    r = _post_tts(text, vs)
    if r.status_code == 422 and "speed" in vs:
        vs.pop("speed"); r = _post_tts(text, vs)
    r.raise_for_status(); d = r.json()
    mp3.write_bytes(base64.b64decode(d["audio_base64"]))
    js.write_text(json.dumps(d["alignment"]))
    return mp3, d["alignment"]

def ffdur(p):
    return float(subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration",
         "-of","default=nk=1:nw=1",str(p)],
        capture_output=True, text=True, check=True).stdout.strip())

# ── Word-sync ─────────────────────────────────────────────────────────────────
def beat_times(beats, al):
    cs = al["character_start_times_seconds"]; t, idx = [], 0
    for (txt, _) in beats:
        t.append(cs[min(idx, len(cs)-1)]); idx += len(txt) + 1
    return t

def compute_reveals(beats, al):
    bt = beat_times(beats, al); rev = {}
    for k, (_, sels) in enumerate(beats):
        base = HEAD_BASE if k == 0 else max(bt[k] - LEAD, HEAD_BASE)
        for j, sel in enumerate(sels):
            rev[sel] = round(base + j * STAGGER, 3)
    return rev

def _f(n): n=round(float(n),3); return str(int(n)) if abs(n-round(n))<1e-9 else f"{n:g}"
def _r(rev, sel, fb=None): return rev.get(sel, fb if fb is not None else HEAD_BASE)

# ── SFX cues ──────────────────────────────────────────────────────────────────
def sfx_cues(ep, rev):
    """Returns [(sfx_name, time_s, gain)] for mixing."""
    cues = []
    def whoosh(t): cues.append(("whoosh", max(0, t - 0.15), 0.16))
    def chime(t):  cues.append(("chime",  t, 0.20))
    def zip_(t):   cues.append(("zip",    t, 0.18))

    if ep == "ep01":
        zip_(_r(rev,"hook_big"))
        whoosh(_r(rev,"three_tag")); zip_(_r(rev,"n_client")); zip_(_r(rev,"n_server")); zip_(_r(rev,"n_db"))
        whoosh(_r(rev,"req_tag")); zip_(_r(rev,"req_card")); zip_(_r(rev,"req_cycle"))
        whoosh(_r(rev,"scale_tag")); zip_(_r(rev,"scale_large"))
        chime(_r(rev,"hotstar_num")); zip_(_r(rev,"hotstar_card")); chime(_r(rev,"cta"))
    elif ep == "ep02":
        zip_(_r(rev,"hook_url")); chime(_r(rev,"hook_stat"))
        whoosh(_r(rev,"dns_tag")); zip_(_r(rev,"dns_resolver")); zip_(_r(rev,"dns_chain")); chime(_r(rev,"dns_ip"))
        whoosh(_r(rev,"http_tag")); zip_(_r(rev,"http_get"))
        zip_(_r(rev,"http_200")); zip_(_r(rev,"http_404")); zip_(_r(rev,"http_500"))
        whoosh(_r(rev,"https_tag")); zip_(_r(rev,"https_card")); zip_(_r(rev,"https_caveat"))
        chime(_r(rev,"recap_main")); chime(_r(rev,"cta"))
    elif ep == "ep03":
        zip_(_r(rev,"hook_time")); zip_(_r(rev,"hook_three"))
        whoosh(_r(rev,"lat_tag")); zip_(_r(rev,"lat_n1")); chime(_r(rev,"lat_ms")); zip_(_r(rev,"lat_card"))
        whoosh(_r(rev,"tp_tag")); zip_(_r(rev,"tp_low")); zip_(_r(rev,"tp_high")); chime(_r(rev,"tp_qps"))
        whoosh(_r(rev,"bw_tag")); chime(_r(rev,"bw_num")); zip_(_r(rev,"bw_card"))
        whoosh(_r(rev,"trap_title")); zip_(_r(rev,"trap_hi")); zip_(_r(rev,"trap_lo"))
        whoosh(_r(rev,"nums_tag")); zip_(_r(rev,"nums_p50")); chime(_r(rev,"nums_p99")); chime(_r(rev,"nums_impact"))
        chime(_r(rev,"cta"))
    elif ep == "ep04":
        zip_(_r(rev,"hook_eng")); chime(_r(rev,"hook_q"))
        whoosh(_r(rev,"recap_tag")); zip_(_r(rev,"recap_mistake")); zip_(_r(rev,"recap_sub"))
        whoosh(_r(rev,"head_tag")); zip_(_r(rev,"head_room")); chime(_r(rev,"head_break"))
        whoosh(_r(rev,"nine_tag")); zip_(_r(rev,"nine_99")); chime(_r(rev,"nine_9999"))
        whoosh(_r(rev,"upi_tag")); zip_(_r(rev,"upi_no")); chime(_r(rev,"upi_story"))
        whoosh(_r(rev,"trade_tag")); zip_(_r(rev,"trade_lo")); zip_(_r(rev,"trade_hi"))
        whoosh(_r(rev,"final_tag")); chime(_r(rev,"final_card")); chime(_r(rev,"cta"))
    return cues

# ── Composition builders ──────────────────────────────────────────────────────
FONT_PATH = "../../../assets/fonts"
GSAP_PATH = "../../../assets/vendor/gsap.min.js"

def _comp_head(comp_id, total_dur):
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"/>
<style>
@font-face{{font-family:"Inter";font-weight:700;src:url("{FONT_PATH}/inter-latin-700-normal.woff2") format("woff2");}}
@font-face{{font-family:"Inter";font-weight:600;src:url("{FONT_PATH}/inter-latin-600-normal.woff2") format("woff2");}}
@font-face{{font-family:"Inter";font-weight:400;src:url("{FONT_PATH}/inter-latin-400-normal.woff2") format("woff2");}}
@font-face{{font-family:"JetBrains Mono";font-weight:400;src:url("{FONT_PATH}/jetbrains-mono-latin-400-normal.woff2") format("woff2");}}
*{{margin:0;padding:0;box-sizing:border-box;}}
:root{{--navy:#0a1628;--cobalt:#3B7BFF;--cobalt2:#6AA0FF;--text:#e8eeff;--muted:#5a7090;--hair:rgba(100,160,220,0.12);--o:#FF6B6B;}}
body{{width:1080px;height:1920px;overflow:hidden;background:var(--navy);font-family:"Inter",sans-serif;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;
  background:radial-gradient(160% 110% at 50% 10%,#1a2d50 0%,#0d1e38 45%,#080f1e 100%);}}
#grid{{position:absolute;inset:-40px;
  background-image:linear-gradient(var(--hair) 1px,transparent 1px),
                   linear-gradient(90deg,var(--hair) 1px,transparent 1px);
  background-size:54px 54px;pointer-events:none;}}
#vig{{position:absolute;inset:0;box-shadow:inset 0 0 300px 80px rgba(2,5,12,.9);pointer-events:none;}}
/* brand strip */
.brand{{position:absolute;top:0;left:0;right:0;height:100px;display:flex;align-items:center;
  justify-content:space-between;padding:0 60px;border-bottom:1px solid var(--hair);}}
.brand-l{{font-family:"JetBrains Mono";font-size:22px;color:var(--muted);letter-spacing:.18em;}}
.brand-r{{font-family:"JetBrains Mono";font-size:22px;color:var(--cobalt);letter-spacing:.12em;}}
/* scan sweep transition */
.sweep{{position:absolute;top:0;left:-100%;width:100%;height:100%;
  background:linear-gradient(90deg,transparent 0%,rgba(59,123,255,.25) 50%,transparent 100%);
  pointer-events:none;opacity:0;}}
/* scene panels */
.sc{{position:absolute;top:100px;left:0;width:1080px;height:1820px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:72px 68px;opacity:0;gap:24px;}}
/* section tag */
.sc-tag{{font-family:"JetBrains Mono";font-size:34px;letter-spacing:.18em;color:var(--cobalt);
  text-transform:uppercase;margin:0;align-self:flex-start;opacity:0;
  padding-left:20px;border-left:5px solid var(--cobalt);z-index:1;}}
/* large question */
.sc-q{{font-size:82px;font-weight:700;line-height:1.05;letter-spacing:-.03em;color:var(--text);
  text-align:center;margin-bottom:60px;opacity:0;}}
.sc-q .hi{{color:var(--cobalt2);}}
/* diagram area */
.sc-dia{{width:100%;display:flex;flex-direction:column;align-items:center;gap:24px;margin-bottom:60px;}}
/* metric reveal */
.sc-metric{{font-size:168px;font-weight:700;letter-spacing:-.04em;
  background:linear-gradient(120deg,#5EEAD4,var(--cobalt2));
  -webkit-background-clip:text;background-clip:text;color:transparent;
  opacity:0;line-height:1;z-index:1;}}
.sc-metric.orange{{background:linear-gradient(120deg,#FF8A55,#FF6B6B);
  -webkit-background-clip:text;background-clip:text;}}
.sc-sub{{font-family:"JetBrains Mono";font-size:32px;color:var(--muted);
  letter-spacing:.06em;opacity:0;margin-top:8px;}}
/* node boxes */
.node{{background:linear-gradient(160deg,#1c3050,#0f1e35);border:2px solid rgba(59,123,255,.45);
  border-radius:20px;padding:28px 36px;display:flex;flex-direction:column;
  align-items:center;gap:8px;opacity:0;}}
.node .nl{{font-family:"JetBrains Mono";font-size:22px;color:var(--cobalt);letter-spacing:.14em;text-align:center;}}
.node .nv{{font-size:44px;font-weight:700;color:var(--text);text-align:center;}}
.node.orange{{border-color:rgba(255,107,44,.55);}}
.node.orange .nl{{color:#FF8A55;}}
/* arrow connector */
.arrow-down{{width:4px;height:60px;background:linear-gradient(180deg,var(--cobalt),rgba(59,123,255,.2));
  border-radius:2px;position:relative;opacity:0;}}
.arrow-down::after{{content:"";position:absolute;bottom:-10px;left:50%;transform:translateX(-50%);
  border:10px solid transparent;border-top:14px solid var(--cobalt);}}
/* stat rows */
.stat-row{{width:100%;display:flex;align-items:center;justify-content:space-between;
  padding:32px 44px;background:linear-gradient(160deg,#182840,#0d1928);
  border-radius:20px;border:2px solid rgba(59,123,255,.35);opacity:0;z-index:1;}}
.stat-row .sn{{font-family:"JetBrains Mono";font-size:46px;color:var(--cobalt);letter-spacing:.08em;}}
.stat-row .sv{{font-size:66px;font-weight:700;color:var(--text);}}
.stat-row .sd{{font-family:"JetBrains Mono";font-size:30px;color:var(--muted);}}
/* split panels (Latency ≠ Throughput) */
.split{{width:100%;display:flex;flex-direction:column;gap:32px;}}
.split-half{{background:linear-gradient(160deg,#1c3050,#0f1e35);border-radius:24px;
  padding:48px 40px;border:2px solid rgba(59,123,255,.3);opacity:0;}}
.split-half.orange{{border-color:rgba(255,107,44,.4);}}
.split-half .sh-label{{font-family:"JetBrains Mono";font-size:28px;color:var(--muted);
  letter-spacing:.1em;margin-bottom:18px;text-align:center;}}
.split-half .sh-val{{font-size:62px;font-weight:700;color:var(--text);line-height:1.1;text-align:center;}}
.split-half .sh-tag{{font-size:34px;color:var(--cobalt);margin-top:10px;font-weight:600;text-align:center;}}
.split-half.orange .sh-tag{{color:#FF8A55;}}
/* hook elements */
.hook-stat{{font-size:210px;font-weight:700;letter-spacing:-.05em;
  color:var(--cobalt2);opacity:0;line-height:1;z-index:1;}}
.hook-label{{font-size:68px;font-weight:600;color:var(--text);opacity:0;
  text-align:center;line-height:1.2;z-index:1;}}
.hook-sub{{font-family:"JetBrains Mono";font-size:34px;color:var(--muted);
  opacity:0;margin:0;letter-spacing:.04em;text-align:center;z-index:1;}}
/* CTA */
.cta-big{{font-size:72px;font-weight:700;color:var(--text);opacity:0;
  text-align:center;line-height:1.15;}}
.cta-sub{{font-family:"JetBrains Mono";font-size:36px;color:var(--cobalt);
  opacity:0;margin:0;letter-spacing:.08em;z-index:1;}}
/* ghost bg — always visible when panel is active, pure decoration */
.ghost-bg{{position:absolute;font-size:520px;font-weight:700;
  color:rgba(59,123,255,0.04);-webkit-text-stroke:2px rgba(59,123,255,0.13);
  pointer-events:none;bottom:-100px;right:-40px;line-height:1;z-index:0;
  user-select:none;white-space:nowrap;}}
/* big scene headline — 124px instead of 82px */
.sc-headline{{font-size:128px;font-weight:700;line-height:1.05;letter-spacing:-.03em;
  color:var(--text);text-align:center;margin:0;opacity:0;z-index:1;}}
.sc-headline .hi{{color:var(--cobalt2);}}
.sc-headline .og{{color:var(--o);}}
/* horizontal chain */
.h-chain{{display:flex;align-items:center;justify-content:center;width:100%;gap:12px;z-index:1;margin:0;}}
.h-node{{background:linear-gradient(160deg,#1c3050,#0f1e35);border:2px solid rgba(59,123,255,.45);
  border-radius:18px;padding:28px 20px;display:flex;flex-direction:column;align-items:center;
  gap:10px;opacity:0;flex:1;min-width:0;}}
.h-node.og{{border-color:rgba(255,107,44,.5);}}
.h-node .hl{{font-family:"JetBrains Mono";font-size:22px;color:var(--cobalt);letter-spacing:.08em;text-align:center;}}
.h-node.og .hl{{color:#FF8A55;}}
.h-node .hv{{font-size:44px;font-weight:700;color:var(--text);text-align:center;}}
.h-arrow{{font-size:40px;color:var(--cobalt);opacity:0;padding:0 4px;flex-shrink:0;z-index:1;font-weight:700;}}
/* node card */
.node-card{{background:linear-gradient(160deg,#182840,#0d1928);border:2px solid rgba(59,123,255,.35);
  border-radius:22px;padding:40px 48px;width:100%;opacity:0;z-index:1;text-align:center;}}
.node-card.og{{border-color:rgba(255,107,44,.45);}}
.node-card .nc-label{{font-family:"JetBrains Mono";font-size:26px;color:var(--cobalt);
  letter-spacing:.12em;margin-bottom:16px;text-align:center;}}
.node-card.og .nc-label{{color:#FF8A55;}}
.node-card .nc-val{{font-size:54px;font-weight:700;color:var(--text);line-height:1.2;text-align:center;}}
.node-card .nc-sub{{font-family:"JetBrains Mono";font-size:28px;color:var(--muted);margin-top:12px;text-align:center;}}
/* ep badge */
.ep-badge{{display:inline-flex;background:linear-gradient(180deg,#FF7A3C,#F2540E);
  color:#fff;font-family:"JetBrains Mono";font-size:26px;letter-spacing:.2em;
  padding:14px 28px;border-radius:10px;opacity:0;margin-bottom:48px;z-index:1;}}
</style>
<script src="{GSAP_PATH}"></script>
</head>
<body>
<div id="root" data-composition-id="{comp_id}" data-start="0" data-duration="{total_dur}">
  <div id="grid"></div>
  <div id="vig"></div>
  <div class="sweep" id="sw1"></div>
  <div class="sweep" id="sw2"></div>
  <div class="sweep" id="sw3"></div>
  <div class="sweep" id="sw4"></div>
  <div class="sweep" id="sw5"></div>
  <div class="sweep" id="sw6"></div>
  <div class="brand">
    <span class="brand-l">THE TECH INTERN</span>
    <span class="brand-r">// SYSTEM DESIGN</span>
  </div>
"""

def _sweep(sw_id, t):
    return (f'tl.set("#{sw_id}",{{opacity:1,left:"-100%"}},{_f(t)});'
            f'tl.to("#{sw_id}",{{left:"100%",duration:0.4,ease:"power2.inOut",opacity:1}},{_f(t)});'
            f'tl.set("#{sw_id}",{{opacity:0}},{_f(t+0.45)});')

def _scene_in(sc_id, sw, t):
    return (f'{_sweep(sw, t-0.2)}'
            f'tl.to("#{sc_id}",{{opacity:1,duration:0.25,ease:"power2.out"}},{_f(t)});')

def _scene_out(sc_id, t):
    return f'tl.to("#{sc_id}",{{opacity:0,duration:0.2,ease:"power2.in"}},{_f(t-0.2)});'

def _fade(sel, t, d=0.45):    return f'tl.to("#{sel}",{{opacity:1,duration:{d},ease:"power2.out"}},{_f(t)});'
def _rise(sel, t, d=0.4):     return f'tl.fromTo("#{sel}",{{opacity:0,y:28}},{{opacity:1,y:0,duration:{d},ease:"power3.out"}},{_f(t)});'
def _slide(sel, t, dx=-60, d=0.38): return f'tl.fromTo("#{sel}",{{opacity:0,x:{dx}}},{{opacity:1,x:0,duration:{d},ease:"power3.out"}},{_f(t)});'
def _pop(sel, t, d=0.45):     return f'tl.fromTo("#{sel}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:{d},ease:"back.out(2)"}},{_f(t)});'
def _grow_x(sel, t, d=0.28):  return f'tl.fromTo("#{sel}",{{opacity:0,scaleX:0,transformOrigin:"left center"}},{{opacity:1,scaleX:1,duration:{d},ease:"power2.out"}},{_f(t)});'

# ─────────────────────────────────────────────────────────────────────────────
def build_comp_ep03(rev, total):
    r = lambda sel, fb=None: _r(rev, sel, fb)
    t_lat  = r("lat_tag");  t_tp   = r("tp_tag")
    t_bw   = r("bw_tag");   t_trap = r("trap_title");  t_nums = r("nums_tag")

    html = _comp_head("short_ep03", total)
    html += """
  <!-- SC1: HOOK -->
  <div class="sc" id="sc1">
    <div class="ghost-bg">8PM</div>
    <div class="hook-stat" id="hook_time">8 PM</div>
    <div class="hook-label" id="hook_label">Half of Mumbai<br>just opened Swiggy.</div>
    <div class="hook-sub" id="hook_server" >The server slows down.</div>
    <div class="node-card" id="hook_three" >
      <div class="nc-label">SLOW CAN MEAN 3 DIFFERENT THINGS</div>
      <div class="nc-val" style="font-size:40px;">Latency · Throughput · Bandwidth</div>
    </div>
  </div>

  <!-- SC2: LATENCY -->
  <div class="sc" id="sc2">
    <div class="ghost-bg">65</div>
    <div class="sc-tag" id="lat_tag">01 / Latency</div>
    <div class="sc-headline" id="lat_headline">How long does<br><span class="hi">ONE</span> request take?</div>
    <div class="h-chain">
      <div class="h-node" id="lat_n1"><div class="hl">CLIENT</div><div class="hv">📱</div></div>
      <div class="h-arrow" id="lat_a1">→</div>
      <div class="h-node" id="lat_n2"><div class="hl">SERVER</div><div class="hv">⚡</div></div>
      <div class="h-arrow" id="lat_a2">→</div>
      <div class="h-node og" id="lat_n3"><div class="hl">DATABASE</div><div class="hv">🗄</div></div>
    </div>
    <div class="sc-metric" id="lat_ms">65 ms</div>
    <div class="node-card" id="lat_card" >
      <div class="nc-label">HIGH LATENCY MEANS</div>
      <div class="nc-val">you watch a spinner</div>
    </div>
  </div>

  <!-- SC3: THROUGHPUT -->
  <div class="sc" id="sc3">
    <div class="ghost-bg">QPS</div>
    <div class="sc-tag" id="tp_tag">02 / Throughput</div>
    <div class="sc-headline" id="tp_headline">How <span class="hi">MANY</span><br>per second?</div>
    <div class="node-card" id="tp_low" >
      <div class="nc-label">1 COOK IN A KITCHEN</div>
      <div class="nc-val">1 dish at a time</div>
      <div class="nc-sub">low throughput</div>
    </div>
    <div class="node-card" id="tp_high" style="border-color:rgba(59,123,255,.65);">
      <div class="nc-label">4 COOKS SIMULTANEOUSLY</div>
      <div class="nc-val">4 dishes at once</div>
      <div class="nc-sub">higher throughput</div>
    </div>
    <div class="sc-metric" id="tp_qps" style="font-size:100px;">qps</div>
    <div class="sc-sub" style="font-size:28px;opacity:1;">queries per second</div>
  </div>

  <!-- SC4: BANDWIDTH -->
  <div class="sc" id="sc4">
    <div class="ghost-bg">128T</div>
    <div class="sc-tag" id="bw_tag">03 / Bandwidth</div>
    <div class="sc-headline" id="bw_headline">The size<br>of the <span class="hi">pipe.</span></div>
    <div class="node-card" id="bw_calc" >
      <div class="nc-label">IPL FINAL · 32M VIEWERS</div>
      <div class="nc-val">32M × 4 Mbps</div>
    </div>
    <div class="sc-metric orange" id="bw_num">128 Tbps</div>
    <div class="node-card orange" id="bw_card" >
      <div class="nc-label">THE REALITY</div>
      <div class="nc-val">Can't serve that<br>from one building</div>
    </div>
  </div>

  <!-- SC5: LATENCY ≠ THROUGHPUT -->
  <div class="sc" id="sc5">
    <div class="ghost-bg">≠</div>
    <div class="sc-headline" id="trap_title" style="font-size:104px;">Latency<br><span class="hi">≠</span><br>Throughput</div>
    <div class="sc-sub" id="trap_sub" style="font-size:30px;">they move independently</div>
    <div class="split">
      <div class="split-half" id="trap_hi">
        <div class="sh-label">WEH AT 8PM</div>
        <div class="sh-val">Thousands of cars<br>stuck in traffic</div>
        <div class="sh-tag">High throughput · High latency</div>
      </div>
      <div class="split-half orange" id="trap_lo">
        <div class="sh-label">WEH AT 3AM</div>
        <div class="sh-val">One car, flying</div>
        <div class="sh-tag">Low throughput · Low latency</div>
      </div>
    </div>
  </div>

  <!-- SC6: THE NUMBERS -->
  <div class="sc" id="sc6">
    <div class="ghost-bg">p99</div>
    <div class="sc-tag" id="nums_tag">The Numbers</div>
    <div class="sc-headline" style="font-size:100px;opacity:1;">engineers<br>actually watch</div>
    <div style="width:100%;display:flex;flex-direction:column;gap:20px;z-index:1;">
      <div class="stat-row" id="nums_p50">
        <span class="sn">p50</span><span class="sv">45 ms</span><span class="sd">median</span>
      </div>
      <div class="stat-row" id="nums_p99" style="border-color:rgba(255,107,44,.5);">
        <span class="sn" style="color:#FF8A55;">p99</span><span class="sv">820 ms</span><span class="sd">the tail</span>
      </div>
    </div>
    <div class="node-card orange" id="nums_impact" >
      <div class="nc-label">AT 10,000 QPS</div>
      <div class="nc-val">100 people · bad time<br>every single second</div>
    </div>
    <div class="cta-sub" id="cta" >3 numbers · 3 problems · 3 fixes</div>
  </div>
</div>
"""
    js = [
        'window.__timelines = window.__timelines || {};',
        'const tl = gsap.timeline({paused: true});',
        'gsap.set("#sc1",{opacity:1});',
        # SC1
        _pop("hook_time",   r("hook_time"),   0.6),
        _rise("hook_label", r("hook_label"),   0.45),
        _slide("hook_server", r("hook_server"), -50),
        _rise("hook_three", r("hook_three"),   0.4),
        # SC2 latency
        _scene_out("sc1", t_lat), _scene_in("sc2","sw1", t_lat),
        _slide("lat_tag",      r("lat_tag"),      -40, 0.35),
        _rise("lat_headline",  r("lat_headline"),  0.45),
        _slide("lat_n1",  r("lat_n1"),  -50, 0.32),
        _grow_x("lat_a1", r("lat_a1"),  0.22),
        _slide("lat_n2",  r("lat_n2"),  -30, 0.28),
        _grow_x("lat_a2", r("lat_a2"),  0.22),
        _slide("lat_n3",  r("lat_n3"),  -30, 0.28),
        _pop("lat_ms",    r("lat_ms"),   0.55),
        _rise("lat_card", r("lat_card"), 0.4),
        # SC3 throughput
        _scene_out("sc2", t_tp), _scene_in("sc3","sw2", t_tp),
        _slide("tp_tag",      r("tp_tag"),      -40, 0.35),
        _rise("tp_headline",  r("tp_headline"),   0.45),
        _rise("tp_low",       r("tp_low"),        0.4),
        _rise("tp_high",      r("tp_high"),       0.4),
        _pop("tp_qps",        r("tp_qps"),        0.55),
        # SC4 bandwidth
        _scene_out("sc3", t_bw), _scene_in("sc4","sw3", t_bw),
        _slide("bw_tag",      r("bw_tag"),      -40, 0.35),
        _rise("bw_headline",  r("bw_headline"),   0.45),
        _rise("bw_calc",      r("bw_calc"),       0.4),
        _pop("bw_num",        r("bw_num"),        0.55),
        _rise("bw_card",      r("bw_card"),       0.4),
        # SC5 trap
        _scene_out("sc4", t_trap), _scene_in("sc5","sw4", t_trap),
        _pop("trap_title",  r("trap_title"), 0.55),
        _fade("trap_sub",   r("trap_sub"),   0.4),
        _rise("trap_hi",    r("trap_hi"),    0.4),
        _rise("trap_lo",    r("trap_lo"),    0.4),
        # SC6 numbers
        _scene_out("sc5", t_nums), _scene_in("sc6","sw5", t_nums),
        _slide("nums_tag",    r("nums_tag"),    -40, 0.35),
        _rise("nums_p50",     r("nums_p50"),     0.4),
        _rise("nums_p99",     r("nums_p99"),     0.4),
        _rise("nums_impact",  r("nums_impact"),  0.45),
        _fade("cta",          r("cta"),          0.5),
        'window.__timelines["short_ep03"] = tl;',
    ]
    html += '<script>\n' + '\n'.join(js) + '\n</script>\n</body></html>'
    return html

# ─────────────────────────────────────────────────────────────────────────────
def build_comp_ep01(rev, total):
    r = lambda sel, fb=None: _r(rev, sel, fb)
    t_three   = r("three_tag")
    t_req     = r("req_tag")
    t_scale   = r("scale_tag")
    t_hotstar = r("hotstar_num")

    html = _comp_head("short_ep01", total)
    html += """
  <!-- SC1: HOOK -->
  <div class="sc" id="sc1">
    <div class="ghost-bg">?</div>
    <div class="hook-stat" id="hook_big" style="font-size:140px;line-height:1;">SWIGGY</div>
    <div class="hook-label" id="hook_label">You open it.<br>So does half your city.<br>It doesn't even lag.</div>
    <div class="node-card" style="opacity:1;">
      <div class="nc-label">THE QUESTION</div>
      <div class="nc-val" style="font-size:52px;">How?</div>
    </div>
  </div>

  <!-- SC2: THREE PIECES -->
  <div class="sc" id="sc2">
    <div class="ghost-bg">3</div>
    <div class="sc-tag" id="three_tag">Every app · 3 pieces</div>
    <div class="sc-headline" id="three_headline">Every app.<br><span class="hi">Same 3 parts.</span></div>
    <div class="h-chain">
      <div class="h-node" id="n_client"><div class="hl">CLIENT</div><div class="hv">📱</div><div class="hl" style="font-size:14px;">the asker</div></div>
      <div class="h-arrow" id="n_arr1">→</div>
      <div class="h-node" id="n_server"><div class="hl">SERVER</div><div class="hv">🧠</div><div class="hl" style="font-size:14px;">the brain</div></div>
      <div class="h-arrow" id="n_arr2">→</div>
      <div class="h-node og" id="n_db"><div class="hl">DATABASE</div><div class="hv">🗄</div><div class="hl" style="font-size:14px;">the shelf</div></div>
    </div>
    <div class="sc-sub" style="opacity:1;font-size:28px;text-align:center;">client · server · database</div>
  </div>

  <!-- SC3: REQUEST CYCLE -->
  <div class="sc" id="sc3">
    <div class="ghost-bg">→</div>
    <div class="sc-tag" id="req_tag">Request → Response</div>
    <div class="sc-headline" id="req_headline">Like asking a<br><span class="hi">librarian</span><br>for a book.</div>
    <div class="node-card" id="req_card">
      <div class="nc-label">YOUR PHONE ASKS</div>
      <div class="nc-val" style="font-size:40px;">→ server finds it<br>→ DB fetches it<br>→ answer back</div>
    </div>
    <div class="node-card" id="req_cycle" style="border-color:rgba(59,123,255,.55);">
      <div class="nc-label">THAT WHOLE LOOP</div>
      <div class="nc-val" style="font-size:44px;">System Design</div>
    </div>
    <div class="sc-sub" id="req_label" style="font-size:28px;text-align:center;">one request · one response</div>
  </div>

  <!-- SC4: SCALE -->
  <div class="sc" id="sc4">
    <div class="ghost-bg">10M</div>
    <div class="sc-tag" id="scale_tag">The Scale Problem</div>
    <div class="node-card" id="scale_small" >
      <div class="nc-label">10 USERS</div>
      <div class="nc-val">One server. Fine.</div>
    </div>
    <div class="node-card og" id="scale_large">
      <div class="nc-label">10 MILLION USERS</div>
      <div class="nc-val">Different story.</div>
    </div>
    <div class="node-card" id="scale_tools" >
      <div class="nc-label">YOU NOW NEED</div>
      <div class="nc-val" style="font-size:38px;">More servers · Caching<br>Load balancers · CDNs</div>
    </div>
  </div>

  <!-- SC5: HOTSTAR -->
  <div class="sc" id="sc5">
    <div class="ghost-bg">59M</div>
    <div class="sc-metric" id="hotstar_num" style="font-size:108px;">59 Million</div>
    <div class="sc-sub" id="hotstar_sub" style="font-size:28px;text-align:center;">
      concurrent viewers<br>Disney+ Hotstar · 2023 World Cup
    </div>
    <div class="node-card" id="hotstar_card" >
      <div class="nc-label">STILL THE SAME 3 PIECES</div>
      <div class="nc-val" style="font-size:40px;">Client · Server · Database</div>
      <div class="nc-sub">just engineered at scale</div>
    </div>
    <div class="cta-sub" id="cta" >That's system design. Starts with one request.</div>
  </div>
</div>
"""
    js = [
        'window.__timelines = window.__timelines || {};',
        'const tl = gsap.timeline({paused: true});',
        'gsap.set("#sc1",{opacity:1});',
        # SC1
        _pop("hook_big",    r("hook_big"),    0.6),
        _rise("hook_label", r("hook_label"),   0.45),
        # SC2 three pieces
        _scene_out("sc1", t_three), _scene_in("sc2","sw1", t_three),
        _slide("three_tag",      r("three_tag"),      -40, 0.35),
        _rise("three_headline",  r("three_headline"),   0.45),
        _slide("n_client",  r("n_client"),  -50, 0.32),
        _grow_x("n_arr1",   r("n_arr1"),    0.22),
        _slide("n_server",  r("n_server"),  -30, 0.28),
        _grow_x("n_arr2",   r("n_arr2"),    0.22),
        _slide("n_db",      r("n_db"),      -30, 0.28),
        # SC3 request
        _scene_out("sc2", t_req), _scene_in("sc3","sw2", t_req),
        _slide("req_tag",      r("req_tag"),      -40, 0.35),
        _rise("req_headline",  r("req_headline"),   0.45),
        _rise("req_card",      r("req_card"),       0.4),
        _rise("req_cycle",     r("req_cycle"),      0.4),
        _fade("req_label",     r("req_label"),      0.4),
        # SC4 scale
        _scene_out("sc3", t_scale), _scene_in("sc4","sw3", t_scale),
        _slide("scale_tag",   r("scale_tag"),   -40, 0.35),
        _rise("scale_small",  r("scale_small"),  0.4),
        _rise("scale_large",  r("scale_large"),  0.4),
        _rise("scale_tools",  r("scale_tools"),  0.4),
        # SC5 hotstar
        _scene_out("sc4", t_hotstar), _scene_in("sc5","sw4", t_hotstar),
        _pop("hotstar_num",   r("hotstar_num"),   0.65),
        _fade("hotstar_sub",  r("hotstar_sub"),   0.45),
        _rise("hotstar_card", r("hotstar_card"),  0.4),
        _fade("cta",          r("cta"),           0.5),
        'window.__timelines["short_ep01"] = tl;',
    ]
    html += '<script>\n' + '\n'.join(js) + '\n</script>\n</body></html>'
    return html

# ─────────────────────────────────────────────────────────────────────────────
def build_comp_ep02(rev, total):
    r = lambda sel, fb=None: _r(rev, sel, fb)
    t_dns   = r("dns_tag");   t_http  = r("http_tag")
    t_https = r("https_tag"); t_recap = r("recap_main")

    html = _comp_head("short_ep02", total)
    html += """
  <!-- SC1: HOOK -->
  <div class="sc" id="sc1">
    <div class="ghost-bg">DNS</div>
    <div class="hook-stat" id="hook_url" style="font-size:80px;letter-spacing:-.02em;">swiggy.com</div>
    <div class="hook-stat" id="hook_stat" style="font-size:160px;">&lt;1s</div>
    <div class="hook-label" style="opacity:1;font-size:48px;">Your phone finds the right<br>server out of <span style="color:var(--cobalt2);">billions.</span></div>
  </div>

  <!-- SC2: DNS -->
  <div class="sc" id="sc2">
    <div class="ghost-bg">IP</div>
    <div class="sc-tag" id="dns_tag">Step 01 / DNS</div>
    <div class="sc-headline" id="dns_headline">Names →<br><span class="hi">Addresses</span></div>
    <div class="node-card" id="dns_resolver" >
      <div class="nc-label">DNS RESOLVER</div>
      <div class="nc-val" style="font-size:42px;">the internet's phonebook</div>
    </div>
    <div class="h-chain" id="dns_chain">
      <div class="h-node"><div class="hl">ROOT</div><div class="hv" style="font-size:28px;">.</div></div>
      <div class="h-arrow" style="opacity:1;">→</div>
      <div class="h-node"><div class="hl">TLD</div><div class="hv" style="font-size:28px;">.com</div></div>
      <div class="h-arrow" style="opacity:1;">→</div>
      <div class="h-node" style="border-color:rgba(59,123,255,.7);"><div class="hl">AUTH</div><div class="hv" style="font-size:28px;">swiggy</div></div>
    </div>
    <div class="node-card" id="dns_ip" style="border-color:rgba(59,123,255,.65);">
      <div class="nc-label">IP ADDRESS</div>
      <div class="nc-val" style="font-family:'JetBrains Mono';font-size:52px;letter-spacing:.04em;">182.50.16.4</div>
    </div>
    <div class="sc-sub" id="dns_done" style="font-size:28px;">now your phone knows where to go</div>
  </div>

  <!-- SC3: HTTP -->
  <div class="sc" id="sc3">
    <div class="ghost-bg">200</div>
    <div class="sc-tag" id="http_tag">Step 02 / HTTP</div>
    <div class="sc-headline" id="http_headline">Request →<br><span class="hi">Response</span></div>
    <div class="node-card" id="http_get" >
      <div class="nc-label">YOUR REQUEST</div>
      <div class="nc-val" style="font-family:'JetBrains Mono';font-size:48px;">GET /restaurants</div>
    </div>
    <div class="node-card" id="http_resp" >
      <div class="nc-label">SERVER DOES THE WORK</div>
      <div class="nc-val" style="font-size:40px;">finds it · sends it back</div>
    </div>
    <div style="width:100%;display:flex;gap:16px;z-index:1;">
      <div class="node-card" id="http_200" style="flex:1;padding:24px 20px;">
        <div class="nc-label">200</div><div class="nc-val" style="font-size:36px;">here it is</div>
      </div>
      <div class="node-card og" id="http_404" style="flex:1;padding:24px 20px;">
        <div class="nc-label">404</div><div class="nc-val" style="font-size:36px;">not found</div>
      </div>
      <div class="node-card og" id="http_500" style="flex:1;padding:24px 20px;border-color:rgba(255,80,80,.4);">
        <div class="nc-label" style="color:#FF6B6B;">500</div><div class="nc-val" style="font-size:36px;">server</div>
      </div>
    </div>
  </div>

  <!-- SC4: HTTPS -->
  <div class="sc" id="sc4">
    <div class="ghost-bg">🔒</div>
    <div class="sc-tag" id="https_tag">The S in HTTPS</div>
    <div class="sc-headline" id="https_headline">Every message<br><span class="hi">encrypted.</span></div>
    <div class="node-card" id="https_card" >
      <div class="nc-label">SEALED ENVELOPE</div>
      <div class="nc-val" style="font-size:44px;">No one reads it<br>in transit</div>
    </div>
    <div class="node-card og" id="https_caveat">
      <div class="nc-label">IMPORTANT DIFFERENCE</div>
      <div class="nc-val" style="font-size:40px;">Padlock = encrypted<br>NOT = trustworthy</div>
    </div>
  </div>

  <!-- SC5: RECAP -->
  <div class="sc" id="sc5">
    <div class="ghost-bg">→</div>
    <div class="sc-headline" id="recap_main" style="font-size:108px;">Name → IP<br>Request →<br>Response</div>
    <div class="node-card" id="recap_sub" >
      <div class="nc-label">THE WHOLE JOURNEY</div>
      <div class="nc-val" style="font-size:40px;">Every time you tap<br>anything on the internet.</div>
    </div>
    <div class="cta-sub" id="cta" >Episode 02 · System Design</div>
  </div>
</div>
"""
    js = [
        'window.__timelines = window.__timelines || {};',
        'const tl = gsap.timeline({paused: true});',
        'gsap.set("#sc1",{opacity:1});',
        # SC1
        _slide("hook_url",  r("hook_url"),  -60, 0.4),
        _pop("hook_stat",   r("hook_stat"),  0.6),
        # SC2 DNS
        _scene_out("sc1", t_dns), _scene_in("sc2","sw1", t_dns),
        _slide("dns_tag",      r("dns_tag"),      -40, 0.35),
        _rise("dns_headline",  r("dns_headline"),   0.45),
        _rise("dns_resolver",  r("dns_resolver"),   0.4),
        _rise("dns_chain",     r("dns_chain"),      0.4),
        _pop("dns_ip",         r("dns_ip"),         0.5),
        _fade("dns_done",      r("dns_done"),       0.4),
        # SC3 HTTP
        _scene_out("sc2", t_http), _scene_in("sc3","sw2", t_http),
        _slide("http_tag",      r("http_tag"),      -40, 0.35),
        _rise("http_headline",  r("http_headline"),   0.45),
        _slide("http_get",      r("http_get"),      -50, 0.38),
        _rise("http_resp",      r("http_resp"),      0.4),
        _rise("http_200",       r("http_200"),       0.32),
        _rise("http_404",       r("http_404"),       0.32),
        _rise("http_500",       r("http_500"),       0.32),
        # SC4 HTTPS
        _scene_out("sc3", t_https), _scene_in("sc4","sw3", t_https),
        _slide("https_tag",      r("https_tag"),      -40, 0.35),
        _rise("https_headline",  r("https_headline"),   0.45),
        _rise("https_card",      r("https_card"),       0.4),
        _rise("https_caveat",    r("https_caveat"),     0.4),
        # SC5 recap
        _scene_out("sc4", t_recap), _scene_in("sc5","sw4", t_recap),
        _pop("recap_main",  r("recap_main"),  0.6),
        _rise("recap_sub",  r("recap_sub"),   0.4),
        _fade("cta",        r("cta"),         0.5),
        'window.__timelines["short_ep02"] = tl;',
    ]
    html += '<script>\n' + '\n'.join(js) + '\n</script>\n</body></html>'
    return html

# ─────────────────────────────────────────────────────────────────────────────
def build_comp_ep04(rev, total):
    r = lambda sel, fb=None: _r(rev, sel, fb)
    t_recap = r("recap_tag"); t_head = r("head_tag"); t_nine = r("nine_tag")
    t_upi   = r("upi_tag");   t_trade = r("trade_tag"); t_final = r("final_tag")

    html = _comp_head("short_ep04", total)
    html += """
  <!-- SC1: HOOK -->
  <div class="sc" id="sc1">
    <div class="ghost-bg">?</div>
    <div class="hook-label" id="hook_eng" style="font-size:64px;">A Swiggy engineer<br>in Bangalore stares<br>at a dashboard.</div>
    <div class="node-card" id="hook_q">
      <div class="nc-label">NUMBERS EVERYWHERE</div>
      <div class="nc-val" style="font-size:48px;">which ones actually matter?</div>
    </div>
  </div>

  <!-- SC2: RECAP + THE MISTAKE -->
  <div class="sc" id="sc2">
    <div class="ghost-bg">qps</div>
    <div class="sc-tag" id="recap_tag">Two you already know</div>
    <div class="sc-headline" id="recap_headline">qps · <span class="hi">p50</span> · <span class="hi">p99</span></div>
    <div class="node-card orange" id="recap_mistake">
      <div class="nc-label">THE MISTAKE ALMOST EVERYONE MAKES</div>
      <div class="nc-val" style="font-size:40px;">1,00,000 online ≠<br>1,00,000 requests/sec</div>
    </div>
    <div class="sc-sub" id="recap_sub" style="opacity:1;font-size:30px;text-align:center;">most people are just staring at the menu</div>
  </div>

  <!-- SC3: HEADROOM -->
  <div class="sc" id="sc3">
    <div class="ghost-bg">10K</div>
    <div class="sc-tag" id="head_tag">Headroom</div>
    <div class="sc-headline" id="head_headline">How close<br>to the <span class="hi">ceiling?</span></div>
    <div class="stat-row" id="head_room">
      <span class="sn">2,000</span><span class="sv">/ 10,000 qps</span><span class="sd">plenty of room</span>
    </div>
    <div class="node-card orange" id="head_break">
      <div class="nc-label">CROSS IT</div>
      <div class="nc-val" style="font-size:40px;">queues form ·<br>ms become seconds</div>
    </div>
  </div>

  <!-- SC4: NINES -->
  <div class="sc" id="sc4">
    <div class="ghost-bg">99.99</div>
    <div class="sc-tag" id="nine_tag">The third number: nines</div>
    <div class="sc-headline" id="nine_headline" style="font-size:104px;">"Nines"</div>
    <div class="stat-row" id="nine_99">
      <span class="sn">99%</span><span class="sv">3.65 days</span><span class="sd">down / year</span>
    </div>
    <div class="stat-row" id="nine_9999" style="border-color:rgba(59,123,255,.65);">
      <span class="sn" style="color:#6AA0FF;">99.99%</span><span class="sv">52 minutes</span><span class="sd">down / year</span>
    </div>
  </div>

  <!-- SC5: UPI -->
  <div class="sc" id="sc5">
    <div class="ghost-bg">Rs</div>
    <div class="sc-tag" id="upi_tag">Real world: UPI</div>
    <div class="node-card" id="upi_card">
      <div class="nc-label">NPCI MANDATES</div>
      <div class="nc-val" style="font-size:52px;">99.99% uptime</div>
    </div>
    <div class="node-card orange" id="upi_no">
      <div class="nc-label">MONEY STUCK MID-TRANSFER</div>
      <div class="nc-val" style="font-size:44px;">isn't a rounding error</div>
    </div>
    <div class="cta-sub" id="upi_story" style="opacity:1;">it's a national story</div>
  </div>

  <!-- SC6: TRADE-OFF -->
  <div class="sc" id="sc6">
    <div class="ghost-bg">±</div>
    <div class="sc-headline" id="trade_tag" style="font-size:88px;">More nines<br>isn't always <span class="hi">worth it.</span></div>
    <div class="split">
      <div class="split-half" id="trade_lo">
        <div class="sh-label">INTERNAL DASHBOARD · 20 MIN DOWN</div>
        <div class="sh-val" style="font-size:48px;">annoying</div>
      </div>
      <div class="split-half orange" id="trade_hi">
        <div class="sh-label">PAYMENT SYSTEM · 20 MIN DOWN</div>
        <div class="sh-val" style="font-size:48px;">a headline</div>
      </div>
    </div>
  </div>

  <!-- SC7: FINAL RECAP + CTA -->
  <div class="sc" id="sc7">
    <div class="ghost-bg">3</div>
    <div class="sc-tag" id="final_tag">Back to that dashboard</div>
    <div class="sc-headline" id="final_headline" style="font-size:96px;">qps · p50/p99 · nines</div>
    <div class="node-card" id="final_card">
      <div class="nc-label">THREE NUMBERS · FIVE SECONDS</div>
      <div class="nc-val" style="font-size:42px;">the entire health<br>of the system</div>
    </div>
    <div class="sc-sub" id="final_caveat" style="opacity:1;font-size:28px;text-align:center;">but knowing them doesn't fix anything</div>
    <div class="cta-sub" id="cta">Next: the load balancer</div>
  </div>
</div>
"""
    js = [
        'window.__timelines = window.__timelines || {};',
        'const tl = gsap.timeline({paused: true});',
        'gsap.set("#sc1",{opacity:1});',
        # SC1
        _rise("hook_eng",   r("hook_eng"),    0.45),
        _rise("hook_q",     r("hook_q"),      0.4),
        # SC2 recap + mistake
        _scene_out("sc1", t_recap), _scene_in("sc2","sw1", t_recap),
        _slide("recap_tag",      r("recap_tag"),      -40, 0.35),
        _pop("recap_headline",   r("recap_headline"),   0.55),
        _rise("recap_mistake",   r("recap_mistake"),    0.4),
        _fade("recap_sub",       r("recap_sub"),        0.4),
        # SC3 headroom
        _scene_out("sc2", t_head), _scene_in("sc3","sw2", t_head),
        _slide("head_tag",      r("head_tag"),      -40, 0.35),
        _rise("head_headline",  r("head_headline"),   0.45),
        _rise("head_room",      r("head_room"),       0.4),
        _rise("head_break",     r("head_break"),      0.4),
        # SC4 nines
        _scene_out("sc3", t_nine), _scene_in("sc4","sw3", t_nine),
        _slide("nine_tag",      r("nine_tag"),      -40, 0.35),
        _pop("nine_headline",   r("nine_headline"),   0.55),
        _rise("nine_99",        r("nine_99"),         0.4),
        _rise("nine_9999",      r("nine_9999"),       0.4),
        # SC5 UPI
        _scene_out("sc4", t_upi), _scene_in("sc5","sw4", t_upi),
        _slide("upi_tag",   r("upi_tag"),   -40, 0.35),
        _rise("upi_card",   r("upi_card"),   0.4),
        _rise("upi_no",     r("upi_no"),     0.4),
        _fade("upi_story",  r("upi_story"),  0.4),
        # SC6 trade-off
        _scene_out("sc5", t_trade), _scene_in("sc6","sw5", t_trade),
        _pop("trade_tag",  r("trade_tag"),  0.55),
        _rise("trade_lo",  r("trade_lo"),   0.4),
        _rise("trade_hi",  r("trade_hi"),   0.4),
        # SC7 final recap + cta
        _scene_out("sc6", t_final), _scene_in("sc7","sw6", t_final),
        _slide("final_tag",      r("final_tag"),      -40, 0.35),
        _pop("final_headline",   r("final_headline"),   0.55),
        _rise("final_card",      r("final_card"),       0.4),
        _fade("final_caveat",    r("final_caveat"),     0.4),
        _fade("cta",             r("cta"),              0.5),
        'window.__timelines["short_ep04"] = tl;',
    ]
    html += '<script>\n' + '\n'.join(js) + '\n</script>\n</body></html>'
    return html

COMP_BUILDERS = {
    "ep01": build_comp_ep01,
    "ep02": build_comp_ep02,
    "ep03": build_comp_ep03,
    "ep04": build_comp_ep04,
}

# ── Audio mixing ──────────────────────────────────────────────────────────────
def mix_audio(voice_mp3, sfx_dir, cues, total_dur, out_aac):
    """Mix voice + SFX into a single AAC track."""
    inputs = ["-i", str(voice_mp3)]
    filter_parts = [f"[0:a]volume=1.0[base]"]
    mix = ["[base]"]

    for i, (name, t, gain) in enumerate(cues):
        sfx_path = sfx_dir / f"{name}.mp3"
        if not sfx_path.exists():
            print(f"  [sfx] missing {name}.mp3, skipping")
            continue
        idx = i + 1
        inputs += ["-i", str(sfx_path)]
        delay_ms = int(t * 1000)
        filter_parts.append(
            f"[{idx}:a]volume={gain},adelay={delay_ms}|{delay_ms}[s{idx}]"
        )
        mix.append(f"[s{idx}]")

    n = len(mix)
    filter_parts.append(f"{''.join(mix)}amix=inputs={n}:normalize=0[out]")
    filter_str = ";".join(filter_parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_str,
        "-map", "[out]",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(total_dur + 0.5),
        str(out_aac),
    ]
    subprocess.run(cmd, check=True, capture_output=True)

# ── Render ────────────────────────────────────────────────────────────────────
def render_and_mux(ep, out_dir, comp_html, voice_mp3, sfx_cues_list, clip_dur):
    comp_path = out_dir / "comp.html"
    comp_path.write_text(comp_html)
    total = math.ceil(clip_dur + TAIL_PAD)

    video_raw = out_dir / "video_raw.mp4"
    short_out = out_dir / "short.mp4"
    mixed_aac = out_dir / "mixed.aac"

    print(f"  [render] {ep} ({total}s) ...")
    comp_rel = str(comp_path.relative_to(STUDIO))
    subprocess.run([
        "npx", "--yes", "hyperframes@0.7.5", "render", str(STUDIO),
        "-c", comp_rel, "-o", str(video_raw),
        "--fps", "24", "--quality", "standard", "--workers", "2"
    ], check=True, cwd=str(STUDIO))

    print(f"  [sfx mix] ...")
    mix_audio(voice_mp3, SFX_SRC, sfx_cues_list, total, mixed_aac)

    print(f"  [mux] ...")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(video_raw), "-i", str(mixed_aac),
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-crf", "22", "-preset", "fast", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0", "-map", "1:a:0", "-shortest",
        str(short_out),
    ], check=True, capture_output=True)
    return short_out

# ── Main ──────────────────────────────────────────────────────────────────────
def run_ep(ep):
    print(f"\n{'='*60}")
    print(f"  build_short: {ep}")
    print(f"{'='*60}")
    out_dir = STUDIO / f"episodes/{ep}/short"
    out_dir.mkdir(exist_ok=True)

    # TTS
    voice_mp3, al = tts(ep, out_dir)
    clip_dur = ffdur(voice_mp3)
    print(f"  clip_dur={clip_dur:.2f}s")

    # Word-sync
    rev = compute_reveals(BEATS[ep], al)
    print("  reveals:")
    for k, v in sorted(rev.items(), key=lambda x: x[1]):
        print(f"    {k:<20} → {v:.3f}s")

    # Composition
    total = math.ceil(clip_dur + TAIL_PAD)
    comp_html = COMP_BUILDERS[ep](rev, total)

    # SFX cues
    sc = sfx_cues(ep, rev)
    print(f"  sfx cues: {len(sc)}")

    # Render + mux
    out = render_and_mux(ep, out_dir, comp_html, voice_mp3, sc, clip_dur)
    print(f"\n  ✓ {out}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ep", required=True, help="ep01 / ep02 / ep03 / ep04 / all")
    args = parser.parse_args()
    eps = ["ep01", "ep02", "ep03", "ep04"] if args.ep == "all" else [args.ep if args.ep.startswith("ep") else f"ep{args.ep.zfill(2)}"]
    for ep in eps:
        run_ep(ep)

if __name__ == "__main__":
    main()
