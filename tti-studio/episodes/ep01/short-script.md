# Ep 1 — 3-min Vertical Short · Narration Script (v4 · TTS-synced)

> 9:16 short, **2:31** (151s). This is the **exact** narration baked into
> `short-3min.mp4` — the video's animations are timed to this read, scene by
> scene. **Read it out loud**; it's written in spoken rhythm, one thought per
> line. Threads the "baby Instagram" example throughout. Captions sit in the
> bottom ~25% (kept clear in the composition).
>
> Each scene below shows its **window** (start–end) so a re-record lands in sync.
> The voice starts ~0.6s after each scene begins and finishes with ~1s to spare.

---

**[1 · HOOK — meet the app]** · 0:00–0:22
It's 8pm.
You open Swiggy.
So does half your city, all at once.
And the app doesn't crash. It doesn't even lag.
It just works.
Ever wonder how?
That's system design.
And the best way to get it? Build it yourself.
So let's design a tiny app. A baby Instagram.
You post a photo, your friends see it.

**[2 · WHAT IS IT]** · 0:22–0:37
So what is it?
System design is just planning your app's pieces, and how they connect, before you write any code.
Code is laying bricks.
System design is the blueprint.
So before we build, we plan.

**[3 · THE MENTAL MODEL]** · 0:37–0:57
Here's the trick.
Almost every app is really just three things.
Your phone — the client.
The app, on a computer somewhere — the server.
And where your photos live — the database.
You post a photo: your phone asks, the server answers.
That's a request, and a response.
Every app, ever.

**[4 · THE 4 STEPS]** · 0:57–1:11
And to design one, engineers always follow the same four steps.
Requirements. High-level design. Core components. Then scale.
Let's run all four on baby Instagram.

**[5 · STEP 1 · REQUIREMENTS]** · 1:11–1:26
Step one, requirements.
What should it do?
Post a photo, and see your friends' feed.
But here's what beginners skip.
For how many people?
Ten friends, or ten million?
Completely different problems.

**[6 · STEP 4 · SCALE]** · 1:26–1:45
Now, scaling.
Ten friends? One server is fine.
But ten million at 9pm? That server melts.
So we add more servers to share the crowd. That's scaling out.
And we keep the popular photos nearby, in a cache.
More users, more boxes. Same idea.

**[7 · HLD vs LLD]** · 1:45–2:00
Two words you'll hear everywhere.
The boxes we drew? That's high-level design. HLD.
The code inside one box? Low-level design. LLD.
Same job, two zoom levels.

**[8 · REAL SCALE]** · 2:00–2:16
And this is real.
When Hotstar streamed the 2023 World Cup final, fifty-nine million people were watching, at the same moment.
The same request and response.
Just a lot more boxes.

**[9 · OUTRO]** · 2:16–2:31
And that's it. You just designed an app.
Decide the pieces, connect them, keep it fast and standing as it grows.
That's system design.
Follow along, and we'll build the whole thing, one box at a time.

---
**Delivery notes:** talk, don't read. Pause at each line break. Let "it just
works" and "fifty-nine million" land. Warm, a little playful. The video is
already timed to this exact wording — if you change a line's length, nudge that
scene's duration in `short-3min.html` to match.
