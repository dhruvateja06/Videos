# Ep04 — Scale Vocabulary: qps, p50/p99, and Availability "Nines"
## Narration Script · ~150 wpm · ~10 min

> **▸** = visual reveal cue, with a bracketed description specific enough to
> build the composition from directly (per `WORKFLOW.md` Phase 3).
> **SFX** blocks follow `docs/SFX.md`'s 5-sound palette: `whoosh` / `zip` /
> `chime` / `riser` / `swell`. Read aloud before finalising.

---

## Scene 1 — The dashboard nobody can read (HOOK) · ~35s

Somewhere in Bangalore, a Swiggy engineer is staring at a dashboard.

▸ *[dashboard frame slides in, dark monitoring-console look]*

Numbers are scrolling past — twelve thousand something, forty-five milliseconds, eight-twenty milliseconds, ninety-nine point nine nine percent.

▸ *[three number blocks tick in fast: "12,000", "45ms / 820ms", "99.99%"]*

To you and me, that's noise. To this engineer, it's the entire health of the system, at a glance.

▸ *[engineer silhouette leans in, numbers pulse]*

So what do these numbers actually mean — and how does one glance tell you if everything's fine, or about to fall over?

**SFX:**
- `whoosh` on the dashboard frame entering
- `zip` on each of the three number blocks as they tick in (~0.3s apart)
- `riser` under the final line, building slightly into Scene 2's cut

---

## Scene 2 — A number alone lies · ~28s

Here's the trap: a single number, with no vocabulary around it, doesn't tell you anything.

▸ *[one bare number floats: "820"]*

"820" — is that good? Bad? Milliseconds? Requests? You can't tell.

▸ *[question marks orbit the number]*

The vocabulary is what turns a number into a diagnosis. That's what this episode gives you.

**SFX:**
- `zip` on the bare number appearing
- (quiet scene otherwise — let the uncertainty sit)

---

## Scene 3 — Quick callback · ~32s

You already met two of these numbers last episode, so this is just a reminder, not a re-teach.

▸ *[qps card slides in from left: "qps — requests handled per second"]*

qps: how many requests the system handles every second.

▸ *[p50/p99 card slides in from right: "p50 / p99 — how fast, for how many people"]*

p50 and p99: how long a request takes, for the typical user and for the unlucky one-in-a-hundred.

▸ *[both cards settle side by side]*

Today we go one level deeper on both — and we add a third number that neither of them tells you.

**SFX:**
- `zip` on each card sliding in
- `whoosh` on the scan-sweep out, into Scene 4

---

## Scene 4 — Concurrent users ≠ qps · ~45s

First correction: "a lakh people opened the app" and "the server is handling a lakh requests a second" are not the same sentence.

▸ *[100 user dots appear on screen, labelled "1,00,000 users online"]*

A hundred thousand people can have Swiggy open right now.

▸ *[dots mostly go still/grey, a few pulse]*

But most of them are just staring at the menu, deciding between biryani and butter chicken. They're not hitting the server every second — they're *idle*, most of the time.

▸ *[only a handful of dots pulse and send a packet toward a server icon]*

Only the ones actually tapping — searching, ordering, refreshing — generate real requests. That gap between "people online" and "requests per second" is called think time.

▸ *[label: "1,00,000 online → maybe 2,000 qps"]*

So a hundred thousand concurrent users might only produce two thousand qps. Confusing the two is how people wildly overestimate — or underestimate — what a server actually needs to handle.

**SFX:**
- `zip` on the 100 users appearing (grouped, not one-by-one)
- `zip` × 3-4 as the handful of active dots send packets
- `chime` on the "1,00,000 online → maybe 2,000 qps" label landing

---

## Scene 5 — Headroom (HERO) · ~42s

Second new idea: it's not enough to know your qps. What matters is how close you are to the edge.

▸ *[gauge/dial appears, needle in green zone: "2,000 / 10,000 qps"]*

If your system can handle ten thousand qps and you're sitting at two thousand, you have headroom — plenty of room before anything breaks.

▸ *[needle climbs into amber: "7,500 / 10,000 qps"]*

At seventy-five hundred, you're getting close. Response times start creeping up even before you hit the ceiling.

▸ *[needle slams into red: "10,200 / 10,000 qps"]*

Cross the ceiling, and it's not a graceful slowdown — queues start forming, and things that used to take milliseconds start taking seconds.

**SFX:**
- `zip` on the gauge appearing
- `riser` as the needle climbs from green through amber
- `chime` (sharp, not warm) as the needle crosses into red, past the ceiling

---

## Scene 6 — Introducing "nines" · ~35s

Now the third number — the one from the cliffhanger. Engineers promise reliability using something called "nines."

▸ *[ladder rises: "99%" → "99.9%" → "99.99%" → "99.999%"]*

Ninety-nine percent uptime. Ninety-nine point nine. Ninety-nine point nine nine. Ninety-nine point nine nine nine.

▸ *[each rung glows as it's named, ladder keeps climbing]*

Every extra nine sounds like a rounding error. It is absolutely not one — and here's why.

**SFX:**
- `zip` on each rung of the ladder appearing (one per "nine")
- `whoosh` on the scan-sweep out

---

## Scene 7 — The downtime-budget math (HERO) · ~50s

Let's translate percentages into something you can actually feel: minutes and hours a year.

▸ *[99% row: "99% → 3.65 days of downtime / year"]*

Ninety-nine percent uptime sounds great — until you realize it allows three point six five days of downtime a year. That's a whole long weekend of "the app is down," spread across the calendar.

▸ *[99.9% row: "99.9% → 8.76 hours / year"]*

Add one nine — ninety-nine point nine percent — and that shrinks to eight point seven six hours a year. Better, but still an entire workday of outages.

▸ *[99.99% row: "99.99% → 52 minutes / year"]*

Add another nine and you're down to fifty-two minutes a year, total.

▸ *[99.999% row: "99.999% → 5 minutes / year"]*

One more nine, and you're at five minutes a year. Five minutes, across the entire year, for every outage combined.

▸ *[all four rows glow together]*

Each nine you add is roughly a ten-times reduction in allowed downtime.

**SFX:**
- `zip` on each row's downtime figure landing (99%, 99.9%, 99.99%, in sequence)
- `chime` on the "99.999% → 5 minutes / year" row — the punch line of the scene
- `swell` under the four rows glowing together at the end

---

## Scene 8 — Why UPI can't afford fewer nines · ~42s

Here's why this isn't just a trivia stat — because some systems literally cannot tolerate the outage a "lower" nine allows.

▸ *[UPI transaction flow: phone → bank → NPCI → bank, money icon travels]*

Every UPI payment in India — from paying an auto driver to a business settling lakhs — runs through this rail.

▸ *[uptime badge stamps on: "99.99% mandated"]*

NPCI, the body that runs UPI, mandates ninety-nine point nine nine percent uptime for banks on the network. Not ninety-nine percent — that extra two nines is the difference between "rare glitch" and "money stuck mid-transfer during peak hours, at scale."

▸ *[downtime comparison: "99% = 3.65 days stuck" vs "99.99% = 52 min stuck"]*

Three point six five days of a payment rail being unreliable would be a national story. Fifty-two minutes a year is survivable. That gap is exactly why the nines matter here — they're a design requirement, not a stat you round off.

**SFX:**
- `whoosh` on scan-sweep into the UPI flow
- `zip` on the money icon traveling each hop
- `chime` on the "99.99% mandated" badge stamping in

---

## Scene 9 — Why each nine costs exponentially more · ~38s

So why doesn't everyone just build for five nines? Because each extra nine gets brutally more expensive.

▸ *[cost curve: flat at 99%, then steepening sharply toward 99.999%]*

Going from ninety-nine to ninety-nine point nine might mean better monitoring and a faster on-call process. Going from ninety-nine point nine nine to five nines can mean an entire second data centre, standing by, just for the days everything else fails at once.

▸ *[label: "diminishing returns, escalating cost"]*

The reliability curve is steep at the top. Chasing the last nine is often the most expensive engineering work a company ever does.

**SFX:**
- `zip` on the cost curve drawing on, left to right
- `chime` on the "diminishing returns, escalating cost" label

---

## Scene 10 — SLA, SLO, SLI · ~42s

One more piece of vocabulary, because you'll hear these three constantly: SLA, SLO, and SLI.

▸ *[card 1: "SLA — the promise to the customer"]*

SLA — service level agreement. The promise made externally, often with a penalty attached if it's broken.

▸ *[card 2: "SLO — the internal target"]*

SLO — service level objective. The internal bar the engineering team actually aims for, usually stricter than the SLA, so there's a safety margin.

▸ *[card 3: "SLI — the actual measurement"]*

SLI — service level indicator. The real number being measured right now, that tells you whether you're meeting the SLO.

▸ *[three cards nest: SLI feeds SLO, SLO backs SLA]*

The SLI is reality. The SLO is the internal goal. The SLA is what you promised the world.

**SFX:**
- `zip` on each of the 3 cards sliding in
- `chime` on the nesting animation ("SLI feeds SLO, SLO backs SLA")

---

## Scene 11 — Reading the dashboard now (HERO) · ~38s

Let's go back to that dashboard from the start of the episode — except now you can actually read it.

▸ *[same dashboard from Scene 1 returns, numbers highlight one by one]*

Twelve thousand qps — that's the load, and you now know to check it against the ceiling for headroom.

▸ *[p50/p99 numbers highlight: "45ms / 820ms"]*

Forty-five milliseconds typical, eight-twenty for the unlucky one percent — that's the felt experience.

▸ *[nines badge highlights: "99.99%"]*

Ninety-nine point nine nine percent — that's the promise being kept, or broken.

▸ *[all three glow together, dashboard "makes sense" moment]*

Three numbers. Five seconds. The entire health of the system.

**SFX:**
- `zip` on each number highlighting in sequence
- `chime` on the "makes sense" moment when all three glow together

---

## Scene 12 — The 8pm spike, diagnosed · ~48s

Let's put it to work. Same 8pm Swiggy rush from last episode — but now watch the numbers, not just the chaos.

▸ *[qps counter climbs fast: "2,000 → 9,800 qps"]*

qps climbs toward the ceiling — headroom is disappearing.

▸ *[p99 counter spikes: "820ms → 4,200ms"]*

p99 latency, which was already the "unlucky" number, spikes hard — now even more people are having a bad time.

▸ *[nines badge flickers red: "99.99% → 99.2% (this month)"]*

And because this outage is dragging on, the month's uptime number is dropping in real time — eating into the whole year's downtime budget in one evening.

▸ *[on-call engineer icon appears, "diagnosing: load vs ceiling"]*

An engineer watching this doesn't need to guess. The vocabulary tells them exactly what's happening and how bad it is — instantly.

**SFX:**
- `riser` under the qps counter climbing, building through the scene
- `zip` as p99 spikes
- `chime` (alarmed, not warm) on the nines badge flickering red — resolves the riser
- `whoosh` on scan-sweep into the next scene

---

## Scene 13 — The cost of chasing more nines (trade-off beat) · ~35s

Here's the trade-off this episode lands on: more nines isn't free, and it isn't always worth it.

▸ *[left panel: small internal tool, "99% is fine — nobody's paying for outages"]*

An internal analytics dashboard breaking for twenty minutes a month is annoying, not a crisis.

▸ *[right panel: payment rail, "99.99% is the minimum acceptable"]*

A payment system breaking for the same twenty minutes is a headline. The right number of nines depends entirely on what breaks if you don't have them.

**SFX:**
- `zip` on each panel sliding in
- `chime` on the payment-rail panel — the scene's actual point

---

## Scene 14 — Recap · ~30s

Three numbers, one vocabulary.

▸ *[qps card: "qps — how much load, right now"]*

qps: how much load the system is under, right now.

▸ *[p50/p99 card: "p50 / p99 — how it feels, typical vs unlucky"]*

p50 and p99: how the request feels — for the typical user, and for the unlucky one.

▸ *[nines card: "nines — the promise being kept"]*

And nines: the promise being kept, measured in minutes of downtime a year.

**SFX:**
- `zip` on each of the 3 recap cards
- `swell` under all three settling together

---

## Scene 15 — Cliffhanger to Ep05 · ~30s

But here's the thing — knowing these numbers doesn't fix anything by itself. They just tell you *that* something's wrong.

▸ *[dashboard flatlines to a single red alert: "9,800 qps — no headroom left"]*

So what do you actually do when the numbers say you're out of room?

▸ *[silhouette of a figure standing at a fork in a hallway, two doors: "one kitchen" / "many kitchens"]*

Next episode: the load balancer — the waiter who decides which kitchen gets your order, so that no single cook ever gets buried.

**SFX:**
- `whoosh` on the dashboard flatlining
- `riser` under the fork-in-the-hallway visual, unresolved — deliberately left hanging into Ep05

---

## Delivery notes

- **Tone:** warm, curious, "delighted lecturer" — same register as Ep03. Never textbook, never alarmed except where the script calls for it.
- **Scene 1 (dashboard):** slight bewilderment in the voice on "that's noise, to this engineer, it's the entire health of the system" — invite the viewer into the confusion before resolving it.
- **Scene 7 (downtime math):** slow down on each number — "three point six five days," "eight point seven six hours" — let each one land before the next.
- **Scene 8 (UPI):** a touch more weight/seriousness here — this is the "why it actually matters" beat.
- **Scene 12 (8pm spike):** mirror Ep03's urgency from its own load-spike scene, but resolve it calmly at the end — this is the "aha, I can read this now" payoff.
- **Scene 15 (cliffhanger):** trail off slightly on "which kitchen gets your order" — let it hang, don't over-explain.
- **Pace:** ~150 wpm. Script runs approximately 9 min 45s at that pace.
