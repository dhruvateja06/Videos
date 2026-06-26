# Ep 1 — 3-min Vertical Short · Narration Script (v2)

> 9:16 short (1080×1920), ~3:10, condensed from the Ep 1 long-form.
> **Silent render** — record this VO (or caption over it). The animation is
> **paced to this script** and **threads the "baby Instagram" running example**
> through every scene. Captions go in the bottom ~25% (kept clear). ≈ 145 wpm.

**[1 · HOOK — meet the app]**
It's 8pm. You — and a lakh other people — all open the same app at once. And it just… works. No crash, no spinning wheel. How? That's system design. And the best way to get it is to build a tiny app ourselves. So here's our project: a baby Instagram — you post a photo, your friends see it. Let's design it.

**[2 · WHAT IS IT]**
First — what even is system design? It's planning your app's parts, and how they fit together, *before* you write a line of code. Writing code is laying bricks. System design is the architect's blueprint. So for our baby Instagram, before we build anything, we plan.

**[3 · THE MENTAL MODEL]**
Here's the trick that makes it click. Underneath, our app is really just three things. Your phone — the client. The app itself, on a server somewhere. And a database, where every photo and caption is saved. You post a photo: your phone *asks*, the server *answers* and saves it. That ask-and-answer? A request, and a response. That's every app, ever.

**[4 · THE 4 STEPS]**
Now, to design any system, engineers follow the same four steps. Requirements. High-level design. Core components. Then scale. And we're going to run all four on baby Instagram, right now.

**[5 · STEP 1 · REQUIREMENTS]**
Step one — requirements. What should it do? Post a photo, and see your friends' feed. Easy. But here's the question beginners skip: for *how many* people? Designing this for ten friends, and for ten *million* users, are completely different problems. "How many" quietly decides everything else.

**[6 · STEP 4 · SCALE]**
So let's jump to scale. Ten friends? One server is fine. But it's 9pm and ten million people open baby Instagram at once — that one server melts. Two fixes. Add more servers to share the crowd — that's scaling out. And keep the popular photos sitting nearby, in a cache. More users, more boxes — same idea.

**[7 · HLD vs LLD]**
And you'll hear two words everywhere. Drawing these boxes — that's high-level design, HLD. Opening one box to write its actual code — like exactly how a single *post* gets stored — that's low-level design, LLD. Same craft, two zoom levels. We start with the boxes.

**[8 · REAL SCALE]**
And this isn't a toy. These exact ideas run the real thing. Hotstar streamed the 2023 World Cup final to fifty-nine million people — all watching at the very same moment. The same request and response you just learned. Just a lot more boxes.

**[9 · OUTRO]**
And that's it — you just designed an app. Decide the parts, connect them, keep it fast and standing as it grows. That's system design. Follow along — we build the whole thing, one box at a time.

---
**Delivery notes:** energetic but clear; pause before each new section; lean into
"a lakh people", "melts", "fifty-nine million". The hook must land in 3 seconds.
