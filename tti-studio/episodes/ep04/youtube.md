# Ep04 — YouTube upload package

> Everything you need to ship the video. Sections are upload-order so you can
> paste them straight into YouTube Studio top to bottom.

---

## TL;DR for the upload form

| Field | Value |
|---|---|
| **Title** | Scale Vocabulary: qps, p50/p99, and "Nines" of Availability (System Design #4) |
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
| **Captions** | Upload `script.srt` (word-synced, generated from `audio_v2/*.align.json`) |
| **Thumbnail** | `assets/thumbnails/sd-ep04-scale-vocabulary.png` (rendered from the series template — see §5) |
| **Video file** | `episodes/ep04/video-voiced.mp4` (1920×1080 · 24fps · 8:19 · ~67 MB) |

---

## 1 · Title options (pick one)

| # | Title (≤60 chars body, then a tag) | Why |
|---|---|---|
| **1 ⭐** | **Scale Vocabulary: qps, p50/p99, and "Nines" of Availability (System Design #4)** | Direct keyword stack (qps, p99, nines, availability) + series tag. **Use this one.** |
| 2 | Why "99.9% Uptime" Is a Lie You Should Worry About — the Vocabulary of Scale | Curiosity/pain-point opener leaning on the downtime-math reveal; strong for re-cuts and Shorts. |
| 3 | qps, Headroom, and the "Nines" — How Engineers Actually Read a Dashboard | Insider/jargon-curious title targeting devs already searching "qps" or "SLA vs SLO". |

**Title-A/B tip:** Run #1 vs #2 for the first 2–4 weeks in Studio → Test & Compare; keep whichever wins on CTR.

---

## 2 · Description

> Paste the whole block below into the **Description** field. The first ~2 lines
> are what shows above "…more" on watch pages and in search.

```
Somewhere in Bangalore, a Swiggy engineer is staring at a dashboard full of numbers — qps, latency, uptime percentages. To you and me, that's noise. To them, it's the entire health of the system, at a glance.

This episode gives you that same fluency. It builds directly on Episode 3's latency/throughput/bandwidth — no re-teaching, only new vocabulary layered on top.

In Episode 4 of The Tech Intern · System Design, we go one level deeper into how engineers actually talk about scale: the difference between concurrent users and qps, what "headroom" means before a system breaks, and the third number nobody explains properly — "nines" of availability, and what they really cost in minutes of downtime a year.

You'll walk away knowing (every term explained on first use, no jargon left dangling):
✦ Why "a lakh users online" and "a lakh requests per second" are NOT the same thing (think time, explained)
✦ Headroom — how close a system is to its ceiling, and why that matters more than the raw qps number
✦ What happens when you cross the ceiling: queues form, milliseconds become seconds
✦ "Nines" of availability — 99%, 99.9%, 99.99%, 99.999% — and why each one sounds like a rounding error but isn't
✦ The downtime-budget math: 99% = 3.65 days down a year. 99.999% = 5 minutes. Each nine is roughly a 10× cut.
✦ Why UPI can't run on fewer nines — money stuck mid-transfer isn't a rounding error, it's a national story
✦ Why chasing the last nine is often the single most expensive engineering work a company ever does
✦ SLA vs SLO vs SLI — the promise, the internal target, and the real-time measurement, finally untangled
✦ Reading a live dashboard end to end: qps for the load, p50/p99 for the feel, nines for the promise being kept
✦ Diagnosing the 8pm Swiggy rush in real time — using nothing but this vocabulary
✦ The trade-off: more nines isn't free, and isn't always worth it (internal tool vs payment rail)

Indian, everyday examples first. Every term explained on first use. No CS degree assumed.

⏱ Chapters
0:00 The dashboard nobody can read
0:29 A number alone lies
0:49 Quick callback — qps, p50, p99
1:15 Concurrent users ≠ qps
2:08 Headroom — how close to the edge
2:43 Introducing "nines"
3:06 The downtime-budget math
3:56 Why UPI can't afford fewer nines
4:48 Why each nine costs exponentially more
5:21 SLA, SLO, SLI
6:05 Reading the dashboard now
6:37 The 8pm spike, diagnosed
7:15 The cost of chasing more nines
7:37 Recap — qps, p50/p99, nines
7:57 Next up: the load balancer

📺 Watch Episode 3: Latency vs Throughput vs Bandwidth
▶ https://youtu.be/PUT_EP03_VIDEO_ID_HERE

📺 Watch Episode 2: How your phone *finds* the server — DNS & HTTP
▶ https://youtu.be/PUT_EP02_VIDEO_ID_HERE

▶ Next episode (Ep05): Scaling up vs out, and load balancers — the waiter who picks the kitchen.

🔔 Subscribe — we're building this whole thing, one box at a time.
📋 Playlist: System Design from Day One — https://www.youtube.com/playlist?list=PUT_PLAYLIST_ID_HERE
🐦 (optional) X / Twitter — @your_handle
💼 (optional) LinkedIn — your URL

📚 Sources for the on-screen numbers
• qps / p50 / p99 definitions → Google SRE Book (ch. 4, "Service Level Objectives"); Gil Tene's "How NOT to measure latency"
• Availability "nines" + downtime-budget math → standard uptime-percentage-to-downtime conversion (99%→3.65d/yr, 99.9%→8.76h/yr, 99.99%→52min/yr, 99.999%→5min/yr); Google SRE Book ch. 4
• SLA / SLO / SLI definitions → Google SRE Book ch. 4
• UPI / NPCI mandated uptime figure → ⚠️ VERIFY before publish — this episode states NPCI mandates 99.99% uptime for member banks; confirm against NPCI's current operating circulars / UPI procedural guidelines before this claim goes live, and cite the specific circular here once confirmed.

🎙 Voice: ElevenLabs (creator's own cloned voice)
🎨 Visuals: HyperFrames + GSAP (HTML/CSS → MP4, deterministic render)

#SystemDesign #Availability #SRE
```

> Replace `PUT_EP02_VIDEO_ID_HERE`, `PUT_EP03_VIDEO_ID_HERE`, and `PUT_PLAYLIST_ID_HERE` after publishing.
> ⚠️ **Do not publish until the UPI/NPCI uptime figure is verified** — see Sources note above.

---

## 3 · Above-the-title hashtags

YouTube shows the first **3 hashtags** from the description above the title:
`#SystemDesign #Availability #SRE` — the three search rails for this episode.

---

## 4 · Tags (paste into Studio → Tags)

> Max 500 chars total. Lead with the strongest broad term, then narrower.

```
system design, system design for beginners, system design tutorial, system design explained, qps explained, what is qps, p50 p99 explained, percentile latency, availability nines, what is 99.99 uptime, sla vs slo vs sli, service level agreement explained, service level objective, downtime budget, uptime percentage explained, five nines, four nines availability, headroom capacity planning, concurrent users vs qps, upi uptime, the tech intern, system design from day one, sre concepts, google sre book explained
```

---

## 5 · Thumbnail

Bespoke per-episode file (same reusable series skin as Ep01–03: dark navy bg +
grid + glows, EPISODE badge, corner brackets, teal/orange palette). Right-side
diagram depicts this episode's own three-number structure — QPS → P50/P99 →
NINES — the same "three metric cards" pattern Ep03 used for latency/throughput/bandwidth.

**File:** `assets/thumbnails/sd-ep04-scale-vocabulary.png` (2560×1440, crops to 1280×720)
**Source:** `thumbnails/ep04.html`

**Re-render / tweak:**
```bash
cd tti-studio
export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
node thumbnails/render.mjs --file thumbnails/ep04.html \
  --out assets/thumbnails/sd-ep04-scale-vocabulary.png
```

---

## 6 · End screen (last 20 seconds)

Scene 15's cliffhanger plays from **7:57 → 8:19** (22s) — the whole window.
Add three end-screen elements, all appearing from **7:59** (20s before the end):

| Element | Position | Links to |
|---|---|---|
| **Subscribe ring** | Right side, vertically centered | (auto — your channel) |
| **Video element** — "Watch Episode 3" | Top-left card | Ep03 video URL |
| **Best for viewer** — let YouTube pick | Bottom-left card | (auto: recommended next video) |

---

## 7 · Cards (mid-roll prompts)

| Timestamp | Card type | What | Why here |
|---|---|---|---|
| **0:49** | Video card → Ep03 | "New here? Watch Latency vs Throughput first." | Catches new viewers right as the callback scene starts |
| **3:56** | Playlist card → System Design playlist | "All System Design videos" | Right after the downtime-math payoff — natural pause point |
| **6:37** | Video card → Ep05 (when published) | "Next: the load balancer" | Right before the diagnosis payoff scene — keeps people watching |

---

## 8 · Pinned comment (post immediately on publish)

```
Quick check before next episode 👇

Your system runs at 99.9% uptime. How many MINUTES of downtime does that allow in a year? (Not days — minutes.)

Drop your answer below — first 5 correct ones get a 💙

Next ep: scaling up vs out, and the load balancer — the waiter who picks the kitchen.
```

(Answer: 99.9% = 8.76 hours/year = **~526 minutes** — the downtime-budget math from this episode.)

---

## 9 · Community post (publish 1 hour before / on upload)

```
new episode is up 🎉

"99.9% uptime" sounds great. Until you do the math: that's still 8.76 hours of downtime a year.

qps. p50/p99. and the number nobody explains properly — "nines."

this one gives you the exact vocabulary an engineer uses to read a dashboard in 5 seconds flat.

with a UPI cameo on why some systems can't afford to round off a nine 💳

watch → [link]
```

Attach the thumbnail as the image (once rendered — see §5).

---

## 10 · Shorts derivatives

The recap Short is already built: `episodes/ep04/short/short.mp4` (92.9s,
vertical 9:16) — covers the full episode: dashboard hook → qps/p50/p99 recap
→ concurrent-users-vs-qps mistake → headroom → nines + downtime math → UPI →
trade-off → recap + cliffhanger.

Two additional focused cuts worth making from the long-form, per `docs/CURRICULUM.md`'s
3–5-shorts-per-episode target:

| Short | Source segment | Hook | Cut |
|---|---|---|---|
| **`ep04-short-2: The downtime math nobody does`** | 3:06–3:56 (Scene 7) | "99.9% uptime sounds great. Here's what it actually costs you." | The four rows building one at a time, ending on "5 minutes a year" |
| **`ep04-short-3: Why UPI can't afford fewer nines`** | 3:56–4:48 (Scene 8) | "Why can't UPI just run at 99%? The answer is scarier than you think." | The money-icon travel + the "national story" line |

---

## 11 · Premiere strategy

| Option | When to use |
|---|---|
| **Standard upload** | Default. Best for replay/SEO. |
| **Premiere** | Schedule for the same day/time slot as Ep03 for consistency; tease in a Community post a few hours earlier. |

---

## 12 · YouTube Studio fields (the easy-to-forget ones)

- **Category:** Education
- **Audience:** "No, it's not made for kids"
- **Age restriction:** None
- **Video language:** English (India)
- **Caption certification:** "Captions provided" (`script.srt` ships with the upload)
- **License:** Standard YouTube License
- **Allow embedding:** Yes
- **Publish to subscriptions feed and notify subscribers:** Yes
- **Shorts remixing:** Allow video and audio remixing

---

## 13 · SEO / cross-promotion checklist (post-publish)

- [ ] Add to the **System Design** playlist (position 4)
- [ ] Update the channel **About** page with the latest episode link
- [ ] Update Ep03's description to link out to Ep04 ("▶ Episode 4 is now live: …")
- [ ] Update Ep03's end-screen "Next" card to point to Ep04
- [ ] Post the thumbnail (once rendered) on X / LinkedIn with the title + URL
- [ ] After 24h: scan comments for misconceptions to fix in a pinned reply / Ep05 intro
- [ ] After 7d: check Studio → Analytics → Audience retention for drop-offs around Scene 9–10 (the cost-curve / SLA-SLO-SLI stretch, the densest part) — if steep, that segment needs a sharper Short re-cut

---

## 14 · A/B levers if Ep04 underperforms in week 1

If CTR < 4% at 24h:
- Swap to **Title #2** (the "99.9% uptime is a lie" pain-point version)
- Try a thumbnail variant leading with the dashboard hook instead of the nines/qps keyword stack

If average view duration < 50%:
- Likely friction around Scene 9 (why nines cost exponentially more) or Scene 10 (SLA/SLO/SLI) — the most abstract stretch in the episode. Consider a sharper visual re-cut for that segment.
- The Scene 12 "8pm spike, diagnosed" payoff (6:37) is the strongest retention beat — if drop-off happens before it, consider moving a taste of it earlier as a cold-open.

---

*This file is the canonical YouTube package for Ep04. Ep03's `youtube.md` was
the template; the next episode's `youtube.md` should copy this structure
verbatim and only change the content.*
