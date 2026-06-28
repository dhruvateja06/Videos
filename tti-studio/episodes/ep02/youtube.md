# Ep02 — YouTube metadata

## Title (pick one)
1. How Your Phone Finds the Server — DNS & HTTP Explained (System Design #2)
2. Client vs Server, DNS & HTTP — System Design from Day One (Ep 2)
3. What Happens When You Tap "Swiggy"? — System Design #2

**Primary recommendation:** #1 — keyword "DNS & HTTP" + a clear curiosity hook.

## Short description (first 2 lines — above the fold)
You tap Swiggy. In a fraction of a second, your phone finds the right server out of billions and starts a conversation with it.
This is how — DNS and HTTP, by way of a restaurant.

## Full description
Open Swiggy. Tap a restaurant. In half a second, your phone has found Swiggy's server out of billions on the internet and asked it for the menu. How does that even work?

In Episode 2 of The Tech Intern — System Design, we crack open the "client" and "server" boxes from Ep01 and watch them actually talk. The whole episode runs on one analogy: a restaurant. The dining room is the client. The kitchen is the server. The waiter is the API. And every tap you make plays out across that picture.

You'll walk away understanding (every acronym spelled out, no jargon left dangling):
- What the client (frontend) and server (backend) really do — and why your data lives only on the server
- The golden rule of system design: never trust the client (and why hacked "pay Rs 1" attacks fail)
- API (Application Programming Interface) as the waiter — one backend serving many apps (iOS, Android, web)
- CSR vs SSR (Client-Side / Server-Side Rendering) — who actually draws the page, and the trade-off
- IP (Internet Protocol) addresses as a server's "phone number" (IPv4 vs IPv6)
- DNS (Domain Name System) as the internet's phonebook — name → number
- The DNS relay: device → resolver → root → TLD → authoritative
- DNS caching and TTL (Time To Live) — the speed-vs-freshness trade-off
- HTTP (HyperText Transfer Protocol) as the shared language — request and response
- Anatomy of a request: method, path, headers, body — and a URL (Uniform Resource Locator) broken down
- GET vs POST — reads vs writes, and why double-tapping POST can place two orders
- Cookies as your ID badge — how HTTP "forgets" but the app remembers you
- Status codes: 200, 301, 404, 500 (and the "4xx = your fault, 5xx = server's fault" rule)
- HTTPS (HTTP Secure) as a sealed envelope — what the padlock actually means (and what it doesn't)

Indian, everyday examples first. Every term explained on first use.

▶ Next episode: All this travelling takes *time*. So how do we measure "fast"? Latency vs throughput.

🔔 Subscribe — we're building this whole thing, one box at a time.

## Chapters (paste into description)
0:00 Welcome back · the missing piece from Ep 01
0:43 Tonight's two questions
1:02 The restaurant (the spine analogy)
1:33 The client — your phone, the dining room
2:02 The server — the kitchen
2:29 Where your data actually lives
2:56 The golden rule: never trust the client
3:25 The API (Application Programming Interface)
4:08 CSR vs SSR — who draws the page?
4:49 Billions of computers, one name
5:10 IP address (Internet Protocol)
5:43 DNS — the Domain Name System
6:14 The DNS relay (resolver → root → TLD → authoritative)
6:56 DNS cache + TTL (Time To Live)
7:42 HTTP (HyperText Transfer Protocol)
8:25 Anatomy of a request + URL
9:00 GET vs POST — read vs write
9:35 Cookies — your ID badge
10:09 Status codes — 200, 301, 404, 500
10:42 The S in HTTPS — sealed envelope
11:18 The whole journey, end to end
11:46 Recap + what's next

## Tags
DNS explained, HTTP explained, client server architecture, what is DNS, what is HTTP, HTTPS explained, GET vs POST, status codes, system design for beginners, how the internet works, IP address, DNS lookup, REST API basics, cookies and sessions, CSR vs SSR, the tech intern, system design from day one

## Pinned comment
Quick check — what's the difference between a 404 and a 500? (And next ep: why "fast" is two different numbers — latency vs throughput.)

## Sources for the on-screen facts
- DNS resolution chain (browser cache → recursive resolver → root → TLD → authoritative): MDN, Cloudflare Learning, AWS Route 53 docs
- HTTP methods, idempotency/safety, URL anatomy, headers/cookies, status codes: MDN Web Docs
- TLS handshake / HTTPS encryption (high level): Cloudflare Learning, MDN
- Client/server split, "never trust the client": MDN, OWASP Input Validation Cheat Sheet
- CSR vs SSR trade-offs (first paint, SEO, server load): web.dev / MDN-aligned guidance
