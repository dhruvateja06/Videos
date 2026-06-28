# Ep02 — YouTube upload package

> Everything you need to ship the video. Sections are upload-order so you can
> paste them straight into YouTube Studio top to bottom.

---

## TL;DR for the upload form

| Field | Value |
|---|---|
| **Title** | How Your Phone *Finds* the Server — DNS & HTTP, Explained Visually (System Design #2) |
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
| **Captions** | Upload `script.srt` (already word-synced to narration) |
| **Thumbnail** | `assets/thumbnails/sd-ep02-dns-http.png` (rendered from the series template — see §5) |

---

## 1 · Title options (pick one)

| # | Title (≤60 chars body, then a tag) | Why |
|---|---|---|
| **1 ⭐** | **How Your Phone *Finds* the Server — DNS & HTTP, Explained Visually (System Design #2)** | Curiosity hook + the two keywords beginners search ("DNS explained" / "HTTP explained") + series tag for binge-watch. **Use this one.** |
| 2 | What Happens When You Tap a Restaurant on Swiggy? — DNS, HTTP & the Whole Journey | Strong India-specific hook; better for the *Shorts* re-cut than the long-form. |
| 3 | Client vs Server, DNS & HTTP — System Design from Day One (Ep 02) | Title-first, hook-second. Less click-y, more SEO-stable; A/B fallback. |

**Title-A/B tip:** YouTube lets you test titles per video now (Studio → Test & Compare). Run #1 vs #3 for the first 4 weeks; whichever wins on CTR, keep.

---

## 2 · Description

> Paste the whole block below into the **Description** field. The first ~2 lines
> are what shows above "…more" on watch pages and in search.

```
You tap a restaurant on Swiggy. In a fraction of a second, your phone finds the right server out of billions on the internet and starts a conversation with it.

This is how that works — DNS and HTTP, explained visually, by way of a restaurant.

In Episode 2 of The Tech Intern · System Design, we crack open the "client" and "server" boxes from Ep01 and watch them actually talk. The whole episode runs on one analogy: a restaurant. The dining room is the client. The kitchen is the server. The waiter is the API. And every tap you make plays out across that picture.

You'll walk away understanding (every acronym spelled out, no jargon left dangling):
✦ What the client (frontend) and server (backend) really do — and why your data lives only on the server
✦ The golden rule of system design: never trust the client (and why hacked "pay Rs 1" attacks fail)
✦ API (Application Programming Interface) as the waiter — one backend serving many apps (iOS, Android, web)
✦ CSR vs SSR (Client-Side / Server-Side Rendering) — who actually draws the page, and the trade-off
✦ IP (Internet Protocol) addresses as a server's "phone number" (IPv4 vs IPv6)
✦ DNS (Domain Name System) — the internet's phonebook
✦ The DNS relay: device → resolver → root → TLD → authoritative
✦ DNS caching + TTL (Time To Live) — the speed-vs-freshness trade-off
✦ HTTP (HyperText Transfer Protocol) — the shared language of request and response
✦ Anatomy of a request: method, path, headers, body — and a URL (Uniform Resource Locator) broken down
✦ GET vs POST — reads vs writes, and why double-tapping POST can place two orders
✦ Cookies — your ID badge, how HTTP "forgets" but the app remembers you
✦ Status codes: 200, 301, 404, 500 (and the "4xx = your fault, 5xx = server's fault" rule)
✦ HTTPS (HTTP Secure) — the sealed envelope, what the padlock actually means (and what it doesn't)

Indian, everyday examples first. Every term explained on first use. No CS degree assumed.

⏱ Chapters
0:00 Welcome back · the missing piece from Ep 01
0:43 It comes down to two questions
1:02 The restaurant — the analogy for the whole episode
1:33 The client — your phone, the dining room
2:02 The server — the kitchen
2:29 Where your data actually lives
2:56 The golden rule: never trust the client
3:25 The API (Application Programming Interface)
4:08 CSR vs SSR — who draws the page?
4:49 Billions of computers, one name
5:10 IP address (Internet Protocol)
5:43 DNS — the Domain Name System
6:14 The DNS relay (resolver → root → TLD → authoritative)
6:56 DNS cache + TTL (Time To Live)
7:42 HTTP (HyperText Transfer Protocol)
8:25 Anatomy of a request + URL
9:00 GET vs POST — read vs write
9:35 Cookies — your ID badge
10:09 Status codes — 200, 301, 404, 500
10:42 The S in HTTPS — sealed envelope
11:18 The whole journey, end to end
11:46 Recap + what's next

📺 Watch Episode 1: What even *is* a "system"? — a request's journey
▶ https://youtu.be/PUT_EP01_VIDEO_ID_HERE

▶ Next episode: All this travelling takes *time*. So how do we measure "fast"? Latency vs throughput.

🔔 Subscribe — we're building this whole thing, one box at a time.
📋 Playlist: System Design from Day One — https://www.youtube.com/playlist?list=PUT_PLAYLIST_ID_HERE
🐦 (optional) X / Twitter — @your_handle
💼 (optional) LinkedIn — your URL

📚 Sources for the on-screen facts
• DNS resolution chain → MDN, Cloudflare Learning, AWS Route 53 docs
• HTTP methods, idempotency/safety, URL anatomy, headers/cookies, status codes → MDN Web Docs
• TLS / HTTPS encryption (high level) → Cloudflare Learning, MDN
• Client/server split, "never trust the client" → MDN, OWASP Input Validation Cheat Sheet
• CSR vs SSR trade-offs → web.dev / MDN-aligned guidance

🎙 Voice: ElevenLabs (creator's own cloned voice)
🎨 Visuals: HyperFrames + GSAP (HTML/CSS → MP4, deterministic render)

#SystemDesign #DNS #HTTP #LearnInPublic
```

> Replace `PUT_EP01_VIDEO_ID_HERE` and `PUT_PLAYLIST_ID_HERE` after publishing.

---

## 3 · Above-the-title hashtags

YouTube shows the first **3 hashtags** from the description above the title.
The three I put at the very bottom (#SystemDesign #DNS #HTTP #LearnInPublic) →
YouTube picks the first three: `#SystemDesign #DNS #HTTP`. That's exactly the
three search/discovery rails we want.

---

## 4 · Tags (paste into Studio → Tags)

> Tags help recommendations more than search now, but still worth filling.
> Max 500 chars total. Lead with the strongest broad term, then narrower.

```
system design, system design for beginners, system design tutorial, system design explained, dns explained, http explained, https explained, what is dns, what is http, how does dns work, how http works, client server architecture, client vs server, frontend vs backend, what is api, api explained, http get vs post, http status codes, 404 vs 500, cookies and sessions, csr vs ssr, ip address explained, the tech intern, system design from day one, how the internet works, beginner system design, dns lookup, tcp ip basics
```

---

## 5 · Thumbnail

Rendered from the **reusable series template** so every episode matches
(constant: SYSTEM DESIGN title + client→server→database flow + brand tag +
the teal/orange series colours; per-episode: only the number + topic line).

**File:** `assets/thumbnails/sd-ep02-dns-http.png` (2560×1440, crops to 1280×720)

**Regenerate / tweak:**
```bash
cd tti-studio
export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
node thumbnails/render.mjs --ep "02" --lead "" --main "DNS & HTTP" \
  --micro "how your phone finds the server" \
  --out assets/thumbnails/sd-ep02-dns-http.png
```

Edit `thumbnails/template.html` to change the look for ALL episodes; see
`thumbnails/README.md`.

> Note: the thumbnail template uses the series' teal/orange palette, while the
> *videos* use the cobalt/navy "Engineer's Terminal" palette. They're internally
> consistent (all thumbnails match each other; all videos match each other) but
> not with each other — worth aligning at some point.


## 6 · End screen (last 20 seconds)

YouTube wants 5–20s of "end screen content." Scene 22's recap + cliffhanger
already plays from 11:46 → 12:26 (40s) — perfect window. Add **three** end
screen elements:

| Element | Position | Links to |
|---|---|---|
| **Subscribe ring** | Right side, vertically centered | (auto — your channel) |
| **Video element** — "Watch Episode 1" | Top-left card | Ep01 video URL |
| **Best for viewer** — let YouTube pick | Bottom-left card | (auto: recommended next video for that viewer) |

Set them all to appear from **12:06** (20s before the end) so they're visible
across the recap + cliffhanger.

---

## 7 · Cards (mid-roll prompts)

Strategic cards drive playlist depth + retention. Pick **2–3** of these slots:

| Timestamp | Card type | What | Why here |
|---|---|---|---|
| **0:38** | Video card → Ep01 | "Missed Episode 1? Start there." | Catches new viewers in the welcome; sends them down the funnel |
| **5:30** | Playlist card → System Design playlist | "All System Design videos" | After "DNS is the phonebook" — natural pause |
| **9:58** | Video card → Ep03 (when published) | "What's coming next: latency vs throughput" | Right before the HTTPS act — keeps people watching |

---

## 8 · Pinned comment (post immediately on publish)

> Pinning a comment within 5 min of publish is a known retention trick — it
> reads like a host's note and earns its own reply tree, which YouTube treats
> as engagement signal.

```
Quick check before next episode 👇

What's the difference between a 404 and a 500? Drop your answer in one line — first 5 correct ones get a 💙

Next ep: why "fast" is two different numbers — latency vs throughput.
```

---

## 9 · Community post (publish 1 hour before / on upload)

> Free reach to your subscribers. Post once when the video goes live.

```
new episode is up 🎉

How does your phone find the right server out of billions on the internet?

It's two invisible helpers — DNS and HTTP — and the whole thing makes a lot more sense once you picture a restaurant 🍽

every acronym actually spelled out this time (DNS, HTTP, TTL, API, the works). no jargon left dangling.

watch → [link]
```

Attach the thumbnail as the image.

---

## 10 · Shorts derivatives (cut after the long-form goes live)

Per `docs/CURRICULUM.md` we ship 3–5 shorts per long-form. Three strong cuts
from this episode (each ≤60s, 9:16, captions burned-in):

| Short | Source segment | Hook | Cut |
|---|---|---|---|
| **`ep02-short-1: DNS in 60s`** | 5:43–6:46 | "DNS in 60 seconds — finally clear." | Open with the phonebook visual, cut to the relay race, end on "you remember the name, DNS remembers the number" |
| **`ep02-short-2: The 404 vs 500 trick`** | 10:09–10:42 | "If you don't know the difference between a 404 and a 500, watch this." | The traffic light visual + the "4xx = your fault, 5xx = the server's fault" line |
| **`ep02-short-3: Never trust the client`** | 2:56–3:24 | "Why you can't actually pay Rs 1 for a Rs 299 order." | The hacked-app → server-rejects → real price flow, ending on "the kitchen has the final say" |

Optional 4th: **Padlock myth** (10:42–11:18 — "the padlock means encrypted, not honest").

---

## 11 · Premiere strategy

| Option | When to use |
|---|---|
| **Standard upload** | Default. Best for replay/SEO; viewers find via search/recommendations |
| **Premiere** (recommended for Ep02) | Lets you build a 2-min countdown + live chat. Schedule for Sunday 8pm IST (your audience is online + bored) and tease in a Community post 6 hours earlier |

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

- [ ] Add to the **System Design** playlist
- [ ] Update the channel **About** page with the latest episode link
- [ ] Update Ep01's description to link out to Ep02 ("▶ Episode 2 is now live: …")
- [ ] Post a 1280×720 still (the thumbnail) on X / LinkedIn with the title + URL
- [ ] If you have a newsletter, link it in the next issue
- [ ] After 24h: scan the comments for misconceptions to fix in a pinned reply / Ep03 intro

---

## 14 · A/B levers if Ep02 underperforms in week 1

If CTR < 4% at 24h:
- Swap to **Title #3** (the SEO-stable one)
- Swap to **Thumbnail variant 2** (the "tap → ?" hook)

If average view duration < 50%:
- Likely intro friction. Re-cut a 0:00–0:30 cold-open and re-upload as a Short cross-link.

---

*This file is the canonical YouTube package for Ep02. Edit it as you learn from
the upload. The next episode's `youtube.md` should copy this structure verbatim
and only change the content.*
