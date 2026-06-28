# Ep 02 — Client, server & the network (DNS & HTTP) · Narration Script (v2)

> v2 changes vs v1:
> - **Branded welcome + Ep01 recap** baked into scene 1 (no more cold open).
> - **Every acronym expanded on first use** — DNS, HTTP, HTTPS, TTL, API, IP,
>   URL, CSR, SSR.
> - **TTL is properly defined** (Time To Live = how long a cached answer is
>   trusted), not just named as a trade-off.
> - Plain-English glosses tightened on first mentions of "resolver," "method,"
>   "header," and "cookie."

> Long-form (16:9), ~14 min, 22 scenes. Faceless — Dhruva voiceover, joyful/brisk.
> Read out loud. Each `▸` is a visual reveal. Restaurant analogy is the spine.
> Running example: Swiggy. Callback: baby Instagram (Ep01).

---

## 1 · WELCOME + RECAP HOOK
▸ Hey, welcome back to The Tech Intern, system design. I'm Dhruva, and this is the show where we build huge apps from scratch, one box at a time.
▸ Last time, we built a baby Instagram, and we found the big secret: every app is really just three pieces. A client, a server, and a database, passing a request back and forth.
▸ But I skipped something sneaky. When your phone sends that request out, how does it even find the right server? Out of billions of computers on the planet?
▸ Tonight we crack those boxes open. What's actually inside "client" and "server," and how they find and talk to each other. So let's order some food. Open Swiggy.

## 2 · TWO QUESTIONS
▸ Everything tonight answers just two questions.
▸ One. What's really inside those words, "client" and "server"? Who does what, and where does your data actually live?
▸ Two. How do they find each other across the whole internet, and how do they talk once they do? Two questions. Let's go.

## 3 · THE RESTAURANT
▸ Here's the one picture to hold in your head all episode. A restaurant.
▸ The dining room is the client. It's where you sit, read the menu, and place your order. Comfortable, friendly. But no food is actually cooked there.
▸ The kitchen is the server. That's where the cooking happens, where the recipes live, and where the pantry, your data, is guarded. You never see it. And the waiter, carrying orders between them? We'll meet him soon.

## 4 · THE CLIENT
▸ So, the client. That's your phone, running the Swiggy app. The dining room.
▸ Its whole job is the stuff you see and touch. It shows you the screen. The restaurants, the photos, the buttons.
▸ It handles your taps and your typing. Scrolling, searching, animating.
▸ And when it needs something real, it asks the server. But notice: it holds no real data of its own. It's just showing you a copy.

## 5 · THE SERVER
▸ Now the kitchen. The server. This is a powerful computer in a data centre, maybe a thousand kilometres away.
▸ It runs the actual logic. The brains of the whole thing.
▸ It enforces the rules. What's allowed, what isn't.
▸ And it owns the data. The database, where every restaurant, every order, every rupee actually lives. The real source of truth.

## 6 · WHERE DATA LIVES
▸ Which brings up the most important idea here. The database is always on the server side. Always.
▸ Your phone only ever holds a temporary copy. Just what's on the screen this very second.
▸ The real, permanent data lives on the server. Pull to refresh, and the truth comes straight from the kitchen. Your phone is a window onto the data, not where it's kept.

## 7 · NEVER TRUST THE CLIENT
▸ And that leads to the golden rule of system design. Say it with me. Never trust the client.
▸ Why? Because anyone can mess with their own phone. Picture a hacked app that claims this order costs one rupee.
▸ The server doesn't just believe it. It re-checks against its own data. The real price is two ninety-nine. Even if you tampered with the app, the kitchen has the final say. Always.

## 8 · THE API
▸ So how do the dining room and the kitchen actually talk? Through a waiter. In tech, we call that waiter an A-P-I. It stands for Application Programming Interface. Long name, simple job. It's the agreed-on way the client asks, and the server answers.
▸ And here's the neat part. The same kitchen can serve many dining rooms.
▸ The iOS app, the Android app, the website. All different clients, all talking to one single backend, through that same API. Why build it this way? Three reasons. Security, so the rules live in one trusted place. Reuse, one backend for every app. And scale, so you can grow each side on its own.

## 9 · CSR vs SSR
▸ Quick question, but an important one. Who actually draws the page you see? There are two answers.
▸ Server-side rendering, S-S-R. The kitchen plates the whole dish and sends it out ready. The page shows up fast, and search engines love it. The catch: more work for the server every time.
▸ Client-side rendering, C-S-R. The kitchen sends raw ingredients and a recipe, and your phone cooks the page itself. Slower to show that first screen, but buttery smooth after. Most big apps do both. First screen from the server, everything after on the phone. A trade-off, not a winner.

## 10 · THE ADDRESS PROBLEM
▸ Okay, question two. Your phone wants Swiggy's kitchen. But there are billions of computers out there.
▸ And all your phone has is a name. swiggy dot com. A name is easy for you to remember.
▸ But the network doesn't move data to names. It moves data to numbers. So we have a little translation problem.

## 11 · THE IP ADDRESS
▸ Because every server on the internet has a number. It's called an I-P address. I-P stands for Internet Protocol. Basically, it's a unique number that picks out one exact machine on the whole network.
▸ Swiggy's might look like this. One-four-two, dot two-fifty, and so on.
▸ Think of it as the server's phone number. This shape is called IPv4. The newer IPv6 ones are much longer, but the idea is the same. A number that points to one exact machine.

## 12 · DNS = THE PHONEBOOK
▸ So how do we get from the name to the number? With the internet's phonebook. It's called D-N-S. That's short for Domain Name System. A domain is just a name like swiggy dot com. So Domain Name System literally means: "the system that looks up domain names."
▸ You type swiggy dot com, and DNS finds the matching number. Just like tapping a saved contact and letting your phone dial it.
▸ You remember the name. DNS remembers the number. You never have to.

## 13 · THE DNS RELAY
▸ But that lookup isn't one quick step. It's more like a relay race, handing a question down the line.
▸ Your device checks first. Do I already have this saved? If not, it asks a helper called the resolver. That's just another computer whose whole job is doing the running around for you.
▸ The resolver asks a root server, who says, "I don't know, but ask the dot-com people." The dot-com server says, "ask Swiggy's own server." And that last one, the authoritative server, finally knows the number. It races all the way back. Root and dot-com never knew the address. They just point you to whoever's next.

## 14 · CACHE + TTL
▸ Now, do you run that whole race every single time? No. The first time, yes. After that, your device just remembers the number.
▸ So the second visit is basically instant.
▸ But here's the question. How long should it remember before checking again? That's controlled by a setting called T-T-L. T-T-L stands for Time To Live. Basically, how long should this answer be trusted before we check again? And it's a trade-off. Set it long, and you save trips, but if the number ever changes, you're slow to find out. Set it short, you're always fresh, but you do more work. Oh, and one myth to kill. DNS only finds the address. It never loads the actual page.

## 15 · HTTP, THE SHARED LANGUAGE
▸ Right. We found the kitchen. Now the dining room and the kitchen need a shared language. That language is H-T-T-P. Short for HyperText Transfer Protocol. Fancy name, simple thing. It's just the agreed-on rules for how a client asks for something and how a server answers.
▸ Your phone sends a request. "Get me the restaurants." The server sends back a response. "Two hundred, OK, here they are."
▸ One ask, one answer. And then it forgets you completely. HTTP keeps no memory between requests. Hold that thought. It matters in a minute.

## 16 · ANATOMY OF A REQUEST
▸ Let's open up that request. Four parts.
▸ The method. That's the verb, what you want done. The path. Which thing you want. The headers. Little labels attached to the request, like who you are or what format you can read. And the body. Any data you're sending up.
▸ And the address itself, the URL, short for Uniform Resource Locator, packs a lot in. The scheme, how to talk, like https. The host, which server. The path, which page. And the query, extra options. Four colours, one line.

## 17 · GET vs POST
▸ Of all those methods, two do most of the work. GET and POST.
▸ GET is for reading. Browsing the menu. It only looks, it changes nothing, and it's safe to do again and again. Its details ride right in the URL, so you can bookmark it.
▸ POST is for writing. Placing the order. It changes something on the server, and its data rides hidden in the body, not the URL. One warning. Send a POST twice, and you might place two orders. We'll fix that double-tap problem in a later episode.

## 18 · HEADERS & COOKIES
▸ Remember how HTTP forgets you after every request? So how does the app keep you logged in? With a cookie. A cookie is just a tiny note your browser stores for a website. Think of it as an ID badge.
▸ You log in once. The server hands your browser a little token. "Set-Cookie."
▸ From then on, every request you send quietly carries that cookie. And the server goes, "ah, it's you again." Still logged in. That's all a session cookie is. A badge that says "it's me."

## 19 · STATUS CODES
▸ Every response also comes stamped with a status code. A quick number telling you how it went.
▸ Two hundred is green. OK, here's what you asked for. Three-oh-one is a redirect. It moved, follow the arrow.
▸ Four-oh-four. Not found. That page doesn't exist, and that one's on your side. Five hundred. Server error. The kitchen itself broke. Easy way to remember: four-something is your fault, five-something is the server's.

## 20 · THE S IN HTTPS
▸ One more letter. The S in H-T-T-P-S. It just stands for "Secure." Plain HTTP is like a postcard. Anyone who handles it on the way can read it. Your card number, right there in the open.
▸ HTTPS is a sealed envelope. Your phone and the server quietly agree on a secret, then scramble everything. To anyone in between, it's gibberish. That's the little padlock.
▸ But careful. The padlock only means the line is encrypted. It does not mean the site is honest. Even scam sites can show a padlock.

## 21 · THE WHOLE JOURNEY
▸ Let's run the whole thing, start to finish. You tap a restaurant on Swiggy.
▸ First, DNS finds the server's number. Then your phone sends a sealed HTTPS request to that server, which checks the rules and pulls the real data from its database.
▸ The answer travels back, and the food appears on your screen. Find the address, knock politely in the right language, get your answer. That, honestly, is the whole web.

## 22 · RECAP + CLIFFHANGER
▸ And that's it. You now know what's happening under every single tap.
▸ A client and a server. The dining room and the kitchen. Never trust the client. DNS, the Domain Name System, turning names into numbers. HTTP, the HyperText Transfer Protocol, the shared language of request and response. And HTTPS, the sealed envelope.
▸ But notice. All of this took time. The request travelled, the relay raced, the data came back. So how do we measure "fast"? That's latency versus throughput, and that's next time. See you there.

---

**Delivery notes.** Talk, don't read. Pause at each line break. Warm, brisk, a
little playful — you're delighted to show this. Let three beats land: "never trust
the client," "it forgets you completely," and "that is the whole web." Lift the
energy on the welcome (1), the API (8), the relay (13) and the whole journey
(21); slow and settle for the recap (22). Read it aloud — if a line doesn't
sound like talking, rewrite.
