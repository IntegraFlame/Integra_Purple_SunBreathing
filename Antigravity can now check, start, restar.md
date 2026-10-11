Antigravity can now check, start, restart and stop the Genesis Kernel, read its logs, and open its dashboard. Everything runs through one new script, [kernel_ctl.ps1](integra-homebase/scripts/kernel_ctl.ps1), and a new Antigravity skill tells its agent how to use it. I haven't seen the skill appear inside Antigravity, and I didn't run `stop` or `restart`, because that would take your live kernel down.

**What I added**
- **The script:** it has five actions: `status`, `logs`, `start`, `stop`, `restart`.
  - `start` goes through your existing "Integra Genesis Kernel" scheduled task. That's the same launcher used at logon, so the kernel stays on 127.0.0.1 only and logs to the Hoard. If a kernel is already running, `start` does nothing.
  - `stop` and `restart` refuse unless the kernel reports SWDS as awake, because Heimdall owns the SWDS cycle. Adding `-Force` overrides that, and should be used only when you approve it.
- **The skill:** `~/.gemini/config/skills/genesis-kernel/SKILL.md`, next to your `integra-protocol` skill. It gives Antigravity's agent the exact commands and these rules:
  - Never start the kernel with `python main.py` (it binds `0.0.0.0` and exposes the API to your network).
  - Ask you before stop, restart or any POST. POSTs can change SWDS state or make paid model calls.
  - Never read `.env` files for the admin token.
  - Never touch the trading routes.
  - Never run tests against the live repo.
  - It also lists the read-only routes, which the agent can query freely without blocking SWDS.
- **IDE task:** the old "integra: start-genesis-kernel" task ran `main.py` directly, which binds `0.0.0.0`. It now calls the script, and I added an "integra: kernel-status" task.

**Testing**
- The script parses cleanly under Windows PowerShell 5.1 and PowerShell 7.
- `status`, `logs`, `start` and the IDE task all work. `start` correctly did nothing because the kernel was already up.
- `stop`, `restart` and their SWDS guard are untested.

**Something I found along the way:** the dashboard I left open in the preview pane was a big part of the slowdown. It polls 7 endpoints every second, and requests were taking 3–14 seconds, sometimes refused. After I moved the tab off the dashboard, responses dropped to 259–434 ms. The skill tells agents to close the dashboard when they're done.

**Two things for you to do**
1. **Allow the commands in Antigravity.** Your Antigravity project has auto-run turned off, so it will ask before the first run of each command; choose "always allow" for `status`, `logs` and `start`. I'd keep asking for `stop`, `restart` and `-Force`. I didn't edit Antigravity's permission settings myself.
2. **Confirm the skill shows up** in Antigravity's skill list. If it doesn't, I can move it into the repo's `.agents/skills/` folder instead.