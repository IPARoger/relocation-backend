# Relay Automation — Setup (non-developer guide)

This makes the two AI agents talk to each other through GitHub so you are no
longer the copy/paste courier. You stay in control of one thing only: clicking
"merge" on the changes you approve. Telegram pings you when that moment arrives.

Nothing here runs or costs money until you deliberately turn it on. By default
the workflow is **manual** and in **dry-run** (a free, no-op rehearsal).

---

## What it costs

- **OpenAI (the "GPT brain")**: pay-per-use. For this low-volume relay it is
  typically a few cents per run, on the order of **$1–2/month**. Each run sends
  only a couple pages of text, which is why it stays cheap.
- **Cursor (the execution)**: runs on your existing Cursor subscription. Cloud
  agent runs may add some usage there. Check your Cursor plan's cloud-agent
  limits.
- **GitHub Actions + Telegram**: free for this usage.

---

## One-time setup (about 10 minutes)

### Step 1 — Get two keys

1. **OpenAI API key**: https://platform.openai.com → API keys → "Create new
   secret key". (This is separate from ChatGPT Plus. You add a little credit;
   set a low monthly usage cap so it can never surprise you.)
2. **Cursor API key**: Cursor Dashboard → Integrations → create a key.

### Step 2 — Put the keys into GitHub (as "secrets", never in code)

In your GitHub repo: **Settings → Secrets and variables → Actions → New
repository secret**. Add these:

| Secret name | Value |
|---|---|
| `OPENAI_API_KEY` | your OpenAI key |
| `CURSOR_API_KEY` | your Cursor key |
| `TELEGRAM_BOT_TOKEN` | (already used by your Telegram pings) |
| `TELEGRAM_CHAT_ID` | (already used by your Telegram pings) |
| `OPENAI_MODEL` *(optional)* | a cheap model name, e.g. a "mini" model |

### Step 3 — Rehearse for free (dry run)

In GitHub: **Actions → two-agent-relay → Run workflow**, leave **Dry run =
true**, click the green button. It will show what it *would* do without calling
any paid API or changing anything. Confirm it runs green.

---

## Going live

When you are ready, run the workflow again with **Dry run = false**. Then:

1. The OpenAI brain writes the next task into `tasks/`.
2. A Cursor cloud agent executes it, writes the `results/` closeout, and **opens
   a Pull Request**.
3. You get a Telegram **"Human approval required"** ping.
4. You review the Pull Request in GitHub and click **Merge** if you approve.
5. Next run, the brain reads your merged result and proposes the next step.

You are only ever needed at step 4.

---

## Full auto (optional, later)

To let it run itself on a timer, uncomment the `schedule` block at the bottom of
`.github/workflows/relay.yml`. Leave it off until you trust the loop.

---

## Low-balance protection (so you are never charged twice)

Before each live run, a cheap check (a fraction of a cent) confirms your OpenAI
balance can cover the work. If it cannot:

- you get a Telegram **"Low balance — top up before this task runs"** ping,
- the run **stops before** the expensive Cursor execution, and
- nothing partial happens, so after you top up and re-run, you do **not** pay
  twice for the same task.

The same warning fires if the Cursor side is out of funds at launch. To top up:
OpenAI → platform billing; Cursor → your Cursor plan/billing. Then just
re-run the workflow.

---

## Stop everything (kill switch)

- GitHub → **Actions → two-agent-relay → "..." → Disable workflow**, or
- delete the `OPENAI_API_KEY` / `CURSOR_API_KEY` secrets.

Either one halts all automation immediately. Your human merge gate means nothing
reaches the main code without you clicking merge, regardless.
