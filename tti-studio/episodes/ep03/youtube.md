# Ep03 — YouTube upload package

> Everything you need to ship the video. Sections are upload-order so you can
> paste them straight into YouTube Studio top to bottom.

---

## TL;DR for the upload form

| Field | Value |
|---|---|
| **Title** | Latency vs Throughput vs Bandwidth — the 3 numbers that rule every system (System Design #3) |
| **Visibility** | Public (or schedule a Premiere — see "Premiere strategy") |
| **Category** | Education |
| **Audience** | "No, it's not made for kids" |
| **Language** | English (India) |
| **Default caption language** | English (India) |
| **Comments** | All comments visible |
| **License** | Standard YouTube License |
| **Allow embedding** | Yes |
| **Show in subscriptions feed** | Yes |
| **Tags** | see "Tags" below |
| **Playlist** | The Tech Intern — System Design (season 1) |
| **Captions** | Upload `script.srt` (word-synced to narration — generate from `preview/s*.align.json` if missing) |
| **Thumbnail** | `assets/thumbnails/sd-ep03-latency-throughput.png` (rendered from the series template — see §5) |
| **Video file** | `episodes/ep03/ep03_v1.mp4` (1920×1080 · 24fps · 11:11 · ~70 MB) |

---

## 1 · Title options (pick one)

| # | Title (≤60 chars body, then a tag) | Why |
|---|---|---|
| **1 ⭐** | **Latency vs Throughput vs Bandwidth — the 3 numbers that rule every system (System Design #3)** | Direct keyword stack + "the 3 numbers" curiosity + series tag for binge-watch. **Use this one.** |
| 2 | Why "It's Slow" Means 3 Different Things — Latency, Throughput & Bandwidth Explained | Pain-point opener; better for re-cuts and Shorts since it leans on the relatable "it's slow" complaint. |
| 3 | p50, p99, qps — the system-design numbers engineers actually care about (Ep 03) | Insider/jargon-curious title; A/B fallback for the SRE / devtools crowd searching for "p99" or "qps". |

**Title-A/B tip:** YouTube lets you test titles per video now (Studio → Test & Compare). Run #1 vs #3 for the first 4 weeks; whichever wins on CTR, keep.

---

## 2 · Description

> Paste the whole block below into the **Description** field. The first ~2 lines
> are what shows above "…more" on watch pages and in search.

```
It's 8pm on a Friday. Half of Mumbai just opened Swiggy at the same time. The app slows down — and "it's slow" can mean three completely different things, with three completely different fixes.

This is how engineers actually pull that apart — latency, throughput, and bandwidth, the three numbers that rule every system at scale.

In Episode 3 of The Tech Intern · System Design, we take the abstract word "slow" and break it into three measurable things. Then we sit on the metrics engineers actually watch — p50, p99, qps — and the one trade-off that lives at the heart of every big system.

You'll walk away knowing (every term explained on first use, no jargon left dangling):
✦ Latency — how long ONE request takes, end to end (and why "65ms total" hides where the time really went)
✦ The three things that drive latency up: physical distance, server processing, database queries (the sneaky one)
✦ Throughput — how many requests per second the system can serve (qps · queries per second)
✦ Bandwidth — the physical ceiling on how much data can flow (the pipe width)
✦ The kitchen analogy: cook speed = latency, number of cooks = throughput, kitchen size = bandwidth
✦ Why high throughput and high latency can coexist (Western Express Highway at 8pm vs 3am)
✦ The IRCTC Tatkal moment — what "high load + bad latency" actually looks like
✦ p50 vs p99 — the percentile latencies engineers actually watch (and why the average lies)
✦ The long tail: why p99 is where your real users live
✦ qps — queries per second, the live pulse of throughput
✦ How a traffic spike becomes a queue, and a queue becomes 8-second p99 latency
✦ Bandwidth at IPL scale: 32M concurrent streams × 4 Mbps = 128 Tbps (and why CDNs exist)
✦ The engineer's trade-off: UPI = latency-first, Swiggy analytics = throughput-first
✦ Same infrastructure, completely different priorities — depending on what the system is for

Indian, everyday examples first. Every term explained on first use. No CS degree assumed.

⏱ Chapters
0:00 The 8pm Swiggy rush · "it's slow" doesn't mean one thing
0:35 The three questions hiding inside "slow"
0:58 Latency — how long one request takes (door to door)
1:45 What actually makes latency go up (distance, processing, the database)
2:38 Throughput — how many requests at once (qps)
3:26 The kitchen analogy — cooks, kitchens, and pipe width
4:11 Bandwidth — the physical ceiling
4:51 Latency ≠ Throughput — the Western Express Highway moment
5:52 p50, p99, qps — the numbers engineers actually watch
6:56 Why p99 matters more than the average (the long tail)
7:45 The food-rush spike — when demand crosses the ceiling
8:30 Hotstar IPL bandwidth at scale (and why CDNs exist)
9:11 The engineer's trade-off — UPI vs Swiggy analytics
10:20 Recap + what's next: SLAs, "four nines", and the vocabulary of scale

📺 Watch Episode 2: How your phone *finds* the server — DNS & HTTP
▶ https://youtu.be/PUT_EP02_VIDEO_ID_HERE

📺 Watch Episode 1: What even *is* a "system"? — a request's journey
▶ https://youtu.be/PUT_EP01_VIDEO_ID_HERE

▶ Next episode (Ep04): The full vocabulary of scale — SLA, SLO, "four nines", availability, MTTR — what they really mean.

🔔 Subscribe — we're building this whole thing, one box at a time.
📋 Playlist: System Design from Day One — https://www.youtube.com/playlist?list=PUT_PLAYLIST_ID_HERE
🐦 (optional) X / Twitter — @your_handle
💼 (optional) LinkedIn — your URL

📚 Sources for the on-screen numbers
• Latency / throughput / bandwidth definitions → AWS Well-Architected, Google SRE Book
• p50 / p99 percentile latency → Google SRE Book (ch. 4 "Service Level Objectives"), Gil Tene's "How NOT to measure latency"
• qps and capacity planning → SRE Book, Designing Data-Intensive Applications (Kleppmann, ch. 1)
• Hotstar IPL peak (~32M concurrent streams) → Disney+ Hotstar / JioCinema engineering posts; figures are illustrative for the order of magnitude
• CDN rationale (Hotstar) → Cloudflare Learning, AWS CloudFront docs
• UPI latency SLA (~sub-second) → NPCI UPI technical specifications

🎙 Voice: ElevenLabs (creator's own cloned voice)
🎨 Visuals: HyperFrames + GSAP (HTML/CSS → MP4, deterministic render)

#SystemDesign #Latency #Throughput #LearnInPublic
```

> Replace `PUT_EP01_VIDEO_ID_HERE`, `PUT_EP02_VIDEO_ID_HERE`, and `PUT_PLAYLIST_ID_HERE` after publishing.

---

## 3 · Above-the-title hashtags

YouTube shows the first **3 hashtags** from the description above the title.
The four at the bottom (`#SystemDesign #Latency #Throughput #LearnInPublic`) →
YouTube picks the first three: `#SystemDesign #Latency #Throughput`. That's
exactly the three search rails for this episode.

---

## 4 · Tags (paste into Studio → Tags)

> Tags help recommendations more than search now, but still worth filling.
> Max 500 chars total. Lead with the strongest broad term, then narrower.

```
system design, system design for beginners, system design tutorial, system design explained, latency vs throughput, latency explained, throughput explained, bandwidth explained, what is latency, what is throughput, what is qps, p50 p99 explained, p99 latency, percentile latency, tail latency, queries per second, scalability basics, performance engineering, the tech intern, system design from day one, how scaling works, swiggy system design, hotstar ipl scale, irctc tatkal explained, cdn explained
```

---

## 5 · Thumbnail

Rendered from the **reusable series template** so every episode matches
(constant: SYSTEM DESIGN title + client→server→database flow + brand tag +
the teal/orange series colours; per-episode: only the number + topic line).

**File:** `assets/thumbnails/sd-ep03-latency-throughput.png` (2560×1440, crops to 1280×720)

**Regenerate / tweak:**
```bash
cd tti-studio
export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
node thumbnails/render.mjs --ep "03" --lead "" --main "Latency vs Throughput" \
  --micro "the 3 numbers that rule every system" \
  --out assets/thumbnails/sd-ep03-latency-throughput.png
```

Edit `thumbnails/template.html` to change the look for ALL episodes; see
`thumbnails/README.md`.

> Note: the thumbnail template uses the series' teal/orange palette, while the
> *videos* use the cobalt/navy "Engineer's Terminal" palette. They're internally
> consistent (all thumbnails match each other; all videos match each other) but
> not with each other — worth aligning at some point.

---

## 6 · End screen (last 20 seconds)

YouTube wants 5–20s of "end screen content." Scene 14's recap + cliffhanger
plays from 10:20 → 11:11 (51s) — perfect window. Add **three** end-screen
elements:

| Element | Position | Links to |
|---|---|---|
| **Subscribe ring** | Right side, vertically centered | (auto — your channel) |
| **Video element** — "Watch Episode 2" | Top-left card | Ep02 video URL |
| **Best for viewer** — let YouTube pick | Bottom-left card | (auto: recommended next video for that viewer) |

Set them all to appear from **10:51** (20s before the end) so they're visible
across the recap + cliffhanger.

---

## 7 · Cards (mid-roll prompts)

Strategic cards drive playlist depth + retention. Pick **2–3** of these slots:

| Timestamp | Card type | What | Why here |
|---|---|---|---|
| **0:33** | Video card → Ep02 | "Missed Ep02? Watch DNS & HTTP first." | Catches new viewers during the hook; sends them down the funnel |
| **5:30** | Playlist card → System Design playlist | "All System Design videos" | After "Latency ≠ Throughput" lands — natural exhale moment |
| **9:00** | Video card → Ep04 (when published) | "Next: SLAs, four nines, the vocabulary of scale" | Right before the recap — keeps people watching |

---

## 8 · Pinned comment (post immediately on publish)

> Pinning a comment within 5 min of publish is a known retention trick — it
> reads like a host's note and earns its own reply tree, which YouTube treats
> as engagement signal.

```
Quick check before next episode 👇

Your dashboard says: p50 = 40ms, p99 = 2200ms, qps = 10,000. How many users per second are having a bad time?

Drop your answer in one line — first 5 correct ones get a 💙

Next ep: SLAs, "four nines", and the vocabulary of scale.
```

(Answer: 1% of 10,000 = **100 users every second** — the "p99 tail" from Scene 10.)

---

## 9 · Community post (publish 1 hour before / on upload)

> Free reach to your subscribers. Post once when the video goes live.

```
new episode is up 🎉

"the app is slow" — three completely different things hiding inside one complaint.

latency. throughput. bandwidth.

three numbers, three different fixes, and mixing them up is how engineers spend a weekend firefighting the wrong thing.

with kitchens, Western Express Highway traffic, and an IRCTC Tatkal cameo 🚆

watch → [link]
```

Attach the thumbnail as the image.

---

## 10 · Shorts derivatives (cut after the long-form goes live)

Per `docs/CURRICULUM.md` we ship 3–5 shorts per long-form. Three strong cuts
from this episode (each ≤60s, 9:16, captions burned-in):

| Short | Source segment | Hook | Cut |
|---|---|---|---|
| **`ep03-short-1: Latency ≠ Throughput in 60s`** | 4:51–5:52 (Scene 8) | "These two words aren't opposites — and confusing them costs engineers weekends." | Western Express Highway 8pm vs 3am split-screen, end on the IRCTC Tatkal line |
| **`ep03-short-2: Why p99 matters more than the average`** | 6:56–7:45 (Scene 10) | "Your average latency is lying to you." | Distribution curve draws on, mean line drops in, then the p99 tail in red — "those are real customers" |
| **`ep03-short-3: 32 million people watching IPL — the bandwidth maths`** | 8:30–9:11 (Scene 12) | "How does Hotstar serve 32 million people at once? The maths is wild." | 32M × 4 Mbps = 128 Tbps reveal, end on the CDN tease |

Optional 4th: **The kitchen analogy** (3:26–4:11 — "cook speed = latency, number of cooks = throughput, kitchen size = bandwidth"). Anchors the whole season.

---

## 11 · Premiere strategy

| Option | When to use |
|---|---|
| **Standard upload** | Default. Best for replay/SEO; viewers find via search/recommendations |
| **Premiere** (recommended for Ep03) | Lets you build a 2-min countdown + live chat. Schedule for Sunday 8pm IST (your audience is online + the episode opens with "It's 8pm…" — meta is good) and tease in a Community post 6 hours earlier |

---

## 12 · YouTube Studio fields (the easy-to-forget ones)

- **Category:** Education *(not Science & Technology — Education trends higher for explainer content)*
- **Audience:** "No, it's not made for kids"
- **Age restriction:** None
- **Recording location:** (skip)
- **Video language:** English (India)
- **Caption certification:** "Captions provided" (since `script.srt` ships with the upload)
- **License:** Standard YouTube License
- **Allow embedding:** Yes
- **Publish to subscriptions feed and notify subscribers:** Yes
- **Shorts remixing:** Allow video and audio remixing *(helps the algorithm)*
- **Category for monetization:** "Standard content" (once monetized)

---

## 13 · SEO / cross-promotion checklist (post-publish)

- [ ] Add to the **System Design** playlist (position 3)
- [ ] Update the channel **About** page with the latest episode link
- [ ] Update Ep02's description to link out to Ep03 ("▶ Episode 3 is now live: …")
- [ ] Update Ep02's end-screen "Next" card to point to Ep03
- [ ] Post a 1280×720 still (the thumbnail) on X / LinkedIn with the title + URL
- [ ] If you have a newsletter, link it in the next issue
- [ ] After 24h: scan the comments for misconceptions to fix in a pinned reply / Ep04 intro
- [ ] After 7d: check Studio → Analytics → Audience retention. Look for drop-offs around Scene 9 (p50/p99/qps) — if steep, the Short re-cut needs a sharper hook

---

## 14 · A/B levers if Ep03 underperforms in week 1

If CTR < 4% at 24h:
- Swap to **Title #2** (the "it's slow means 3 things" pain-point version)
- Swap to a thumbnail variant that leads with the **8pm Swiggy hook** instead of the metric stack

If average view duration < 50%:
- Likely intro friction at Scene 1–2. Re-cut a 0:00–0:30 cold-open ("Why 'it's slow' means 3 different things") and re-upload as a Short cross-link.
- Or: the p50/p99 section (Scene 9, 5:52) is the technical density spike — consider a more visual re-cut for that segment in the next iteration.

---

*This file is the canonical YouTube package for Ep03. Edit it as you learn from
the upload. The next episode's `youtube.md` should copy this structure verbatim
and only change the content.*
