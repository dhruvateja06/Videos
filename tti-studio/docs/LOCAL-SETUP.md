# Local Claude Code Setup (Mac/Linux/Windows)

> For when you need to do things the cloud sandbox can't do — voice
> generation (ElevenLabs), or any external API the sandbox firewall
> doesn't allow.
>
> The cloud sandbox stays useful for the heavy stuff (compositions,
> rendering, docs). Local Claude Code is for the network-dependent steps.

## One-time setup (only do this once per machine)

### 1. Install Claude Code locally

**macOS / Linux:**
```bash
curl -fsSL https://claude.com/install.sh | sh
```

**Windows:** use the installer at https://docs.claude.com/en/docs/claude-code/quickstart

Sign in with your Anthropic account when prompted.

### 2. Install `uv` (the Python runner the ElevenLabs MCP needs)

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Reload your shell, then verify:
```bash
which uvx       # should print a path
```

### 3. Clone the repo

```bash
cd ~/code              # or wherever you keep projects
git clone https://github.com/dhruvateja06/videos.git
cd videos
git checkout claude/gifted-brown-7e7t72   # or whichever branch you're working on
```

### 4. Set the ElevenLabs API key as an environment variable

**First — rotate any key that's been exposed before** (elevenlabs.io →
Settings → API Keys → revoke old, create new). Never type the key into
chat.

**macOS / Linux** — add to `~/.zshrc` (or `~/.bashrc`):
```bash
export ELEVENLABS_API_KEY="sk_NEW_KEY_HERE"
```

Then reload:
```bash
source ~/.zshrc
```

**Windows (PowerShell)** — add to your PowerShell profile:
```powershell
[System.Environment]::SetEnvironmentVariable('ELEVENLABS_API_KEY', 'sk_NEW_KEY_HERE', 'User')
```

Verify the env var is set:
```bash
echo $ELEVENLABS_API_KEY    # macOS/Linux
echo $env:ELEVENLABS_API_KEY # Windows PowerShell
```

### 5. Install HyperFrames + render toolchain (only if you'll render locally)

If you only want to do voice work locally (and render in the cloud
sandbox), skip this step.

```bash
cd /path/to/videos/tech-intern-videos
npm install hyperframes @ffmpeg-installer/ffmpeg @ffprobe-installer/ffprobe
node -e "require('fs').symlinkSync(require('@ffmpeg-installer/ffmpeg').path,'/usr/local/bin/ffmpeg')"
node -e "require('fs').symlinkSync(require('@ffprobe-installer/ffprobe').path,'/usr/local/bin/ffprobe')"
node_modules/.bin/hyperframes browser ensure
```

## Per-session (every time you open a local Claude Code session)

### Start the session

```bash
cd ~/code/videos      # or wherever you cloned it
claude
```

The session will boot and automatically:
- Read `CLAUDE.md` → load the channel brain instructions
- Read `.mcp.json` → start `uvx elevenlabs-mcp` as a subprocess
- Read `.claude/settings.json` → trust the MCP server (no prompt)
- Inherit your `ELEVENLABS_API_KEY` env var → MCP can authenticate
- Load all 5 project-scope skills from `tti-studio/.claude/skills/`

### Verify ElevenLabs is connected

In the session, just type:

> *What ElevenLabs tools do you have? Also list my voices on the
> account.*

If it works, you'll see tool names like `elevenlabs__text_to_speech`,
`elevenlabs__voice_clone`, etc., plus a list of voices.

If it doesn't work:
- `ELEVENLABS_API_KEY not set` → step 4 didn't take, re-export and
  restart the session
- `command not found: uvx` → step 2 didn't install in this shell, run
  the install again and re-open the terminal
- 401 from ElevenLabs → wrong key or revoked, generate a new one

## The hybrid workflow (cloud + local)

Most efficient division of labor:

| Phase | Where to do it | Why |
|---|---|---|
| Topic / Outline / Script | Either (chat works in both) | Pure thinking — no network constraints |
| Build composition + deck | **Cloud sandbox** | Heavy file editing, no external network needed |
| Voice generation (ElevenLabs) | **Local** | Cloud sandbox firewall blocks elevenlabs.io |
| Composition retime to match VO | Either (just file edits) | Reading the VO MP3 and adjusting numbers |
| Render video | **Cloud sandbox** (faster + bigger CPU) | Render is CPU-heavy; no network needed |
| Compress + push deliverable | Either | Trivial |
| Editing in Captions AI | Browser, not Claude Code | External tool |

Files travel between cloud and local sessions via git push / pull — both
see the same repo state after a sync.

## The first thing to do in your new local session

Once `claude` is running and you've verified ElevenLabs is connected, paste this:

```text
Read docs/WORKFLOW.md and docs/PIPELINE.md. We're in the local session
to do the voice work for EP02.

Steps for this session:
1. Use elevenlabs__get_voices to confirm the API works
2. I'll record and provide a 1-3 minute voice reference sample saved
   at episodes/ep02/voice-reference.mp3
3. Use elevenlabs__voice_clone (instant clone) to create a voice named
   "tech-intern-host"
4. Generate VO for slides 1-2 of episodes/ep02/script.md using that
   voice. Settings: stability 0.4, similarity 0.75, style 0.3.
5. Save output to episodes/ep02/vo-test-slides-1-2.mp3
6. Report the duration; I'll listen and decide if quality is good
   enough to proceed with full episode VO.
7. Commit + push the test MP3 so I can also QA from the cloud session.
```

That's the prompt. The local session will do the work, push the MP3,
and I can pick up from there in the cloud sandbox if needed.

## Security checklist

- [ ] Rotated any API key that's been pasted in chat
- [ ] New key only in env vars, never in committed files or chat
- [ ] `.env` files (if you create any) are in `.gitignore`
- [ ] `git status` shows no `.env` or other secret-bearing files
  before any commit
