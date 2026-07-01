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
git checkout claude/eager-shannon-i79f3n   # system design branch
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
cd /path/to/videos/tti-studio
npm install
npx hyperframes@0.7.5 browser ensure
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
- Load all project-scope skills from `tti-studio/.claude/skills/`

### Verify ElevenLabs is connected

In the session, just type:

> *What ElevenLabs tools do you have? Also list my voices on the account.*

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

Files travel between cloud and local sessions via git push / pull — both
see the same repo state after a sync.

## Voice settings for this vertical

Locked voice: `7hshzsnMFQgQHNhu6yYM` (Dhruva), model: `eleven_multilingual_v2`

```python
VOICE_SETTINGS = {
    "stability": 0.30,
    "similarity_boost": 0.75,
    "style": 0.65,
    "use_speaker_boost": True,
    "speed": 1.02,
}
```

See `docs/VOICEOVER.md` for the full word-sync pipeline.

## Security checklist

- [ ] Rotated any API key that's been pasted in chat
- [ ] New key only in env vars, never in committed files or chat
- [ ] `.env` files (if you create any) are in `.gitignore`
- [ ] `git status` shows no `.env` or other secret-bearing files before any commit
