# EP02 — Editing Direction (Captions AI)

> A scene-by-scene editing map for the rendered EP02 video. Use this in
> Captions AI (or any editor) to know where to add captions, B-roll, SFX,
> and intercuts. This is your **first-pass** template — adjust as you
> learn what works for your voice and the channel.

## Inputs

- **Video:** `episodes/ep02/video.mp4` (11:00, 1920×1080, silent)
- **Outro:** `episodes/ep02/outro.mp4` (0:30, splice at end)
- **Voiceover:** record per `episodes/ep02/script.md`, drop on top
- **Subtitles:** import `episodes/ep02/script.srt` as starting point (will need to nudge to your actual voice timing)

## Track layout (recommended)

| Track | Use |
|---|---|
| V1 | The EP02 video (silent base layer) |
| V2 | B-roll inserts (overlay or cut-in) |
| V3 | Reaction / talking-head shots if you ever add them (skip for now) |
| A1 | Your voiceover |
| A2 | SFX (one-shot sounds) |
| A3 | Background music (very low, ~ -22dB) |

## Global settings — set once, applies everywhere

### Captions
- **Style:** Karaoke or Hormozi style — bold word-by-word highlight, brand orange `#FF6B2C` as the highlight color, white base text with black stroke (`2-3px`) for readability over the cream paper background.
- **Font:** Inter Bold or Montserrat Bold (matches our brand sans).
- **Size:** Large (60-70% of safe-zone height for mobile).
- **Position:** Lower-third, slightly above the bottom 15% safe zone for Reels/Shorts crops.
- **Animation:** Pop-in per word, no excessive bounce.

### Music
- **Genre:** Soft cinematic / lo-fi educational. Channels like *Tom Scott*, *Veritasium*, *3Blue1Brown* use sparse minimal-piano + ambient pad. NOT corporate-explainer royalty-free.
- **Suggested search terms for the Captions music library:** "thoughtful", "documentary minimal", "lo-fi piano", "contemplative tech"
- **Volume:** -22 to -26 dB under voice. Should disappear under speech, gently fill the breaths.

### SFX vocabulary (used repeatedly)
- **Reveal-ding:** soft chime / single piano note → for new visual elements appearing
- **Whoosh:** quick swoosh → for scene transitions / wipes
- **Click:** crisp UI click → for satisfying box/element snaps into place
- **Thunk:** muted impact → for "blocked", "wrong", endings of statements
- **Notification:** gentle ping → for phone-screen scenes (UPI, ChatGPT)
- **Pop:** small pop → for bullet points appearing
- **Riser:** building-tension sweep → before big reveals (the 4-nested-boxes moment)

---

## Scene-by-scene direction

### SCENE 1 — Title (0:00 – 0:30)

**On-screen:** "AI vs ML vs DL vs GenAI" headline + tagline "Four words. One picture. Finally clear."

| Element | Direction |
|---|---|
| **Captions** | None needed — your VO is short here, the title IS the visual. If you do caption, keep tiny in upper corner. |
| **B-roll** | NONE. Don't break the title. |
| **SFX** | Single soft **riser** building under the first 5 seconds. Single **reveal-ding** when each of the four words ("AI", "ML", "DL", "GenAI") highlights — 4 dings total, one beat apart. |
| **Music** | Music starts at 0:08 (after "Welcome back to The Tech Intern"), fades up to its quiet baseline by 0:15. |
| **Cut** | No cuts. Hold the title. |

---

### SCENE 2 — The everyday confusion (0:30 – 1:15)

**On-screen:** 4 misquote cards from "LinkedIn".

| Element | Direction |
|---|---|
| **Captions** | Karaoke style. Highlight each of the four buzzwords in **brand orange** whenever you say them: AI, Machine Learning, Deep Learning, Generative AI. |
| **B-roll** | • **0:30–0:35:** quick 3-second clip of someone scrolling LinkedIn on phone (Captions AI has stock — search "linkedin scroll phone"). Overlay on V2, fade in/out. <br>• **0:42–0:47:** When narrator says "founder, usually very confident" — quick stock clip of a confident person on stage (search "tech founder pitch stage"). |
| **SFX** | **Pop** when each of the 4 misquote cards appears (~ 0:35, 0:37, 0:40, 0:42). **Typing sound** during the LinkedIn-scroll B-roll. |
| **Cut** | After each misquote card pops in, hold ~1 second, then cut to the next. No fancy transitions. |

---

### SCENE 3 — Callback to Episode 1 (1:15 – 1:50)

**On-screen:** "Last episode: RULES vs PATTERNS" + small "EP 01" callback strip.

| Element | Direction |
|---|---|
| **Captions** | Standard. Bold "RULES" and "PATTERNS" when said. |
| **B-roll** | • **1:15–1:20:** If you have access to EP01's render, splice a 3-second cut from EP01's scatter-plot scene (around EP01 5:30 mark). It cements the callback visually. <br>• If not, use a small "EP01" badge overlay (Captions AI lets you upload a PNG). |
| **SFX** | **Rewind / time-jump** sound at the moment the EP 01 strip appears (~1:20). Subtle. |
| **Music** | Music drops to silence for ~2 seconds when EP01 callback appears, then returns. Creates "we're remembering something" beat. |

---

### SCENE 4 — The big reveal: 4 nested boxes (1:50 – 2:40)

**This is the first big payoff. Treat it that way.**

| Element | Direction |
|---|---|
| **Captions** | Bold orange highlight on "**4 nested boxes**" and "**like Russian dolls**". |
| **B-roll** | **1:58–2:02:** Russian matryoshka dolls being opened (search "matryoshka doll nesting opening" — many beautiful stock clips). 3 seconds, picture-in-picture in the top-right corner, then fade out. |
| **SFX** | **Riser** building from 1:50, peaks at 1:58 just before "Russian dolls". Then 4 satisfying **click** sounds as each box nests into place (~ 2:00, 2:02, 2:04, 2:06). |
| **Cut** | No cuts inside this scene. The visual IS the cut. Let it land. |
| **Music** | Music swells slightly during the reveal, settles after. |

---

### SCENE 5 — Box 1: AI (2:40 – 3:35)

**On-screen:** AI definition + 3 examples (chess, spam, ChatGPT).

| Element | Direction |
|---|---|
| **Captions** | Standard. Highlight "**smart**" and the three examples. |
| **B-roll** | **3 quick cut-ins** (1-1.5 sec each), perfectly timed to your VO: <br>• **~ 3:00:** Garry Kasparov chess clip (search "kasparov chess deep blue 1997"). <br>• **~ 3:05:** Gmail spam folder screenshot (you can screenshot your own and upload). <br>• **~ 3:10:** ChatGPT logo or interface (search "chatgpt logo dark"). |
| **SFX** | **Pop** when each example bullet appears. |
| **Cut** | After each B-roll cut-in, snap back to the main composition. Keep cuts crisp (< 0.1s transition). |

---

### SCENE 6 — Box 2: ML (3:35 – 4:20)

**On-screen:** ML definition + Swiggy callback.

| Element | Direction |
|---|---|
| **Captions** | Standard. Highlight "**learns from data**". |
| **B-roll** | **~ 3:55–3:58:** Brief Swiggy app screen recording showing the ETA prediction (you can record this on your phone). Or splice the Swiggy scatter-plot scene from EP01 again. |
| **SFX** | **Reveal-ding** when the EP01 callback strip appears (~ 3:55). |

---

### SCENE 7 — UPI fraud (4:20 – 5:15)

**On-screen:** Phone mockup with ₹50,000 BLOCKED at 3 AM.

**This is one of the most cinematic moments. Lean in.**

| Element | Direction |
|---|---|
| **Captions** | Big bold red highlight on "**BLOCKED**" when it appears. Standard for the rest. |
| **B-roll** | • **4:20–4:25:** Quick stock cut of real Indian person using UPI on phone (search "upi payment india smartphone"). 4 seconds, overlay. <br>• **4:40–4:45:** When "Blocked" lands — quick freeze + zoom on the phone mockup (Captions AI has a Ken-Burns zoom effect). Hold for impact. <br>• **5:00–5:05:** When "saves your money every single day" — quick cash-register-closing sound + visual of money safely back in account (or just freeze on the BLOCKED badge). |
| **SFX** | • **Phone notification ding** when UPI screen appears (~4:25). <br>• **Thunk + alarm** sound when "BLOCKED" appears (~4:42). <br>• **Cash register / vault-close** sound at "saves your money" (~5:05). |
| **Cut** | One slow zoom on the phone mockup over the full 55 seconds. Slow Ken Burns. Stops on "BLOCKED". |

---

### SCENE 8 — Box 3: Deep Learning (5:15 – 6:10)

**On-screen:** DL definition + neural network mini-diagram.

| Element | Direction |
|---|---|
| **Captions** | Highlight "**neural network**" and "**brain made out of math**". |
| **B-roll** | **5:25–5:30:** Stock clip of a stylized brain-with-circuitry / neural network animation (search "neural network animation abstract"). 5 seconds, overlay 30% opacity behind the main composition. |
| **SFX** | Subtle **synth / electronic shimmer** sound when the NN diagram reveals (~5:30). Not loud — adds texture. |

---

### SCENE 9 — Why "deep"? (6:10 – 6:40)

**On-screen:** 4 stacked layer rows: 1 → 3 → 100 → 1000+

**Short, punchy scene. Treat it like a comedic beat.**

| Element | Direction |
|---|---|
| **Captions** | Big bold orange "**DEEP**" highlight when the word is said. |
| **B-roll** | Optional: **6:25:** Quick visual of physical paper stacks growing (search "paper stack tower"). Or skip — the on-screen visual is already explanatory. |
| **SFX** | **Click / stack sound** as each layer-row appears (4 stacks, 4 clicks: ~6:15, 6:19, 6:23, 6:27). Building anticipation. |

---

### SCENE 10 — Phone camera (6:40 – 7:30)

**On-screen:** Phone in portrait mode with face detected.

| Element | Direction |
|---|---|
| **Captions** | Standard. Highlight "**face**" and "**neural network**". |
| **B-roll** | • **6:42–6:46:** Real footage of someone using their phone camera in portrait mode (search "phone portrait mode photo face"). <br>• **7:10–7:15:** Karnataka farmer scanning a crop leaf with a phone (search "indian farmer phone agriculture app"). 4 seconds, overlay. <br>• **7:18–7:22:** Quick X-ray / medical imaging visual (search "x-ray scan medical ai"). |
| **SFX** | **Camera shutter** when the phone appears (~6:42). **Autofocus beep** when the FACE box appears in the viewfinder mockup. |

---

### SCENE 11 — Box 4: Generative AI (7:30 – 8:25)

**On-screen:** GenAI definition + 5 type chips (Text / Images / Code / Music / Video).

| Element | Direction |
|---|---|
| **Captions** | Highlight "**creates**" in italic orange. Standard for the rest. |
| **B-roll** | Each type chip can have a 1-second B-roll showing what it generates: <br>• **Text:** quick ChatGPT typing animation <br>• **Images:** quick Midjourney generation reveal <br>• **Code:** Cursor / VS Code AI suggestion popping up <br>• **Music:** Suno waveform <br>• **Video:** Sora-style clip <br>Quick cuts, 1 second each, in rhythm with the chips appearing on screen (~ 7:50–7:58). |
| **SFX** | Each chip gets a different small sound: text=typewriter ding, image=camera shutter, code=keyboard click, music=note, video=film clack. Builds variety. |

---

### SCENE 12 — ChatGPT example (8:25 – 9:15)

**On-screen:** Phone chat: "Write an email to my landlord" → AI generates email.

| Element | Direction |
|---|---|
| **Captions** | Highlight "**five seconds ago**" big and orange. Standard for the rest. |
| **B-roll** | • **8:25–8:30:** Real screen recording of typing into ChatGPT (you can record your own — type a similar prompt and let it generate). <br>• **8:50–8:55:** When narrator says "Bollywood movie poster of a tiger in a Mumbai monsoon" — show an actual generated image of exactly that. Use Midjourney/DALL-E to generate one, save the PNG, splice it in. Will WOW viewers. |
| **SFX** | **Typing sound** continuously during the ChatGPT generation (~8:25–8:40, low volume). **Magical reveal sound** when the Bollywood tiger image appears (~8:52). |

---

### SCENE 13 — The full picture (9:15 – 10:00)

**On-screen:** All 4 nested boxes synthesis with one Indian example in each layer.

**This is THE shareable screenshot moment. Don't pollute it.**

| Element | Direction |
|---|---|
| **Captions** | Minimal. Maybe just highlight "**four boxes, one picture**" at the start, then go silent for the rest of the synthesis. Let viewers READ the diagram. |
| **B-roll** | **NONE.** Don't break the synthesis visual. |
| **SFX** | **Big reveal sting** when the full nested-boxes diagram completes (~9:25). Something cinematic. Then SILENCE for 5-10 seconds, just your voice, music dropped low. Let the picture do the work. |
| **Music** | Drop music to near-silent at 9:20. Resume gently at 9:50. The silence makes the synthesis feel important. |

---

### SCENE 14 — Your new habit (10:00 – 10:30)

**On-screen:** "Someone says AI did X?" → "Ask: WHICH BOX?"

| Element | Direction |
|---|---|
| **Captions** | **HUGE bold orange "WHICH BOX?"** Karaoke-style explosion. This is your meme moment. |
| **B-roll** | • **10:00–10:05:** Quick stock cut of a confused-but-confident manager talking (search "businessman talking confident"). <br>• **10:15:** Cut to a thoughtful person nodding (search "person realization nodding"). Optional. |
| **SFX** | **Question-mark sound** (riser + ding) when "WHICH BOX?" appears. **Subtle "ah-ha"** chime when narrator says "Nine times out of ten — the person who said AI won't actually know." |

---

### SCENE 15 — Recap (10:30 – 11:00)

**On-screen:** Recap of 4 definitions.

| Element | Direction |
|---|---|
| **Captions** | Follow each definition as it appears on screen. Standard. |
| **B-roll** | **NONE.** Keep the recap clean. |
| **SFX** | **Sequential ding** as each of the 4 lines appears (4 dings, evenly spaced). Build subtle anticipation. |
| **Music** | Music builds slightly through the recap, swells at the last line ("…that creates new things."), then transitions smoothly into the outro. |

---

### OUTRO (11:00 – 11:30) — `outro.mp4`

| Element | Direction |
|---|---|
| **Captions** | Standard. Maybe highlight "**EP 03**" and "**Subscribe**" in orange. |
| **B-roll** | **NONE.** Keep CTA clean. |
| **SFX** | • **Soft chime** when "EP 03 · Data → Model → Prediction" appears. <br>• **Subscribe-button click sound** when Subscribe CTA appears (~11:12). <br>• **Final brand sting** at the very end (11:28). |
| **Music** | Music swells out, then fades to silence by 11:30. |

---

## Critical "don'ts" for the first edit

1. **Don't overdo B-roll.** Maximum 3-4 seconds per insert. Cut back to the main composition fast. The motion graphics ARE the visual; B-roll is seasoning, not the meal.
2. **Don't add captions to the entire video.** Yes, all of it should have captions for accessibility, BUT — don't add a giant caption over the on-screen text. The composition already has on-screen text. The captions exist for moments when your VO says something the visual doesn't show.
3. **Don't drown the voice in music.** -22 dB minimum. Test on phone speakers and AirPods both.
4. **Don't over-SFX.** One sound per beat. If two sounds collide, pick the more important one.
5. **Don't transition with fancy effects.** Hard cuts only. Whoosh transitions = amateur energy.

## After the first edit, do this

1. Watch the whole video at **1.0x speed**, headphones on, like a viewer would.
2. Note every place you feel **bored** or **lost**.
3. Bored → add a small B-roll or punchier SFX there.
4. Lost → add a bigger caption emphasis or hold the visual longer.
5. Re-export. Watch again on **mobile**.
6. Ship.

## Captions AI specific tips

- Use their **Magic B-Roll** feature for the auto-suggestions — but review every suggestion before accepting. AI tends to over-insert.
- Their **SFX library** is huge — search by emotion, not just sound name ("satisfying" surfaces lots of dings).
- **Don't enable eye-contact correction** — there's no face here.
- Export at **1080p, H.264** for YouTube. For Shorts, do a vertical reframe pass after.

---

## Reusable template

Once you've done EP02 and learned what works, formalize this into a
generic editing template under `docs/EDITING.md`. Future episodes will
just need scene-specific notes instead of starting from scratch.
