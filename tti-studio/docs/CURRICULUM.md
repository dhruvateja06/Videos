# The Tech Intern — Curriculum

> The channel covers tech broadly (AI, system design, DevOps, security, …).
> **Season 1 is AI** (30 episodes, fully sequenced below). Later seasons —
> system design, DevOps, security — reuse the same format, style, and pipeline.

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

## Future seasons (placeholders)

- **Season 2 — System Design** (how real apps scale: load balancers, caches,
  queues, databases, CAP, sharding…). Same format; Indian product teardowns
  (how Swiggy/UPI/Hotstar scale) as the worked examples.
- **Season 3 — DevOps**, **Season 4 — Security** — TBD.
