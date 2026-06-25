# SD Ep 1 — "Introduction to System Design" · Teleprompter Script

> **Voice:** conversational, warm, a friend explaining — not a narrator reading slides.
> Contractions, direct "you", rhetorical questions, short punchy lines mixed with
> longer ones. It should sound like one continuous talk, not 13 paragraphs.
> **Read this clean** — no animation directions on screen (per PIPELINE.md).
> Pace ≈ 140 wpm. Pause at each `———` (that's where the slide advances).
> Total ≈ 7.5 min.

---

**[1 · TITLE]** *(~16s)*

Alright — let's talk about system design. It's the thing every tech interview seems obsessed with… and honestly, the thing that sounds way scarier than it actually is. So forget the scary version. We're not going to memorize definitions today. We're going to actually *get* it — by building something together.

———

**[2 · THE HOOK]** *(~42s)*

Here's the question this whole topic is really about. How does one app — Instagram, Swiggy, whatever you've got open right now — handle *millions* of people at the same time, and just… not fall over? You'd think there's some genius sitting in a control room making it all work. There isn't. It's design. Smart decisions, made ahead of time. And the fastest way to understand those decisions is to build a tiny version yourself. So that's our project for today. We're going to design a baby Instagram. You post a photo, your friends see it. That's it. Let's build it.

———

**[3 · WHAT IS SYSTEM DESIGN]** *(~30s)*

So first — what even *is* system design? Here's the simple version: it's planning out the pieces of an app, and how they fit together, *before* you build it. Think of it like this. Writing code is laying bricks — making one wall, one feature, actually work. System design is the architect's blueprint — figuring out what the whole building looks like before anyone touches a single brick. And today, you're the architect.

———

**[4 · THE MENTAL MODEL]** *(~38s)*

Now here's the little secret that makes all of this click. Underneath, almost every app you use is really just *three* things. There's you — your phone. We call that the client. There's the app itself, running on some computer far away. That's the server. And there's the place where all your photos and data actually live. That's the database. You ask, the app answers. That "ask" has a name — it's a request. And the answer is the response. Request, response. That back-and-forth? That's the heartbeat of every single app on your phone.

———

**[5 · THE FOUR STEPS]** *(~28s)*

Okay, so how do real engineers actually design this stuff? Here's the good news — they don't just wing it. They follow the same four steps, every single time. Figure out the requirements. Sketch a high-level design. Design the core pieces. And then, scale it. Some people call this the "system design life cycle" — fancy name, simple idea. And we're going to run all four steps, right now, on our baby Instagram.

———

**[6 · STEP 1 — REQUIREMENTS]** *(~32s)*

Step one — requirements. Before you build anything, you ask two questions. First: what should it actually do? That one's easy — post a photo, and see your friends' photos in a feed. But here's the question beginners always skip, and it's the one that matters most: for *how many* people? Because designing this for ten friends, and designing it for ten *million* users… those are completely different problems. "How many" isn't a tiny detail. It quietly decides everything else.

———

**[7 · STEP 2 — HIGH-LEVEL DESIGN]** *(~28s)*

Step two — the high-level design. This is the fun part: we grab a whiteboard and start drawing boxes. Your phone talks to the server. The server saves your posts and captions in the database. And the actual photo files? Those are big, so they get their own storage. Boxes, and arrows between them. That's genuinely all it is — and this little whiteboard sketch even has a name. It's called the high-level design.

———

**[8 · STEP 3 — CORE COMPONENTS]** *(~36s)*

Step three — we zoom into the pieces. Let's pick just one box: the feed. When you open the app, your phone fires off a little message to the server — basically, "hey, give me the latest photos." The server thinks for a moment, and sends them back. And that tiny gap — between you asking and the photos actually showing up — meet a word you're going to hear *constantly* in system design: latency. That's all it means. The wait. The lag you can feel. And a huge part of good design is just fighting to keep that wait as small as possible.

———

**[9 · STEP 4 — SCALE IT]** *(~46s)*

And step four — this is the big one — scaling. So far everything's working beautifully… for your ten friends. But let's say your app blows up. It's 9pm, and now ten *million* people open it at the exact same time. That one little server we drew? It melts. Instantly. So what do we do? Two things. First, we add more servers to share the crowd — that's called scaling out. And second, we keep the most popular photos sitting right nearby, ready to go, in something called a cache — or a CDN. And that question of how many people you can serve every second? That's got a name too — throughput. So: more users, more boxes. But honestly? Same simple idea you already understand.

———

**[10 · RECAP]** *(~22s)*

And… that's it. Seriously — stop for a second, because something just happened here. You just did system design. Requirements, high-level design, components, scale. That's the entire loop. Decide the pieces, connect them, and keep the whole thing fast and standing as it grows. That, right there, is the whole game.

———

**[11 · HLD vs LLD]** *(~36s)*

Now, one more idea before we wrap — because you're going to hear these two terms absolutely everywhere. Everything we just did — drawing the boxes — that's called high-level design. HLD for short. But you can also go the other way: zoom all the way *in*, open up a single box, and design the actual code inside it — like exactly how one post gets built and saved. That's low-level design — LLD. Same craft, just two different zoom levels. We're starting with the boxes, because that's where it all makes sense. We'll get to the code in a later season.

———

**[12 · THE REAL WORLD]** *(~28s)*

And just so you don't think this is only a toy example — it's really not. These exact four steps run the biggest apps in the country. When Disney+ Hotstar streamed the 2023 World Cup final, fifty-nine million people were watching at the very same moment. Fifty-nine million. And it's the same request and response you just learned — only scaled out massively, with a whole lot more boxes.

———

**[13 · OUTRO]** *(~32s)*

So here's where you stand right now. You can pick up your phone, open literally any app, and actually picture the boxes working behind it. That's pretty great for one video. And from here, we're going to crack open every one of those boxes — load balancers, caching, databases, queues — one at a time, nice and slow. Next up, we follow a single tap all the way through: what *really* happens the moment you open Swiggy. If this made system design feel even a little less scary, do me a favour — subscribe, and stick around. We're building this whole thing together, one box at a time. See you in the next one.
