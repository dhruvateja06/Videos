# Ep 1 — 3-min Vertical Short · Narration Script (v3 · conversational)

> 9:16 short, ~3 min. **Read this out loud** — it's written in spoken rhythm, one
> thought per line, so it teleprompts cleanly. Don't read it like a paragraph.
> Threads the "baby Instagram" example. Captions go in the bottom ~25%.

**[1 · HOOK — meet the app]**
It's 8pm.
You open Swiggy to order dinner.
And so does half your city, at the exact same time.
But the app doesn't crash. It doesn't even lag.
It just… works.
Ever stopped to think about how?
That right there? That's system design.
And the best way to actually get it isn't reading about it. It's building it.
So that's the plan today. We're going to design a tiny app together. A baby Instagram. You post a photo, your friends see it.
Let's go.

**[2 · WHAT IS IT]**
So, system design.
Simplest way to put it: it's planning out the pieces of your app, and how they fit together, before you write a single line of code.
Think of it like this.
Writing code is laying the bricks.
System design is the architect, drawing the blueprint first.
So before we build our baby Instagram, we plan it.

**[3 · THE MENTAL MODEL]**
Here's the part that makes it all click.
Under the hood, almost every app is really just three things.
There's you. Your phone. That's the client.
There's the app itself, running on a computer somewhere far away. That's the server.
And there's the place all your photos get saved. The database.
You post a photo, your phone asks, the server answers and saves it.
That little back-and-forth has a name. A request, and a response.
And honestly? That's every app you've ever used.

**[4 · THE 4 STEPS]**
Okay, so how do engineers actually design this stuff?
Good news. They don't just wing it.
They follow the same four steps, every single time.
Figure out the requirements. Sketch the high-level design. Build the core pieces. Then scale it.
And we're going to run all four on our baby Instagram. Right now.

**[5 · STEP 1 · REQUIREMENTS]**
Step one. Requirements.
Before you build anything, you ask two questions.
First: what should it actually do?
Easy. Post a photo, and see your friends' feed.
But here's the one beginners always skip.
For how many people?
Because building this for ten friends, and building it for ten million, are completely different problems.
"How many" quietly decides everything else.

**[6 · STEP 4 · SCALE]**
So let's jump to the fun one. Scaling.
Ten friends? One server handles it, no sweat.
But it's 9pm, and ten million people open baby Instagram at the same second.
That one little server? It melts.
So we do two things.
We add more servers to share the crowd. That's scaling out.
And we keep the popular photos sitting close by, ready to go, in a cache.
More people, more boxes. Same simple idea.

**[7 · HLD vs LLD]**
Quick one, because you'll hear these two everywhere.
Drawing the boxes, like we just did? That's high-level design. HLD.
Cracking open one box to write its actual code? Like exactly how a single post gets stored? That's low-level design. LLD.
Same job, two zoom levels.
We're starting with the boxes.

**[8 · REAL SCALE]**
And look, this isn't just a toy example.
When Hotstar streamed the 2023 World Cup final, fifty-nine million people were watching. At the same moment.
Fifty-nine million.
And it's the exact same request and response you just learned. Just… a lot more boxes.

**[9 · OUTRO]**
And that's it. You just designed an app.
Decide the pieces, connect them, keep the whole thing fast and standing as it grows.
That's system design.
Stick around. We're building this whole thing together, one box at a time.

---
**Delivery notes:** talk, don't read. Pause at each line break. Let "it just…
works" and "fifty-nine million" land. Keep it warm and a little playful.
