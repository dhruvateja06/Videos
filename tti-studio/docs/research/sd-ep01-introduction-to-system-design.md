# Ep 1 — Introduction to System Design · Research Dossier

> **Status:** ✅ researched (deep-research pass, 2026-06-25). 12 claims verified,
> 2 refuted. This is the **script source** for `compositions/sd-ep01-full.html`.
> Anything not marked ✅ below does **not** go on screen as a stated fact.

Episode reframed (per creator direction) from the "one user → a million" scaling
story to the **proper foundations**: what system design is, the basics
vocabulary, HLD vs LLD, and the system-design life cycle.

---

## 1. One-line promise

> After this episode a total beginner can say, in plain words, **what system
> design is, the handful of words the field is built on, and the step-by-step
> process designers actually follow** — and isn't scared of the phrase anymore.

---

## 2. The design section (🅗 HLD lens — this is a conceptual intro, no code)

### A. What system design IS (and why it matters)
- **Definition (beginner-safe):** system design is the practice of deciding a
  system's **architecture, components, and data flow** so it meets its
  requirements — especially as the number of users grows.
- Where it sits: it's the **"plan the building before you build it"** layer of
  software engineering. Coding is laying bricks; system design is the blueprint.
- Why interviews test it: it shows whether you can reason about **trade-offs at
  scale**, not just write a function.
- ⚠️ Attribution: present the crisp definitions as drawn from the **System
  Design Primer** (the canonical open reference, 300k+ stars), which traces to
  primary sources (Werner Vogels for scalability). Don't present one phrasing as
  "the one true definition."

### B. System Design BASICS — the core vocabulary (one line each)
| Term | Beginner one-liner | Status |
|---|---|---|
| **Client / server** | The client (your phone/app) **asks**; the server **answers**. | standard ✅ |
| **Request / response** | One ask + one answer = one round trip. | standard ✅ |
| **Latency** | How long **one** action takes (e.g. ms per request). | ✅ verified |
| **Throughput** | How **many** actions per second the system handles. | ✅ verified |
| **Scalability** | A system is scalable if performance **grows in proportion to the resources you add.** | ✅ verified (Vogels / SD Primer) |
| **Vertical scaling (scale up)** | A **bigger** machine. | ✅ verified |
| **Horizontal scaling (scale out)** | **More** (commodity) machines. Generally more cost-efficient + higher availability *at scale*. | ✅ verified |
| **Availability** | The % of time the system is up — measured in **"nines."** | ✅ verified |
| **Load balancer** | A traffic cop spreading requests across many servers. | standard (not independently verified this pass) |
| **Cache** | A small fast store of popular answers, so you don't redo work. | standard |
| **Database** | The durable source of truth for your data. | standard |
| **CDN** | Copies of content kept near users to cut distance/latency. | standard |
| **Queue** | A buffer that lets work be handled **later**, decoupling parts. | standard |

> **Design goal heuristic (✅ verified):** aim for **maximal throughput with
> acceptable latency.** (Caveat: some systems — IRCTC booking, trading — flip to
> latency-first; the "acceptable latency" clause already carries that.)

### C. HLD vs LLD (the precise distinction)
- **HLD (High-Level Design):** the **big picture** — major components, how they
  interact, data flow, and non-functional needs (scalability, availability).
  "Boxes and arrows on a whiteboard."
- **LLD (Low-Level Design):** the **inside of one box** — classes, methods, data
  structures, schemas for a single component. "Now write the code for that box."
- Worked mini-example: *"Design Instagram."* HLD = app servers + a database + a
  CDN for photos + a feed service. LLD = the exact `Post` class, the table
  columns, the function that builds a user's feed.
- ⚠️ Status: textbook-standard (Baeldung / GeeksforGeeks framing); **not**
  anchored by an independently-verified claim in this pass — present as the
  standard distinction, which it is, and it matches our own Season 2/3 split.

### D. The SYSTEM DESIGN LIFE CYCLE / process
- ✅ **Verified spine (System Design Primer's recommended 4 steps):**
  1. **Outline use cases, constraints & assumptions** (who uses it, how much, what must it do).
  2. **Create a high-level design** (the main boxes + arrows).
  3. **Design the core components** (each box in detail).
  4. **Scale the design** — find the **bottlenecks** and address them (load balancing, caching, sharding, replication).
- The episode can show the **fuller lifecycle** as an expansion of that spine:
  *requirements → scope/constraints & capacity estimate → high-level design →
  data/API design → low-level design → weigh trade-offs → find bottlenecks /
  scale → iterate.*
- ⚠️ Attribution: call the 4-step version **"the framework recommended by the
  System Design Primer,"** not "the one universal lifecycle."

---

## 3. Cross-link (how this stitches to other seasons)
- This episode is the **front door** to all of Season 2 (HLD). Each basics term
  becomes a future episode (load balancers → S2·E8, caching → S2·E10, …).
- The **HLD vs LLD** bit previews the Season 2 ↔ Season 3 split. **OOP / SOLID /
  patterns live in Season 3 (LLD)**, so we name LLD here but don't teach code.

---

## 4. The Indian teardown — Disney+ Hotstar / JioHotstar
The one deeply-verified real-world example.

- ✅ **Concurrency:** ~**25 million** concurrent viewers in **2019** (ICC World
  Cup India–NZ semi-final) as a prior milestone; the measured **record is 59
  million** concurrent (2023 World Cup final, **19 Nov 2023**).
  **🚩 Do NOT show "60M" or "61M"** — those figures were **refuted** (internally
  inconsistent in the source). Use **25M → 59M** only.
- ⚠️ **Architecture (medium confidence — engineering-blog sourced, attribute as
  "per engineering reports"):** ~**800+ microservices**; migrated from
  self-managed **KOPS → Amazon EKS**; replaced **200+ load balancers** with a
  centralized **Envoy-based API gateway**; split **cacheable vs non-cacheable
  APIs** at the CDN (live scores cached; user sessions not).
- ⚠️ **Time-stamp it:** "as of the documented 2023 World Cup overhaul" — these
  details are point-in-time.

> **Other Indian products (Swiggy/UPI/IRCTC/Ola):** great for *analogy* and
> qualitative framing, but **no verified beginner-safe numbers** were surfaced.
> On screen keep them qualitative ("billions of UPI payments a month", "lakhs of
> Tatkal tickets in minutes") — **no specific digits** until a follow-up
> research pass cites NPCI / IRCTC / Swiggy primaries.

---

## 5. The analogy (one mental model, reused)
**Designing a system = designing a restaurant.**
- Clients = diners placing orders; servers = the kitchen; the menu/waiter = the
  API; the pantry = the database; a popular pre-made dish kept ready = the cache;
  more kitchens for a rush = horizontal scaling; the host directing diners to
  free tables = the load balancer.
- Where it breaks: a restaurant has a fixed building; software can add "kitchens"
  in seconds — which is exactly why scaling decisions matter.

---

## 6. Common misconceptions (debunk beats — great shorts)
1. ✅ **"Premature optimization is the root of all evil" = never optimize.**
   Wrong. It's a **truncation of Knuth (1974)**; the full quote says forget small
   efficiencies *~97% of the time* but **"we should not pass up our opportunities
   in that critical 3%."** (3%/97% are Knuth's illustrative figures, not data.)
   🚩 Do **not** credit the line to Tony Hoare on screen — that attribution was
   **refuted**; cite it as published by **Knuth**.
2. ✅ **"Faster hardware (Moore's Law) makes optimization pointless."** Rebutted
   (ACM Ubiquity, 2009) — doubling memory/CPU doesn't remove the need to design
   well.
3. **"System design = drawing boxes."** The boxes are easy; the **trade-offs**
   (why this box, not that one) are the actual skill.
4. **"You must clarify requirements first; jumping to architecture is the #1
   beginner mistake."** (Standard interview guidance; present as guidance.)
5. **"HLD and LLD are the same thing / interchangeable."** They're different
   altitudes — big picture vs the code inside one box.

---

## 7. 8th-grade explanation (the BRAND.md test — ≤2 sentences)
> System design is drawing the **plan** for an app **before** you build it —
> deciding what parts you need (servers, a database, a cache) and how they talk —
> so it stays **fast** and **doesn't crash** even when millions of people use it
> at once.

---

## 8. Numbers to get right (each with a source + on-screen rule)
| Fact | On-screen? | Source |
|---|---|---|
| Scalability = performance ∝ resources added | ✅ yes (frame as "a system is scalable if…") | SD Primer; Vogels 2006 |
| Latency = 1 action's time; throughput = actions/sec | ✅ yes | SD Primer |
| 99.9% ≈ **8h 45min/yr** down; 99.99% ≈ **52min/yr** | ✅ yes (assumes 365.25-day yr — round or state) | SD Primer |
| Horizontal vs vertical (scale out vs up) | ✅ yes (qualitative) | SD Primer |
| **Vendor cost %s** ("40–65%", "20×", "$/min downtime") | 🚩 NO | unconfirmed vendor blogs |
| 4-step process | ✅ yes (attribute to SD Primer) | SD Primer |
| Knuth quote + 3%/97% | ✅ yes (illustrative) | Knuth 1974 / ACM Ubiquity |
| Hotstar **25M (2019)** & **59M (2023)** concurrent | ✅ yes | systemdesign.one; TechCrunch/Sportcal |
| Hotstar **60M / 61M** | 🚩 NO (refuted) | — |
| Hotstar 800+ microservices, 200+ LBs, KOPS→EKS | ⚠️ yes, attributed "per engineering reports" | ByteByteGo; pritamroy.com |
| UPI / IRCTC / Swiggy specific digits | 🚩 NO (keep qualitative) | not yet sourced |

---

## 9. Sources (with confidence)
**Verified / primary-backed (✅):**
- System Design Primer — https://github.com/donnemartin/system-design-primer (vocabulary, nines, 4-step process) — *secondary, 300k★, traces to primaries*
- Werner Vogels, "A Word on Scalability" (2006) — https://www.allthingsdistributed.com/2006/03/a_word_on_scalability.html — *primary (scalability)*
- Knuth via ACM Ubiquity, "The Fallacy of Premature Optimization" (2009) — https://ubiquity.acm.org/article.cfm?id=1513451 — *secondary, cites Knuth 1974 primary*
- Hotstar 59M record — https://newsletter.systemdesign.one/p/hotstar-scaling (+ TechCrunch/Sportcal corroboration)
- Hotstar 25M (2019) — AWS re:Invent CMY302 deck

**Single-source / attribute carefully (⚠️):**
- Hotstar architecture details — https://blog.bytebytego.com/p/how-disney-hotstar-now-jiohotstar ; https://www.pritamroy.com — *engineering blogs, not official press*

**Refuted — do not use (🚩):**
- Hotstar "60M/61M" concurrent (0-3) — internally inconsistent
- Tony Hoare as the origin of the optimization maxim (0-3) — cite Knuth instead

**Open follow-ups (for a later pass):** authoritative on-screen numbers for
UPI (NPCI), IRCTC tickets/min, Swiggy peak orders; a primary anchor for the
HLD-vs-LLD worked example; beginner-safe capacity-estimation math.
