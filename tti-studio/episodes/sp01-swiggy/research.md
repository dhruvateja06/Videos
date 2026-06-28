# Sunday Special #1 — Swiggy · Deep Research Brief

> **How Swiggy actually works, end to end** — for a 15–20 min teardown video.
> Research pass: 104 agents fanned out across Swiggy's engineering blog and
> credible teardowns; 49 falsifiable claims extracted, 25 adversarially
> verified (3-vote), **18 confirmed · 7 explicitly refuted.**
> Last updated: 2026-06-28.

> **Reading guide.** "Confirmed" = primary Swiggy engineering source, 3-0
> verified. "Inferred" = strongly implied but not in a confirmed quote. "Open"
> = not surfaced by this research pass (needs targeted follow-up). **Date
> every fact** — most architecture detail is era-stamped 2023–2026 and the
> systems keep evolving.

---

## 0 · The system at a glance

Swiggy is a three-sided marketplace — **customer · restaurant · delivery
partner** — running on a microservices backbone. An order moves through a
state machine: cart → placed → restaurant-accepts → rider-assigned → picked
up → delivered. Every customer-facing **pre-order page** (home, listings,
search, restaurant menu, checkout) is gated by one critical-availability
service called **Serviceability**, which must answer "can we deliver to this
exact point right now?" in <200ms — failing it means Swiggy stops taking
orders. The customer's delivery-time promise and the live tracking ETA are
two *separate* ML systems. Real-time data flows on **Apache Kafka** (now
Confluent-managed, since Mar 2025) fed by Change Data Capture from
service databases. UPI payments are now **in-app** (Aug 2024, Juspay
HyperUPI). Instamart (quick commerce) uses a different fulfilment model —
**8,000–10,000 sq ft "mega dark stores"** offering staggered 10/20-min
delivery windows.

What this brief is solid on:
- Serviceability (the gating spatial index)
- The 4-leg ETA ML system
- The real-time data platform (Kafka + CDC + Flink)
- Swiggy UPI
- Instamart megapods

What this brief still has **open questions** on (see §7):
- The dispatch/assignment algorithm itself
- The rider functional side (onboarding, surge, incentives)
- The restaurant functional flow (partner-app handshake, POS, kitchen)
- Search / home-feed ranking models
- Live-tracking transport infra

---

## 1 · The customer journey

### Opening the app → Serviceability

The moment you tap the app icon, a single backend platform decides whether
Swiggy can do anything for you: the **Serviceability platform**. It runs on
*every* pre-order page — home, listings, search, restaurant menu, checkout —
not just at order placement. **If Serviceability fails, Swiggy can't take
new orders.** ✓ *(Confirmed, primary)*

How it answers "can we deliver to your point?" at massive scale:

1. Restaurants/stores are pre-clustered into thousands of delivery
   **polygons**, organised in an **in-memory GeoHash index**.
2. Your lat/lng is hashed → the index returns a *small* candidate set of
   overlapping clusters.
3. Only on that small set does the expensive **Point-in-Polygon (PIP)**
   check run.

GeoHash is a coarse filter; PIP is the precise answer. Brute-forcing PIP on
every polygon would be too slow. ✓ *(Confirmed, primary)*

**The scale this has to absorb** (Swiggy's own design figure, 2023):
- ~100k app visits/min at peak × ~2,000 nearby pickup locations per visit
- = ~**200 million serviceability evaluations per minute**
- at **P99 < 200ms**

Caveat for the script: 200M is Swiggy's design back-of-envelope (the product
of two planning assumptions), not audited prod telemetry. Still
hold-your-coffee scale. ✓ *(Confirmed; flag as design figure)*

### Restaurant discovery, search, home-feed ranking

How the home feed orders restaurants for *you* — and how search ranks
results — was requested but **not confirmed by this research pass**.
Swiggy has published two relevant posts (`evolution-of-and-experiments-with-
feed-ranking` and `learning-to-rank-restaurants`) but the fetcher timed
out on both. → **Open question §7-A.**

### Menu, cart, checkout, payments

The cart triggers the **pre-order ETA (the "at-cart SLA promise")** — an ML
prediction shown to you *before* you place the order. (Details in §4.)

Payments now have a notable wrinkle: **Swiggy UPI** (launched **14 Aug 2024**)
keeps the entire UPI flow inside Swiggy — no redirect to a UPI app.
Technically it's powered by **Juspay's HyperUPI plugin**, integrating
NPCI's UPI Plug-in solution. Swiggy markets the experience as "5 steps to 1."
✓ *(Confirmed, primary)*

⚠ **Do NOT use:** the "15s → 5s transaction time" number floating around —
the verifier refused to confirm it (1-2). Cite the 5→1 step claim instead,
and frame it as Swiggy's own characterisation. After the one-time bank
linking, each transaction still requires a UPI PIN.

### Live order tracking + the post-order ETA

After placement, the cart promise is replaced by a **post-order tracking
ETA** built on top of the promise and refined as the order progresses.
That's a *different* ML system. (Details in §4.) ✓ *(Confirmed, primary)*

**Open:** how the rider's GPS *physically reaches your map* (WebSocket?
long-polling? push?) — refuted as a generic pattern, real implementation
unknown. → §7-E.

### Ratings, refunds

Not covered by this research pass. Low-priority for the teardown.

---

## 2 · The restaurant side

**Almost entirely an open question.** Verified primary sources gave us
exactly one restaurant-side detail: **"restaurant stress"** is a paramount
ETA feature (more on that in §4). The rest — how the order reaches the
partner-app, accept/reject, POS integrations, kitchen workflow,
menu/inventory management — was not surfaced. → **Open question §7-C.**

For the script, we should either:
- Do a second targeted research pass on Swiggy's restaurant-side blog posts
  (the "tech-that-brings-you-your-food" piece looks promising but timed out), or
- Frame it as "we couldn't get authoritative sources on this side — here's
  what's publicly known from press / partner docs." Less satisfying.

---

## 3 · The delivery partner (rider) side

Mostly an **open question** at the functional level (onboarding, going
online, earnings, incentives, surge). What *was* confirmed is how the
**rider's GPS data is turned into ETA features**:

- Delivery-executive (DE) GPS pings are **bucketed into time windows**.
- **Outlier pings are screened** out.
- **Distance travelled** in each window = sum of **Haversine distances
  between successive pings**.
- **Speed** = cumulative distance ÷ (last-ping time − first-ping time).

This is the feature engineering underlying real-time rider tracking + the
Last-Mile ETA model. Standard, not exotic — but it's the actual recipe. ✓
*(Confirmed, primary)*

Everything else on the rider side — **the dispatch algorithm that picks
which rider gets your order, the batching/clubbing logic, the surge
mechanic** — is the biggest open question in this brief. → §7-B & §7-D.

---

## 4 · The ETA ML system — the cleanest story in this brief

The customer-facing delivery time is **two separate ML systems**, not one:

### Stage A — the "at-cart SLA promise" (pre-order)
Shown to you in the cart, before you tap "Place order." Uses:
- traffic
- **restaurant stress** (see below)
- delivery-partner availability
✓ *(Confirmed; the cart-time blog itself timed out, but the
predicted-SLA concept was confirmed via a corroborated third-party
teardown that quotes the primary)*

### Stage B — the post-order **tracking-screen ETA**
**Built on top of** the at-cart promise. Refines it with real-time signals
as the order progresses. Refreshed at **fixed intervals**. ✓

It does NOT predict the whole journey in one shot. It **decomposes the
journey into four legs** and trains a **separate neural-net model per leg**:

| Stage | Acronym | What it predicts |
|---|---|---|
| **O2A** | Ordered-to-Assignment | Time until a rider is assigned |
| **FM** | First Mile | Rider → restaurant |
| **WT** | Wait Time | Rider waiting at restaurant (kitchen lag) |
| **LM** | Last Mile | Restaurant → you |

Why four models instead of one? **"The model feature space varies for the
different stages of an order."** Each leg has different signals: O2A cares
about supply/demand around the rider pool; FM/LM care about traffic + rider
movement; WT cares about kitchen state. ✓ *(All 3-0 confirmed, primary)*

**Model details (as of May 2023):** each leg is a feed-forward neural net,
**4 hidden layers, Leaky ReLU, 50 epochs, ADAM** optimizer. They migrated
*to* neural nets *from* gradient-boosted trees because the feature spaces
diverged. ✓ (Caveat: this is 2023; architecture has almost certainly
evolved.)

### The two stress features that matter
Both confirmed primary. These are the explainability hook the teardown
should hammer:

| Feature | Definition |
|---|---|
| **Restaurant stress** | orders placed vs orders prepared — "deviation from general behaviour." On a weekend dinner peak, *"even a small new order might take high preparation times due to kitchen stress."* |
| **System stress** | active delivery executives vs active orders. |

This is the cleanest "wow" beat in the whole research — the ETA isn't just
distance ÷ speed, it's *modelling the kitchen's mood*. Great teardown moment.

---

## 5 · The technical stack

### Real-time data — Kafka + CDC + Flink

The streaming spine, confirmed against Swiggy's own CDC blog + secondary
sources:

- **Apache Kafka** = the durable message queue.
- Fed by **Change Data Capture** from service databases — **MySQL (on
  AWS RDS)** via binlog tools (Maxwell / Debezium / AWS DMS), and
  **DynamoDB** via DynamoDB Streams.
- **Apache Flink** does sub-second processing (Swiggy's internal real-time
  alerting platform "Rill" is built on it).
- **Migrated from self-managed Kafka → Confluent Cloud** (announced 4 Mar
  2025). Stated reason: escape the **maintenance/hardware burden** of running
  Kafka in-house. ✓ *(Confluent migration via Confluent's customer page +
  multiple secondary trade press)*

⚠ Flag carefully: Confluent's "elastic scaling absorbs festival peaks"
line is **vendor marketing**, single-sourced. Use it as Confluent's
statement, not as independently confirmed engineering fact.

⚠ **Do NOT use:** "Swiggy's order load jumps from 100 to 15,000 orders/min
at peak" — explicitly refuted 0-3. Don't put fake-looking numbers on screen.

### Dispatch / order-to-rider matching

**The single biggest open question.** Despite this being the heart of any
Swiggy teardown, *no surviving confirmed claim describes the matching
algorithm, the batching/clubbing logic, or the optimisation objective.*

Swiggy *has* published on this — the bytes.swiggy.com URLs
`logistic-zones-for-assignment` and `the-tech-that-brings-you-your-food`
look directly relevant — but the fetcher timed out on both. → **§7-B.**

The teardown can't ship without this. Recommend a second targeted research
pass before scripting (see §8).

### Search / home-feed ranking

Same story. `learning-to-rank-restaurants` and `evolution-of-and-experiments-
with-feed-ranking` are Swiggy's own posts; fetches timed out. → §7-A.

### Demand forecasting / surge

`hyperlocal-forecasting-at-scale-the-swiggy-forecasting-platform` is the
relevant Swiggy post; timed out. → §7-D.

⚠ **Do NOT use** any "millions of predictions per second" ML-platform
number — refuted 1-2.

---

## 6 · Instamart (quick commerce)

Different fulfilment model from the food-delivery app. The headline shift,
confirmed via a named CFO quote + multiple corroborating outlets:

- Swiggy is rolling out **"mega dark stores" / "megapods"**: **8,000–10,000
  sq ft** each (newer ones 10–12k sq ft), equivalent to 2–3 conventional
  dark stores.
- Each megapod covers roughly a **2 km radius**, holds up to **40–50k SKUs**.
- Enables **"assorted" / staggered delivery windows**: some items in
  ~10 min, others within ~20 min — a deliberate shift from "everything in
  10 min."
- Source: CFO Rahul Bothra to Inc42 + Swiggy's own press; Q2 2025 ~half of
  40 new dark stores were megapods. ✓ *(Confirmed, primary CFO quote)*

⚠ **Do NOT use:** "Instamart pilot launched Sept 2020, 45-min promise,
Bengaluru + Gurgaon, 7am–1am" — refuted 0-3.
⚠ **Do NOT frame** Instamart as "hub-and-spoke micro-fulfillment pods" —
that framing was refuted 1-2.

---

## 7 · Open questions (the gaps in this brief)

These are what we owe a second research pass on **before scripting the
video**. The video can't truthfully claim to "go deep on how Swiggy works"
while leaving these blank.

| # | Topic | Why it matters | Suggested follow-up |
|---|---|---|---|
| **7-A** | Search / home-feed ranking / personalization models | Customer side is incomplete without it | Re-fetch `learning-to-rank-restaurants` + `evolution-of-and-experiments-with-feed-ranking-at-swiggy` |
| **7-B** | **Dispatch / assignment algorithm + order batching/clubbing** | THE heart of a teardown — currently missing | Re-fetch `logistic-zones-for-assignment` + `the-tech-that-brings-you-your-food`; search Swiggy tech-talk videos |
| **7-C** | Restaurant functional flow (partner app, POS, kitchen, accept/reject) | Whole side of the marketplace is dark | Targeted search of bytes.swiggy.com; supplement with Swiggy partner-onboarding docs |
| **7-D** | Demand forecasting + dynamic / surge pricing | Trade-off beat for the teardown | Re-fetch `hyperlocal-forecasting-at-scale-the-swiggy-forecasting-platform` |
| **7-E** | Live-tracking transport infra (how rider GPS reaches your map) | "How tracking works" is on every viewer's mind | Search for Swiggy realtime / pubsub / location-streaming posts |

**Note on the fetch failures:** the verifier repeatedly couldn't load
bytes.swiggy.com / Medium pages via direct fetch (60s timeouts) — they
exist, they're indexable by search, but live fetches stalled. A second
pass with `WebFetch` directly on each URL (one at a time) should land them.

---

## 8 · Refuted claims — keep these OUT of the script

All explicitly killed in the 3-vote verification step. Listing them so we
don't accidentally repeat them from memory or other teardowns:

| ✗ Claim | Vote |
|---|---|
| In-app UPI cuts transaction time from 15s to 5s | 1-2 |
| Predicted SLA is "powered by" Confluent/Kafka (as causal link) | 1-2 |
| Instamart pilot: Sept 2020, 45-min, Bengaluru+Gurgaon, 7am-1am | 0-3 |
| Instamart = hub-and-spoke micro-fulfilment pods | 1-2 |
| Order load jumps 100 → 15,000 orders/min at peak | 0-3 |
| Swiggy ML serving handles >1M predictions/sec | 1-2 |
| Live tracking = drivers → Location Service → WebSocket to customer | 1-2 (generic pattern, not Swiggy's confirmed impl) |

---

## 9 · Sources

**Primary (Swiggy's own engineering blog, verified):**
- [Designing the Serviceability Platform — Part 1](https://bytes.swiggy.com/designing-the-serviceability-platform-at-swiggy-for-high-scale-part-1-751a631f0379)
- [How ML powers "When is my Order coming?" — Part I](https://bytes.swiggy.com/how-ml-powers-when-is-my-order-coming-part-i-4ef24eae70da)
- [How ML powers "When is my Order coming?" — Part II](https://bytes.swiggy.com/how-ml-powers-when-is-my-order-coming-part-ii-eae83575e3a9)
- [Architecture of CDC System](https://bytes.swiggy.com/architecture-of-cdc-system-a975a081691f)
- [Swiggy Launches Swiggy UPI](https://blog.swiggy.com/news/swiggy-launches-swiggy-upi-for-faster-payment-experience/)
- [Juspay HyperUPI Plug-in SDK](https://juspay.io/en-in/blog/juspay-hyper-upi-upi-plug-in-sdk)

**Secondary (corroborating):**
- [Confluent customer story — Swiggy](https://www.confluent.io/customers/swiggy/) *(vendor marketing — use with care)*
- [Inc42 — Swiggy Instamart mega dark store plan](https://inc42.com/features/swiggy-instamart-mega-dark-store-plan-ipo/)
- [Medium — Architecting Swiggy's Real-Time AI Data Platform](https://medium.com/@vsanmed/from-billions-of-events-to-milliseconds-of-insight-architecting-swiggys-real-time-ai-data-a43a2697cdee) *(third-party teardown, claims cross-checked against Swiggy primaries)*

**Open-question targets (fetch timed out — re-try):**
- bytes.swiggy.com/the-tech-that-brings-you-your-food-1a7926229886
- bytes.swiggy.com/logistic-zones-for-assignment-48d9ce06c4a8
- bytes.swiggy.com/learning-to-rank-restaurants-c6a69ba4b330
- bytes.swiggy.com/evolution-of-and-experiments-with-feed-ranking-at-swiggy-17204769e79f
- bytes.swiggy.com/hyperlocal-forecasting-at-scale-the-swiggy-forecasting-platform-c07ecd5f5b86
- bytes.swiggy.com/predicting-food-delivery-time-at-cart-cda23a84ba63
- bytes.swiggy.com/the-swiggy-delivery-challenge-part-one-6a2abb4f82f6
- bytes.swiggy.com/architecture-and-design-principles-behind-the-swiggys-delivery-partners-app-4db1d87a048a

---

## 9b · Addendum — Pass 2 (cheap targeted-search pass)

> Filled most of the §7 gaps via **search-engine snippets** (5 WebSearches,
> after 5 direct WebFetches all timed out — same as Pass 1). Snippets are
> shorter than full posts and don't reproduce every detail, but they're
> verbatim from Swiggy's own engineering blog. Treat as **confirmed primary
> if Swiggy authored, but slightly thinner evidence than Pass 1's full quotes**.

### Dispatch formula (the unlock — §7-B)

From [The Swiggy Delivery Challenge — Part One](https://bytes.swiggy.com/the-swiggy-delivery-challenge-part-one-6a2abb4f82f6):

> **Delivery Time = max(Assignment Delay + First Mile, Prep Time) + Last Mile**

That `max(...)` is everything. The rider getting to the restaurant *in
parallel* with the food being cooked is the cost-saver — whichever finishes
first waits for the other. The assignment algorithm's job is to pick the
rider that **minimises this total**, not just the closest rider. This single
formula is the cleanest "wow" beat for the dispatch section.

### Logistic zones — how Swiggy scales the matching (§7-B)

From [Logistic Zones for Assignment](https://bytes.swiggy.com/logistic-zones-for-assignment-48d9ce06c4a8) (Ritwik Moghe, Core-Logistics DS, Aug 2022):

- A **single citywide** assignment run scales badly — too many orders × riders.
- Solution: **divide the city into logistic zones, run independent assignment
  algorithms per zone, in parallel.** Fewer orders per run → faster runtime,
  enables auto-scaling.
- The trick that keeps this from being sub-optimal: **restaurant embeddings.**
  Train embeddings so that *"orders from restaurants with similar embeddings
  are usually assigned delivery partners from similar locations"* — i.e. the
  zones aren't drawn by city geography alone, they're learned from where
  riders historically deliver each restaurant's orders.
- Goal: **minimise sub-optimal assignments** where a rider gets batched
  across zones. ✓ Primary, snippet-confirmed.

### Order batching / clubbing (§7-B continued)

From the same Part One + general teardown corroboration:

- Batch orders **from the same area**.
- Constraints: rider's current location, time to reach restaurant, expected
  delivery time, **wait time** at restaurant.
- Cost function includes **distance + travel time + wait time + fairness
  across riders**. The fairness term is notable — they're not just
  minimising cost, they're keeping rider earnings balanced. ✓ Primary,
  snippet-confirmed.

### Feed ranking (§7-A) — the actual evolution

From [Evolution of and Experiments with Feed Ranking at Swiggy](https://bytes.swiggy.com/evolution-of-and-experiments-with-feed-ranking-at-swiggy-17204769e79f) (Jairaj Sathyanarayana, Director Data Science):

- Started with **pointwise** ranking (each restaurant scored independently).
- Moved to **Learning to Rank (LTR)** — a *list-aware* method that accounts
  for *"how the probability to order from a given restaurant is impacted by
  what other restaurants are in the list and at what positions."*
- Now being **reformulated as multi-objective optimization (MOO)** — i.e.
  the feed doesn't just maximise click-through, it balances multiple
  objectives (likely: clicks, orders, business metrics).
- Evaluation: **nDCG** + **"proportion of orders from top X positions."**
✓ Primary, snippet-confirmed.

### Two more ranking systems exist (bonus finds)

These weren't in the original research but came up in Pass 2:

- [Using Deep Learning for Ranking in Dish Search](https://bytes.swiggy.com/using-deep-learning-for-ranking-in-dish-search-4df2772dddce) — DISH search (when you search for "biryani") uses a separate deep-learning ranker, distinct from the restaurant-feed ranker.
- [Swiggy Improves Search Autocomplete Using Real Time Machine Learning Ranking](https://www.infoq.com/news/2026/05/swiggy-autocomplete-rt-ranking/) — InfoQ, May 2026. The autocomplete (as you type "bir…") uses **real-time ML ranking** — its own dedicated system.

So there are **at least three ranking systems**: feed (restaurants),
dish-search, autocomplete. Each has its own model. Nice teardown beat:
"Swiggy isn't one ranker, it's three."

### Order modeling — the platform's mental model (§7-C partial)

From snippets of [The Tech That Brings You Your Food](https://bytes.swiggy.com/the-tech-that-brings-you-your-food-1a7926229886):

> *"The engineering team visualized everything as tasks that need to be
> run, making it easier to group each order into a list of **tasks, job
> legs and duties**."*

That's the abstraction: an order isn't a single thing the system tracks,
it's a **bag of tasks** (assign rider, navigate to restaurant, wait at
restaurant, pick up, navigate to customer, drop off). The system schedules
those tasks. Clean teaching abstraction.

### Delivery Partner app — one architectural constraint (§7-B)

From snippet of [Architecture and Design Principles Behind the Swiggy's Delivery Partners App](https://bytes.swiggy.com/architecture-and-design-principles-behind-the-swiggys-delivery-partners-app-4db1d87a048a):

- The DE app **runs in background for ~4–5 hours per session** on average.
- Background-running needs: continuous **GPS tracking** (for assignment +
  customer-facing live tracking + distance-based pay calculation).
- Battery + reliability are first-class concerns — long-session mobile apps
  is its own engineering problem. ✓ Primary, snippet-confirmed.

### Still open after Pass 2

- **Hyperlocal forecasting model architecture** (LSTM? Prophet? hybrid?) —
  search returned no Swiggy-specific snippet. The blog post exists; both
  passes failed to extract. Low-cost option: ship without it, frame surge
  as "they predict demand by zone and time and shift incentives," cite
  the post URL.
- **Live-tracking transport infra** (WebSocket vs push vs polling) —
  Swiggy explicitly hasn't published this detail.
- **Restaurant POS integrations / kitchen workflow** — same.

These three are now small enough gaps that the video can ship around them.

---

## 10 · Notes for the script

- **Date-stamp every architecture detail** (e.g. "as of Swiggy's 2023 blog
  post"). The systems evolve.
- **Frame design figures as design figures**, not prod telemetry (the 200M
  evals/min line).
- **Vendor-marketing lines** ("Confluent absorbs festival peaks") should
  be attributed to the vendor, not stated as engineering fact.
- The **kitchen-stress** beat is the single best teaching hook the
  research surfaced — the ETA is *modelling the kitchen's mood*. Make
  that a payoff moment.
- The **two-stage ETA** (at-cart promise vs tracking-screen) is the second
  cleanest beat — most viewers think it's one number; it's two systems.
- Reuse the System Design series' visual language so this special feels
  like part of the same channel, but mark it visually as the **Sunday
  Special / App Teardown** subseries (different accent or chrome).
