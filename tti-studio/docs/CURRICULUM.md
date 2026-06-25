# The Tech Intern — Curriculum

> The channel covers tech broadly (AI, system design, DevOps, security, …).
> **Season 1 is AI** and **Season 2 is System Design** — both fully sequenced
> below (30 episodes each). Later seasons — DevOps, security — reuse the same
> format, style, and pipeline.

## Season 1 — AI (30 episodes)

**Promise:** Zero to understanding modern AI. No PhD, no jargon, no skipped steps.
**Pace:** 2 long-form/week (Mon + Thu) → 15 weeks. 10–12 min each + 3–5 shorts.
**Output:** 30 long-form + ~120 shorts.

### Modules

| # | Module | Eps | Locks in |
|---|---|---|---|
| M1 | Foundations | 1–5 | What AI even is. Vocabulary. Mental map. |
| M2 | How Machines Learn | 6–11 | The learning mechanism. First code. |
| M3 | Neural Networks | 12–17 | The building blocks. Second code. |
| M4 | Modern Architectures | 18–23 | CNN, RNN, Transformer, attention, embeddings. |
| M5 | Generative AI Era | 24–30 | LLMs, RAG, RLHF, agents, diffusion, what's next. |

### Episode map

| Ep | Title | Diff | Code | Status |
|---|---|---|---|---|
| 1 | What is AI, really? | 🟢 | – | **DONE** — `compositions/ep01-full.html` |
| 2 | AI vs ML vs Deep Learning vs GenAI — finally clear | 🟢 | – | |
| 3 | DATA → MODEL → PREDICTION: the framework every AI system uses | 🟢 | – | |
| 4 | Supervised, Unsupervised, Reinforcement — three ways to learn | 🟢 | – | |
| 5 | Why AI is having a moment NOW (compute + data + algorithms) | 🟢 | – | |
| 6 | What does "learn from data" actually mean? | 🟢 | – | |
| 7 | The loss function: how a machine knows it's wrong | 🟡 | – | |
| 8 | Gradient descent: the "walking downhill" mental model | 🟡 | – | |
| 9 | Train / validation / test: why we split data | 🟢 | – | |
| 10 | Overfitting: when the model memorizes instead of learns | 🟡 | – | |
| 11 | Your first ML model in Python (code-along) | 🟡 | ✅ | |
| 12 | The neuron: just a weighted sum + activation | 🟡 | – | |
| 13 | Why layers? Building from simple to complex | 🟡 | – | |
| 14 | Activation functions: ReLU, Sigmoid, Softmax | 🟡 | – | |
| 15 | Backpropagation: how networks actually update | 🔴 | – | |
| 16 | Why depth matters (deep vs shallow) | 🟡 | – | |
| 17 | Build a tiny neural net in Python (code-along) | 🔴 | ✅ | |
| 18 | CNN: how computers actually see | 🟡 | – | |
| 19 | RNN / LSTM: how computers process sequences | 🔴 | – | |
| 20 | The Transformer: the most important paper of the decade | 🔴 | – | |
| 21 | Attention is all you need: what that actually means | 🔴 | – | |
| 22 | Embeddings: turning words into math | 🟡 | – | |
| 23 | Tokens, context windows, and why ChatGPT forgets | 🟡 | – | |
| 24 | What is a Large Language Model, really? | 🟡 | – | |
| 25 | Pre-training vs fine-tuning vs RLHF | 🔴 | – | |
| 26 | RAG: giving an LLM your own knowledge | 🟡 | – | |
| 27 | Prompt engineering: what actually works | 🟢 | – | |
| 28 | AI agents: when models can act, not just talk | 🟡 | – | |
| 29 | Diffusion models: how images and videos are generated | 🔴 | – | |
| 30 | The roadmap from here: what to learn after Season 1 | 🟢 | – | |

## The 4-beat teaching pattern (every episode)

```
1. HOOK with something they already do   → "You just opened Swiggy. Watch this..."
2. SURFACE the question                   → "How does it know 32 minutes?"
3. EXPLAIN in 8th-grade language          → 1 visual analogy + 1 simple sentence
4. CONNECT BACK                           → "That's what just happened on your phone."
```

## Recurring mental models (the compounding moat)

Introduce a metaphor once, then *invoke* it later (never re-explain):

| Metaphor | Introduced | Reused in | Explains |
|---|---|---|---|
| **Rules vs Patterns** | Ep 1 | 2, 6, 25 | Why AI ≠ traditional software |
| **Downhill walker** (gradient descent) | Ep 8 | 11, 15 | How models improve |
| **Weighted sum** (neuron) | Ep 12 | 13, 14, 16 | Building block |
| **Memorize vs generalize** | Ep 10 | 11, 17, 25 | The eternal trap |
| **Spotlight** (attention) | Ep 21 | 23, 24 | What Transformers do |
| **Map of meanings** (embeddings) | Ep 22 | 23, 26, 27 | Why LLMs feel like they understand |

## Indian example matrix (use ≥2 per episode)

| Example | First in | Concept |
|---|---|---|
| Swiggy delivery ETA | Ep 1 | Regression |
| UPI fraud detection | Ep 1 | Binary classification |
| Bhashini multilingual | Ep 5 | Embeddings / multilingual transformers |
| Flipkart recommendations | Ep 4 | Unsupervised / similarity |
| Indian Railways seat allocation | Ep 4 | Reinforcement learning |
| Krishi agri AI (Karnataka) | Ep 18 | CNN / computer vision |
| Diffusion poster generation | Ep 29 | Diffusion |

## Shorts derivation (3–5 per long-form)

| Type | Source | Hook |
|---|---|---|
| Definition | the 30s "what it is" opener | "X in 60 seconds — finally clear" |
| Example | the Indian-example portion | "Why [product] uses [concept]" |
| Visual | the mental-model diagram | "The simplest way to understand [concept]" |
| Cliffhanger | the roadmap ending | "[Concept] is just the beginning…" |
| Hot take | one contrarian moment | "Most people get [concept] wrong" |

## Pre-record quality checklist

- [ ] First 15s = familiar Indian scenario, no jargon
- [ ] One specific question the viewer would ask themselves
- [ ] Core concept in ≤2 sentences, 8th-grade level
- [ ] One visual analogy (the episode's recurring metaphor)
- [ ] Concept restated 2–3× in different words
- [ ] Last 30s calls back to the opening scenario
- [ ] Every jargon term defined in plain English on first use
- [ ] A "verify on your phone right now" moment
- [ ] Concrete cliffhanger to the next episode

---

## Season 2 — System Design · HLD (30 episodes)

> Same channel, same format, same pipeline. Where Season 1 answered *"what is
> the machine thinking?"*, Season 2 answers *"what happens after you tap the
> button — and how does it still work when a million people tap at once?"*
> Worked examples are **Indian product teardowns** (Swiggy, UPI, Hotstar, IRCTC,
> Flipkart, WhatsApp, Ola) — the apps the viewer already has open.

**Promise:** Zero to designing real systems. From "what is a server" to "how
Hotstar streams the IPL final to 50 million people" — no CS degree, no jargon,
no skipped steps.
**Pace:** 2 long-form/week (Mon + Thu) → 15 weeks. 10–12 min each + 3–5 shorts.
**Output:** 30 long-form + ~120 shorts.

### HLD & LLD are two separate seasons (read this first)

System design is taught — and interviewed — as two distinct skills. We give each
its **own season** so neither gets the shallow treatment, and so the difficulty
curve stays honest (HLD needs no code; LLD assumes light OOP):

- **Season 2 — HLD (High-Level Design):** the *boxes-and-arrows* view. Components
  and how they connect — servers, load balancers, caches, databases, queues,
  CDNs — plus the trade-offs that decide which box goes where. "Draw the system
  on a whiteboard." Beginner-reachable with no code. **(The 30 episodes below.)**
- **Season 3 — LLD (Low-Level Design):** the *inside-one-box* view. Turning a
  single component into actual classes, methods, data structures and state
  machines — the LRU cache, the token bucket, the circuit-breaker state machine,
  the payment ledger — built on OOP, SOLID and the core design patterns. "Now
  write the code for that box." **(Sequenced as its own season further down.)**

The two seasons are designed to **rhyme**: many Season 2 HLD episodes have a
direct Season 3 LLD counterpart (caching → *build an LRU cache*; rate limiting →
*token-bucket class*; resilience → *circuit-breaker state machine*). Those
cross-links are mapped in the table under the episode map, so a viewer can watch
the HLD episode, then later the LLD episode, and feel the same topic from both
sides. This also resolves the old "where do OOP/SOLID/patterns live?" gap —
**they're Season 3's foundation module.**

### Modules

| # | Module | Eps | Locks in |
|---|---|---|---|
| M1 | What a system even is | 1–6 | Client/server, the request, latency, the API, where data lives. |
| M2 | Scaling the basics | 7–12 | More users than one box can serve. Load balancers, caching, CDN. |
| M3 | Data at scale | 13–18 | SQL vs NoSQL, indexes, replication, sharding, CAP, consistency. |
| M4 | Talking & staying up | 19–24 | Queues, async, rate limits, idempotency, retries, micro vs mono. |
| M5 | Designing real systems | 25–30 | The whiteboard interview classics, end-to-end, the Indian way. |

### Episode map (all HLD)

Season 2 is **pure HLD** — every episode is the boxes-and-arrows view, no code, no
OOP required. The LLD counterparts live in Season 3 (cross-link table below).

| Ep | Title | Diff | Code | Status |
|---|---|---|---|---|
| 1 | What is system design, really? (one user → one million) | 🟢 | – | |
| 2 | Client & server: what actually happens when you open Swiggy | 🟢 | – | |
| 3 | The request's journey: DNS → server → screen, in plain English | 🟢 | – | |
| 4 | Latency vs throughput: the two numbers that decide everything | 🟢 | – | |
| 5 | The API: how apps talk to each other (the waiter analogy) | 🟢 | – | |
| 6 | Where data lives: databases for absolute beginners | 🟢 | – | |
| 7 | Vertical vs horizontal scaling: bigger box vs more boxes | 🟢 | – | |
| 8 | Load balancers: the traffic cop in front of your servers | 🟡 | – | |
| 9 | Stateless vs stateful: the rule that makes scaling possible | 🟡 | – | |
| 10 | Caching: why your feed loads before you blink | 🟡 | – | |
| 11 | Cache invalidation: the "two hard problems" one, made simple | 🟡 | – | |
| 12 | CDN: how Hotstar streams the IPL to 50 million phones | 🟡 | – | |
| 13 | SQL vs NoSQL: picking the right database (no holy war) | 🟡 | – | |
| 14 | Indexing: how a query finds one row out of a billion | 🟡 | – | |
| 15 | Replication: copies that keep you online when a server dies | 🟡 | – | |
| 16 | Sharding: splitting one giant database across many machines | 🔴 | – | |
| 17 | The CAP theorem: consistency vs availability, finally clear | 🔴 | – | |
| 18 | Eventual consistency: why your like-count lags for a second | 🟡 | – | |
| 19 | Message queues: how an app says "I'll handle this later" | 🟡 | – | |
| 20 | Sync vs async: why your order confirms instantly but ships later | 🟡 | – | |
| 21 | Rate limiting: stopping abuse and the thundering herd | 🟡 | – | |
| 22 | Idempotency: why double-tapping "Pay" doesn't pay twice | 🔴 | – | |
| 23 | Retries, timeouts & circuit breakers: failing gracefully | 🔴 | – | |
| 24 | Monolith vs microservices: one big app or many small ones | 🟡 | – | |
| 25 | Design a URL shortener (the classic first interview question) | 🟡 | – | |
| 26 | Design a news feed (Instagram / X): fan-out explained | 🔴 | – | |
| 27 | Design a chat app (WhatsApp): delivered, then those blue ticks | 🔴 | – | |
| 28 | Design a ride-hailing match (Ola / Uber): finding the nearest cab | 🔴 | – | |
| 29 | Design a payment system (UPI): money must never be wrong | 🔴 | – | |
| 30 | Putting it together: how Swiggy survives New Year's Eve | 🟡 | – | |

### HLD → LLD cross-links (how the two seasons rhyme)

Many Season 2 (HLD) episodes have a natural Season 3 (LLD) counterpart — the same
topic, now coded as a class/data structure. This map is the through-line that
makes the channel feel like one course. Not every HLD episode has an LLD twin
(some are purely architectural), and Season 3 adds its own foundation + pattern
episodes that have no HLD parent. Season 3 numbering is finalized in its own
section below; this table shows the *pairing intent*.

| S2 HLD episode | → S3 LLD counterpart (the thing you code) |
|---|---|
| 5 · The API | Designing clean endpoints / interfaces (resources, verbs, DTOs) |
| 6 · Where data lives | Schema & entity modelling; normalization |
| 8 · Load balancers | A balancing-strategy class (round-robin / least-connections) |
| 9 · Stateless vs stateful | A `SessionStore` interface; the sticky-session trap |
| 10 · Caching | **Build an LRU cache** (HashMap + doubly-linked list) — the classic LLD Q |
| 11 · Cache invalidation | Write-through + TTL eviction; a stampede (single-flight) lock |
| 13 · SQL vs NoSQL | Modelling the same data both ways (normalized vs access-pattern-first) |
| 14 · Indexing | B-tree vs hash index structure; composite-index design |
| 16 · Sharding | A **consistent-hashing ring** class (virtual nodes) |
| 19 · Message queues | Producer/consumer with at-least-once + ack; a bounded queue |
| 20 · Sync vs async | Callbacks → futures/promises; an async handler |
| 21 · Rate limiting | **Token-bucket / sliding-window** limiter class |
| 22 · Idempotency | Idempotency-key store + dedup; the double-tap-Pay guard |
| 23 · Retries & circuit breakers | **Circuit-breaker state machine** (closed/open/half-open) |
| 25 · URL shortener | base62 encode/decode + key-gen + schema (HLD & LLD meet) |
| 26 · News feed | `FeedItem` model; ranking; merging N timelines |
| 27 · Chat app | **Message delivery state machine** (sent → delivered → read) |
| 28 · Ride-hailing | Geohash/quadtree index + nearest-driver matching |
| 29 · Payment (UPI) | Payment state machine + double-entry ledger + idempotency key |

> Purely-HLD episodes with **no** LLD twin: 1–4, 7, 12, 15, 17, 18, 24, 30
> (architecture/theory — there's no single class to build).

## The 4-beat teaching pattern (still every episode)

Same discipline as Season 1 — only the worked examples change:

```
1. HOOK with something they already do   → "It's 8pm. You and a lakh others open Swiggy..."
2. SURFACE the question                   → "How does ONE app not just fall over?"
3. EXPLAIN in 8th-grade language          → 1 visual analogy + 1 simple sentence
4. CONNECT BACK                           → "That's the load balancer you never saw."
```

## Recurring mental models (the Season-2 moat)

Introduce a metaphor once, then *invoke* it later (never re-explain):

| Metaphor | Introduced | Reused in | Explains |
|---|---|---|---|
| **The busy restaurant** (host, waiters, kitchen) | Ep 2 | 5, 7, 8, 30 | Client/server, APIs, scaling, load balancing |
| **Express checkout lane** | Ep 10 | 11, 12 | Caching & CDN (keep the popular thing nearby) |
| **The library catalogue** | Ep 14 | 16 | Indexing (don't read every book to find one) |
| **Photocopies of the ledger** | Ep 15 | 17, 18 | Replication & consistency |
| **Splitting the guest list A–M / N–Z** | Ep 16 | 28, 29 | Sharding & partitioning |
| **The courier / post office** | Ep 19 | 20, 21 | Queues & async ("drop it, I'll process later") |
| **The fuse box** (trips to protect the house) | Ep 23 | 30 | Circuit breakers & graceful failure |

## Indian product teardown matrix (use ≥2 per episode)

| Product | First in | Concept it anchors |
|---|---|---|
| Swiggy / Zomato dinner rush | Ep 1 | Load, scaling, the whole-system finale |
| UPI payment | Ep 5 | APIs, idempotency, strong consistency |
| Hotstar IPL live stream | Ep 12 | CDN, read-heavy fan-out, surge |
| IRCTC Tatkal 10am rush | Ep 21 | Rate limiting, concurrency, locking |
| Flipkart Big Billion Days | Ep 10 | Caching, queues, horizontal scaling |
| WhatsApp message delivery | Ep 27 | Queues, delivery guarantees, ticks |
| Ola / Uber cab matching | Ep 28 | Geo-sharding, nearest-neighbour, real-time |

## Shorts derivation (3–5 per long-form)

Same five shapes as Season 1 — sourced from each system-design episode:

| Type | Source | Hook |
|---|---|---|
| Definition | the 30s "what it is" opener | "Load balancers in 60 seconds — finally clear" |
| Teardown | the Indian product segment | "How Hotstar streams the IPL without crashing" |
| Visual | the build-up diagram | "The simplest way to picture sharding" |
| Cliffhanger | the end-of-episode tease | "Caching is easy. Cache *invalidation* isn't…" |
| Hot take | one contrarian moment | "You probably don't need microservices" |

> **Status:** Season 2 (HLD) is fully sequenced — 30 architecture episodes, no
> code. Its LLD counterpart is **Season 3** (sequenced below). No episodes built
> yet. Production is **research-gated**: each episode is only authored once its
> research dossier (standard below) exists. Ep 1
> (`compositions/sd-ep01-full.html`) is the first target, after its dossier.

## Per-topic research dossier (the standard)

> The rule for this season: **no episode is authored until its dossier is written
> and fact-checked.** We go *one topic at a time, maximum depth* — strong,
> sourced research per topic, not thin coverage across all 30.

Each dossier lives at **`docs/research/sd-epNN-<slug>.md`** and must contain, in
this order:

1. **One-line promise** — what the viewer can do/explain after watching.
2. **The design section** — for a **Season 2 (HLD)** episode: the components, the
   trade-offs, and *why* each choice (the boxes-and-arrows the episode builds on
   screen). For a **Season 3 (LLD)** episode: the class / data structure / state
   machine with a tiny correct code sketch (the thing we animate building). Each
   dossier is one lens — never both crammed together.
3. **The cross-link** — name the sibling episode in the other season (e.g. HLD
   "Caching" ↔ LLD "Build an LRU cache") so the two seasons stay stitched.
4. **The Indian teardown** — the real product example with **real, cited
   numbers** (concurrency records, RPS, data volumes, outage post-mortems). No
   invented figures — every number carries a source.
5. **The analogy** — the one everyday mental model (restaurant, checkout lane,
   ledger…) and exactly how it maps to the tech, where it breaks down.
6. **Common misconceptions** — 3–5 "most people get this wrong" beats (great
   shorts + the episode's hot-take).
7. **8th-grade explanation** — the core idea in ≤2 plain sentences (the test
   from BRAND.md).
8. **Numbers to get right** — the handful of figures/definitions that must be
   accurate, each with a source link.
9. **Sources** — every claim cited; mark each ✅ verified / ⚠️ single-source /
   ❓ couldn't confirm. Anything not ✅ does **not** go on screen as fact.

**Research method:** use the `deep-research` skill (fan-out web search → fetch →
adversarially verify → cited synthesis) per topic. Beginner framing is on us;
the *facts and numbers* must be sourced and verified — that is the bar the
creator asked for.

**Dossier status tracker:**

| Ep | Dossier | State |
|---|---|---|
| 1 | `docs/research/sd-ep01-introduction-to-system-design.md` | ✅ researched & written |
| 2–30 | — | ⬜ queued (one at a time, on pick) |

---

## Season 3 — Low-Level Design (LLD) (25 episodes)

> The sibling season to Season 2. Where HLD drew the boxes, LLD opens **one box**
> and writes the code inside it: objects, classes, the right data structure, a
> clean state machine. Same channel, same format, same pipeline — but now there's
> code on screen (animated building, the way EP01 builds diagrams). Assumes only
> what Season 1's code-along episodes taught; we still teach OOP from zero.

**Promise:** From "what is an object?" to confidently modelling any system on a
whiteboard — parking lot, BookMyShow, Splitwise — the way an LLD interview asks.
**Pace:** same — 2 long-form/week + shorts.
**Output:** 25 long-form + ~100 shorts.

### Modules

| # | Module | Eps | Locks in |
|---|---|---|---|
| L1 | Objects from zero | 1–5 | What classes/objects are; the 4 OOP pillars, in plain English. |
| L2 | Writing code that doesn't rot | 6–10 | SOLID, clean code, UML you'll actually use. |
| L3 | The design patterns that matter | 11–17 | The ~7 patterns that show up again and again. |
| L4 | The classic LLD data structures | 18–20 | LRU cache, token bucket, state machines — the reusable kit. |
| L5 | "Design X" object-modelling | 21–25 | The interview classics, fully modelled. |

### Episode map (all LLD)

| Ep | Title | Diff | Code | S2 HLD link |
|---|---|---|---|---|
| 1 | What is an object? (a thing that knows stuff + does stuff) | 🟢 | ✅ | – |
| 2 | Classes, instances & the 4 pillars, with one running example | 🟢 | ✅ | – |
| 3 | Encapsulation & abstraction: hide the mess, show the buttons | 🟢 | ✅ | – |
| 4 | Inheritance vs composition: "is-a" vs "has-a" (prefer has-a) | 🟡 | ✅ | – |
| 5 | Polymorphism: one call, many behaviours | 🟡 | ✅ | – |
| 6 | SOLID #1–2: Single Responsibility & Open/Closed | 🟡 | ✅ | – |
| 7 | SOLID #3–5: Liskov, Interface Segregation, Dependency Inversion | 🔴 | ✅ | – |
| 8 | Clean code: naming, small functions, the smell test | 🟢 | ✅ | – |
| 9 | UML you'll actually use: class & sequence diagrams | 🟢 | – | – |
| 10 | From requirements to classes: the noun/verb method | 🟡 | ✅ | – |
| 11 | Strategy pattern: swap the algorithm at runtime | 🟡 | ✅ | LB strategies (S2·8) |
| 12 | Factory pattern: stop calling `new` everywhere | 🟡 | ✅ | – |
| 13 | Observer pattern: when one change must notify many | 🟡 | ✅ | News feed (S2·26) |
| 14 | State pattern: model behaviour that changes with state | 🔴 | ✅ | Chat ticks (S2·27) |
| 15 | Decorator pattern: add features without subclass explosions | 🟡 | ✅ | – |
| 16 | Singleton (and why it's often a trap) | 🟡 | ✅ | – |
| 17 | Builder & Adapter: the two everyday workhorses | 🟡 | ✅ | – |
| 18 | Build an LRU cache (HashMap + doubly-linked list) | 🔴 | ✅ | Caching (S2·10) |
| 19 | Build a rate limiter (token bucket / sliding window) | 🔴 | ✅ | Rate limiting (S2·21) |
| 20 | Build a circuit breaker (closed / open / half-open) | 🔴 | ✅ | Resilience (S2·23) |
| 21 | Design a parking lot (the classic warm-up) | 🟡 | ✅ | – |
| 22 | Design BookMyShow seat booking (no double-booking) | 🔴 | ✅ | Idempotency/locking (S2·22) |
| 23 | Design Splitwise (who owes whom — the graph) | 🔴 | ✅ | – |
| 24 | Design a food-ordering cart & order (Swiggy, at class level) | 🟡 | ✅ | Putting it together (S2·30) |
| 25 | Design a URL shortener at class level (encode/decode/store) | 🟡 | ✅ | URL shortener (S2·25) |

### Recurring mental models (Season 3)

| Metaphor | Introduced | Reused in | Explains |
|---|---|---|---|
| **A thing with buttons** (remote, washing machine) | Ep 1 | 2, 3 | Object = state + behaviour; encapsulation |
| **Lego vs a moulded toy** | Ep 4 | 12, 15, 17 | Composition over inheritance; building from small parts |
| **A job description** (one role, done well) | Ep 6 | 7, 8 | Single Responsibility / clean boundaries |
| **A vending machine** (states & transitions) | Ep 14 | 20, 22 | State machines |
| **Swappable drill bits** | Ep 11 | 12, 13 | Strategy / pluggable behaviour |

> **Status:** Season 3 (LLD) is sequenced. Same research-dossier gate as Season 2
> — each episode authored only after its dossier (one lens, the LLD lens) exists.
> Built **after** Season 2 ships, but planned now so the two seasons cross-link
> cleanly. The "S2 HLD link" column above is the same pairing shown in Season 2's
> cross-link table, from the LLD side.

## Future seasons (placeholders)

- **Season 4 — DevOps** (CI/CD, containers, Kubernetes, observability, infra-as-code).
- **Season 5 — Security** (auth, encryption, OWASP, the UPI-fraud thread from S1).

Both reuse the same format, style, and pipeline; teardowns of Indian product/infra
teams as the worked examples.
