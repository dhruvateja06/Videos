# Ep03 — Latency vs Throughput vs Bandwidth: the numbers that rule everything
## Narration Script · ~145 wpm · ~10–11 min

> **▸** = visual reveal cue. One reveal per marker.
> Read aloud before finalising — if you pause at a comma, the voice will too.

---

## Scene 1 — The 8pm crush (HOOK) · ~40s

It's 8pm on a Friday, and half of Mumbai just opened Swiggy at the same time.

▸ *[clock hits 8pm]*

You tap "order." So does a lakh of other people — right now, simultaneously.

▸ *[phones flood toward server]*

And somewhere in a data centre, one poor server starts sweating.

▸ *[server goes red]*

The app slows down, some orders fail — and every engineer on call gets a message that just says "it's down."

▸ *[order counter spikes]*

But here's the thing — "it's slow" or "it's down" doesn't actually tell you what broke, because slowness has three completely different causes, and you need to know which one you're dealing with.

---

## Scene 2 — Three different problems · ~38s

When an engineer says "the system's struggling," they're really asking one of three questions.

▸ *[card 1 appears: "How long does ONE order take?"]*

How long does a single order take, end to end?

▸ *[card 2 appears: "How many orders per second?"]*

How many orders can we handle per second?

▸ *[card 3 appears: "How wide is the pipe?"]*

And how much data can we actually move at once?

Three different questions, three different problems, three different fixes — and mixing them up is how you spend a weekend firefighting the wrong thing.

---

## Scene 3 — Latency (HERO) · ~52s

Let's start with the first one — latency, which just means how long one single request takes.

▸ *[CLIENT box appears]*

You tap "order" on your phone — that's the client, the thing making the request.

▸ *[SERVER box appears]*

The request travels to Swiggy's server — maybe 12 milliseconds over the network.

▸ *[DATABASE cylinder appears]*

The server needs to check the restaurant, fetch your address, calculate the delivery fee — so it hits the database, and that query takes around 40 milliseconds.

▸ *[packet travels, +12ms, +40ms hop annotations appear]*

Then the answer comes back — another 8 milliseconds to process, 5 milliseconds back to your phone.

▸ *[+8ms, +5ms, total = 65ms appears]*

Total: 65 milliseconds. That's latency — the time for one round trip, door to door.

When latency is low, the app feels instant. When it's high, you sit there watching a spinner wondering if your order went through.

---

## Scene 4 — What makes latency go up · ~48s

So what makes latency go up?

There are three main culprits, and they show up in almost every slowness investigation.

▸ *[network distance card appears]*

First: physical distance. If you're ordering from Leh and the server is in Mumbai, the signal is literally travelling hundreds of kilometres through cables — that adds latency you cannot code your way out of, because physics has a speed limit.

▸ *[server processing card appears]*

Second: server processing. If your order triggers ten different calculations — discount codes, surge pricing, restaurant availability — each one adds time before the server can even reply.

▸ *[database bottleneck card appears]*

And third — almost always the sneaky one — the database. A query without the right index doesn't find one row, it scans every single row in the table. On a big table, that's catastrophic.

Distance is physics, processing is code, but the database is usually where the real time goes.

---

## Scene 5 — Throughput (HERO) · ~48s

Now latency answers "how long does one request take?" — but that's only half the picture.

The other question is: how many requests can we handle at the same time?

That's throughput.

▸ *[single pipe, 1 qps]*

Imagine a pipe. One order travels through it per second — one qps, "queries per second," which is the unit engineers use.

▸ *[wider pipe, 100 qps]*

Now imagine we make the pipe wider — or better, add more pipes side by side. Now a hundred orders a second can flow through.

▸ *[even wider pipe, 10,000 qps]*

And a well-engineered system at scale might handle ten thousand qps or more.

▸ *[counter ticks up]*

Throughput isn't about making one request faster — it's about how many requests you can serve simultaneously before the system starts refusing or slowing down.

---

## Scene 6 — The kitchen analogy · ~43s

Here's the analogy that makes this stick, and we'll keep coming back to it all season.

▸ *[single cook, 1 qps label]*

Imagine a kitchen with one cook. That cook can make one dish at a time — one order per minute, let's say. That's your throughput: one qps.

▸ *[four cooks appear, 4 qps label]*

Now you hire four cooks. Each one still takes the same amount of time per dish — the latency per order hasn't changed — but now you're serving four orders simultaneously. Throughput just quadrupled.

▸ *[bandwidth label: "same kitchen size = same bandwidth"]*

But the kitchen itself — the physical space, the number of burners, the gas supply — that's bandwidth. You can add more cooks, but if the kitchen is full, you're stuck.

Each cook's speed is latency. The number of cooks is throughput. The kitchen size is bandwidth.

---

## Scene 7 — Bandwidth · ~43s

So: bandwidth — the width of the pipe.

▸ *[narrow pipe: "Jio 4G · 25 Mbps"]*

If you're on a standard Jio connection, you've got maybe 25 megabits per second of bandwidth. A text-based order request — a few kilobytes — flies through with room to spare.

▸ *[wide pipe: "YouTube 4K stream · 15 Mbps per viewer"]*

But a 4K YouTube stream needs around 15 megabits per second, just for one video. And your connection is 25. So if two people in your house are streaming 4K, you've hit the ceiling — and everything else slows to a crawl.

▸ *[math annotation: "32M viewers × 15 Mbps"]*

Scale that up: 32 million people streaming the IPL final simultaneously, each needing 15 megabits — that's 480 terabits per second of bandwidth that has to exist somewhere in the world.

Bandwidth is the physical ceiling. You can be fast and efficient, but if the pipe isn't wide enough, none of it matters.

---

## Scene 8 — Latency ≠ Throughput (HERO) · ~53s

Here's where a lot of people trip up — and it's worth being really clear about this.

Latency and throughput are independent. You can have high throughput and high latency at the same time. They're not opposites.

▸ *[left panel: highway at 8pm, many cars but slow]*

Think about the Western Express Highway on a Friday at 8pm. Thousands of cars are on the road — that's high throughput, a lot of vehicles moving through. But each car is stuck in traffic — high latency, because it takes an hour to travel ten kilometres.

▸ *[HIGH THROUGHPUT / HIGH LATENCY label]*

Many requests being handled, but each one taking forever. That's not a contradiction — that's congestion.

▸ *[right panel: empty road at 3am, one car flying]*

Now picture the same highway at 3am. One car, no traffic, doing a hundred and twenty — low latency, you're flying. But only one car is moving — very low throughput.

▸ *[LOW THROUGHPUT / LOW LATENCY label]*

This is exactly what IRCTC looks like at 10am on Tatkal booking day — thousands of requests hammering the server simultaneously, each one taking twenty seconds to get a response. High load, terrible latency, and the system eventually buckles.

▸ *[.sub note appears]*

Understanding which one is your problem completely changes what you do next.

---

## Scene 9 — p50, p99, qps · ~48s

Okay, so how do engineers actually measure this stuff in the real world?

Three numbers come up constantly, and once you know them, you'll spot them everywhere.

▸ *[qps card: "12,000 qps"]*

First: qps — queries per second. How many requests is the system handling right now? 12,000 qps means 12,000 orders every second. That's the throughput number, the live pulse of the system.

▸ *[p50 card: "p50 · 45 ms"]*

Second: p50 latency, the 50th percentile. Half your users got a response faster than this, half slower. If p50 is 45 milliseconds, the typical experience is pretty snappy.

▸ *[p99 card: "p99 · 820 ms"]*

Third — and this is the one engineers actually care about most — p99 latency. One percent of requests took this long or longer. If p99 is 820 milliseconds, that's one in every hundred users sitting there for nearly a second.

On a system doing 12,000 qps, that's 120 people every single second having a bad experience.

---

## Scene 10 — Why p99 matters more than average (HERO) · ~43s

Here's why p99 matters more than the average — and why the average is actually a bit of a liar.

▸ *[distribution curve draws on, bulk in cobalt]*

Imagine you plot every request's response time as a curve. Most requests are fast — that's the big hump in the middle.

▸ *[mean line appears: "mean: 52ms"]*

The average, or mean, sits somewhere in that hump. 52 milliseconds — looks great, right?

▸ *[p99 line appears: "p99: 820ms"]*

But there's a long tail to the right, where a small fraction of requests took much longer. p99 is out here at 820 milliseconds.

▸ *[tail highlights red, "these are real customers"]*

That tail isn't a statistical artefact — those are real users, real people, and they're the ones who leave the one-star reviews and tweet at your support account.

If you only watch the average, the tail is completely invisible to you. p99 is how you see it.

---

## Scene 11 — The food-rush spike · ~48s

Let's go back to our 8pm Swiggy rush, because now you have the vocabulary to understand exactly what's happening.

▸ *[sparkline draws — flat, then spiking]*

Here's the traffic pattern over the day — flat in the morning, picking up at lunch, then at 8pm it spikes hard.

▸ *[throughput ceiling line: "5,000 qps"]*

The system's throughput ceiling — the maximum it can handle — is 5,000 qps. That's a line. The spike crosses it.

▸ *[queue column builds]*

When demand exceeds throughput, requests don't disappear — they wait. A queue forms. Orders are stacking up, each one sitting in line before the system even starts processing it.

▸ *[p99 latency counter spikes: "45ms → 8,200ms"]*

And watch what happens to p99 latency as that queue grows — it goes from a healthy 45 milliseconds all the way to over 8 seconds. The kitchen didn't get slower. There are just more orders than it can cook.

This is what congestion actually looks like under the hood.

---

## Scene 12 — Bandwidth: Hotstar IPL · ~38s

Let me give you a real-world example of bandwidth at scale, because the numbers are genuinely wild.

▸ *[32M viewers label appears]*

The IPL Final on Hotstar in 2023 — 32 million concurrent streams at its peak.

▸ *[× 4 Mbps per stream]*

Each stream needs roughly 4 megabits per second of bandwidth.

▸ *[= 128 Tbps total]*

That's 128 terabits per second of total bandwidth that has to flow — from servers to every viewer's screen, simultaneously.

▸ *[pipe + CDN annotation]*

You cannot serve that from one building in Mumbai. This is why Hotstar pre-positions the video in CDN nodes — Content Delivery Network — scattered across India, close to the viewers. Each viewer pulls the stream from a nearby node, not from one central server.

Bandwidth is why the CDN exists, and we'll get deep into CDNs in a later episode.

---

## Scene 13 — The trade-off: latency vs throughput (HERO) · ~53s

Now here's the engineer's decision — the trade-off at the heart of this episode.

Latency and throughput are often in tension, and you frequently have to choose which one you're optimising for.

▸ *[left panel: UPI payment flow]*

Take a UPI payment. When you tap "Pay" and send 500 rupees to someone, that money needs to move — right now. The server cannot batch it up and process it later. You need a response in under 500 milliseconds or the UX feels broken and the user panics. This is a latency-first system — every rupee must land immediately.

▸ *[LOW LATENCY / LOWER THROUGHPUT label]*

To guarantee that latency, you actually end up handling fewer requests at once. You trade some throughput to protect the latency.

▸ *[right panel: Swiggy analytics pipeline]*

Now contrast that with Swiggy's internal analytics pipeline — the system that tells the business team how many Hyderabadi biryani orders came in last week. Nobody is sitting there waiting for that number in real time. The system can collect ten million events through the day, batch them up, and process the whole lot every ten minutes.

▸ *[HIGH THROUGHPUT / HIGHER LATENCY label]*

That's a throughput-first design — you get massive efficiency by processing in batches, and the latency is perfectly acceptable because nobody needs the answer instantly.

▸ *[two-headed arrow + "engineer picks based on use-case"]*

The same data, the same infrastructure — and completely different priorities depending on what the system is actually for.

---

## Scene 14 — Recap + cliffhanger · ~38s

So here's what you now have — three numbers that, together, tell you almost everything about a system's health.

▸ *[latency card: "LATENCY — how long one request takes"]*

Latency: how long one request takes, end to end. Measured in milliseconds, tracked at p50 and p99.

▸ *[throughput card: "THROUGHPUT — how many per second"]*

Throughput: how many requests the system handles per second. Measured in qps.

▸ *[bandwidth card: "BANDWIDTH — how wide the pipe is"]*

And bandwidth: the physical ceiling on how much data can flow at once. Measured in megabits or terabits per second.

▸ *[cliffhanger line appears]*

In the next episode, we go one level deeper — into the full vocabulary engineers use to talk about scale. What does "four nines of availability" actually mean? Why does 99.9% uptime still leave you with nine hours of downtime every year? And what is qps really telling you when a system is close to its limit?

That's Ep04 — and it builds directly on everything you just learned.

---

## Delivery notes

- **Tone:** warm, curious, "delighted lecturer" — never textbook. Treat every analogy like you just thought of it.
- **The kitchen scene (S6):** slow down slightly here, it's the anchor metaphor for the whole season.
- **IRCTC moment (S8):** a touch of exasperated empathy — everyone's been there.
- **p99 tail (S10):** lean in, this is the "aha" moment. Give it a half-beat before "those are real people."
- **The trade-off scene (S13):** the two panels contrast — let there be a breath between them.
- **Pace:** ~145 wpm. The script runs about 10 min 20s at that pace.
