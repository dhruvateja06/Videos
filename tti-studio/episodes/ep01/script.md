# Ep 01 — What even *is* a "system"? · Narration Script (v2, humanized)

> Long-form (16:9), ~10 min. Faceless — Dhruva voiceover, joyful/conversational.
> **Read it out loud.** Spoken rhythm, one thought per line. Each `▸` is a visual
> reveal (matches a deck click point). No on-screen directions in the read.
> Scene windows are approximate — `sync_build.py` re-times every scene to the
> measured narration, so don't worry if a scene runs a little long or short.
> Running example threaded throughout: **baby Instagram**. Analogies: house
> blueprint, the librarian, footbridge-vs-highway, the ticket counter.

---

## 1 · HOOK
▸ It's 8pm. You flop onto your bed, pull out your phone, and open your favourite app.
And here's the wild part. At that same second, half your city is doing the exact same thing.
Millions of taps, all at once.
And the app? It just works. No crash, no spinning wheel.
Ever stopped to wonder how that's even possible?
Stick around, because by the end of this video you'll understand it completely. Not by memorising anything. By building one yourself.
▸ Meet our project for the whole series. A tiny photo app. We'll call it baby Instagram.
▸ It does two things. You post a photo. Your friends see it. That's the entire app. And it's all we need to learn how the big ones work.

## 2 · THE QUESTION
▸ Hold on to that 8pm picture. A whole city, tapping at once. And nothing breaks.
That isn't luck, and it certainly isn't magic.
Somebody sat down, long before launch, and planned for that crowd. They worked out where everything goes, and how it all holds together under pressure.
▸ That invisible plan is system design. And it might be the most useful thing you'll ever learn as an engineer.

## 3 · WHAT IT ACTUALLY IS
▸ So let's get the definition out of the way, in plain English.
System design is planning how the pieces of your app fit together, before you write a single line of code.
The easiest way to picture it is building a house.
▸ Writing code is laying the bricks. It's the actual construction. Real, important work.
▸ System design is the blueprint. Where do the rooms go? Where do the pipes run? You draw that first, because nobody builds a house and figures out the bathroom afterwards. Software is no different.

## 4 · MEET BABY INSTAGRAM
▸ Right. Let's actually design our baby Instagram. And we're keeping it tiny on purpose.
▸ One simple screen. A feed, and a button to post.
Here's the secret: the small version teaches you the exact same ideas as the giant version, just without the headache.
▸ So, two jobs. One, post a photo. Two, see your friends' feed. Everything we build from here serves those two buttons.

## 5 · THE THREE PIECES
▸ Now the big idea. The one that, once it clicks, you'll start seeing everywhere.
Almost every app you have ever used is really just three pieces, talking to each other.
▸ The first piece is the client. That's a fancy word for your phone. The thing in your hand, showing you the app.
▸ The second is the server. That's the app's brain, running on a powerful computer in some data centre, maybe a thousand kilometres away.
▸ The third is the database. Picture a giant, very organised filing cabinet, where every photo and every caption actually lives.
▸ Client, server, database. Hold on to those three, because every episode after this one is built on top of them.

## 6 · REQUEST & RESPONSE
▸ So we've got our three pieces. What do they actually do all day? One thing, again and again.
▸ Your phone asks for something. "Show me the latest photos." That little ask has a name. It's called a request.
▸ The server hears it, goes and gets what's needed, and sends it back. That return trip is called a response.
The easiest way to feel this is to picture asking a librarian for a book. You ask. They walk to the shelf. They bring it back to you.
You're the client. The librarian is the server. And the shelf full of books is the database.
▸ One request, one response. That tiny back-and-forth is, quite literally, every app you've ever opened.

## 7 · THE REQUEST'S JOURNEY
▸ Let's slow it right down and follow one single tap, step by step.
▸ You tap to open your feed. Your phone sends a request off to the server. That's the first hop.
▸ The server doesn't keep the photos itself, so it turns around and fetches them from the database. Second hop.
▸ Then the whole thing travels back. Database, to server, to your screen, and the photo appears. All of that in a fraction of a second.
▸ And this is the heart of the whole episode. That exact path is hiding inside every app you use. Once you've seen it, I promise, you can't unsee it.

## 8 · THE FOUR STEPS
▸ So how do real engineers design something like this? Do they just start typing? Not a chance.
They follow the same four steps, every single time.
▸ Step one, requirements. What are we building, and who for?
▸ Step two, high-level design. Sketching the big boxes.
▸ Step three, core components. Zooming into each box to see how it works.
▸ Step four, scale. Making sure it survives a crowd.
▸ And here's the fun part. We're going to run all four, right now, on baby Instagram.

## 9 · STEP 1 · REQUIREMENTS
▸ Step one. Requirements. That's a serious-sounding word for a simple question: what should the app do?
▸ It should let you post a photo.
▸ And it should let you see your friends' feed. Easy so far.
But here's the bit beginners rush past. You also have to ask: for how many people?
▸ Because ten friends...
▸ ...and ten million users are not the same project. Not even close.
▸ Same app on the screen, completely different problem underneath. One's a little footbridge. The other's a national highway. You'd design those very differently.

## 10 · STEP 2 · HIGH-LEVEL DESIGN
▸ Step two. High-level design. Big name, gentle idea. You just draw the boxes, and connect them.
▸ Here's our phone, the client.
▸ Here's the server.
▸ And here's the database, all wired together.
▸ That's the whole move. This simple bird's-eye picture is your high-level design. The map of the system, before any of the detail.

## 11 · STEP 3 · CORE COMPONENTS (HLD vs LLD)
▸ Step three. Core components. Now we zoom inside one of those boxes.
▸ The boxes and how they connect, that wide view, is called high-level design. HLD. The map.
▸ But the fine detail of how one single photo gets stored inside the database, that close-up, is low-level design. LLD. The street view.
▸ Same system, two zoom levels. Today, we're happily staying up on the map.

## 12 · STEP 4 · SCALE
▸ And now, step four. Scale. This is where it gets really fun.
▸ Picture ten million people opening baby Instagram at 9pm. That one little server we drew? It melts. Completely overwhelmed. Think of one ticket counter facing an entire stadium.
▸ So what do we do? We add more servers. A whole row of them, splitting the crowd between them. That trick has a name: scaling out.
▸ And the photos everyone's asking for? We keep ready-made copies close by, in something called a cache, so we're not bothering the database every single time.
▸ More servers, plus a cache. And just like that, green lights. We're healthy again.

## 13 · THE TRADE-OFF
▸ But here's the move that makes you sound like a real engineer. You don't build all of that on day one.
▸ Start simple. One server. Ship it. Watch what real people actually do with it.
▸ Then add a new piece only when something actually breaks. Not a second sooner. You wouldn't pour a six-lane highway for a street with three houses on it.

## 14 · THIS IS REAL · HOTSTAR
▸ And if part of you is thinking "sure, but this is just a toy example", it really isn't.
▸ When Hotstar streamed the 2023 World Cup final, fifty-nine million people were watching at the very same moment.
▸ Fifty-nine million. And it held. It's the exact same request and response you just learned. There were simply a lot more boxes working behind the scenes.

## 15 · RECAP + CLIFFHANGER
▸ And that's it. I mean it, you just designed an app. Let's lock in what you know.
▸ Every app is a client, a server, and a database.
▸ They talk in one request, one response.
▸ Engineers design in four steps, every time.
▸ And you scale only when something breaks.
▸ But one sneaky question is left hanging. Your phone asked the server... so how did it even find that server, out of the entire internet? That's DNS and HTTP, and that's exactly where we pick up next time. See you there.

---

**Delivery notes.** Talk, don't read. Pause at each line break. Keep it warm and a
little playful, like you're genuinely delighted to show someone this for the first
time. Let three moments land with a beat of silence after them: "it just works,"
"that's system design," and "fifty-nine million." Lift the energy on the four
steps (8) and on scale (12); soften and slow for the recap (15). The whole read
should feel quick and bright, never lectured.
