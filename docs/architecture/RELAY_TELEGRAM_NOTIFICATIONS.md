# Relay Telegram Notifications

Minimal, notification-only bridge for the two-agent relay. It sends short status
pings to Telegram so the human operator knows when to look at the repo. It does
**not** transmit task content.

## Design guarantees

- **Notifications only.** The script can send exactly five fixed labels and
  nothing else. There is no argument or code path that accepts free-form text.
- **No task content / code / repository data.** The only transmittable strings
  are the five labels below. File paths, diffs, task names, IDs, and results are
  never sent.
- **No secrets in the repo.** The bot token and chat id are read from the
  environment at runtime and are never logged or printed.
- **No production code changes.** This is standalone notification infrastructure.

## Allowed events

| Event key | Message sent |
|---|---|
| `started` | Task started |
| `complete` | Task complete |
| `approval` | Human approval required |
| `verified` | VERIFIED |
| `not-verified` | NOT VERIFIED |

Decorative emoji prefixes are added for readability; they carry no task data.

## Files

- `scripts/relay_notify.py` — the notification script (standard library only;
  no extra dependencies).

## Configuration

Set two environment variables (do not commit real values):

```
TELEGRAM_BOT_TOKEN=<token from BotFather>
TELEGRAM_CHAT_ID=<destination chat id>
```

Recommended: keep these in `.env.local` (already git-ignored) alongside other
local secrets. They are intentionally **not** added to `.env.example` defaults,
but the variable names are documented here.

### Getting the values

1. In Telegram, message `@BotFather`, run `/newbot` (or reuse the existing relay
   bot), and copy the bot token.
2. Start a chat with the bot (or add it to the target group) and send any
   message.
3. Get the chat id: open
   `https://api.telegram.org/bot<TOKEN>/getUpdates` in a browser and read
   `result[].message.chat.id`. For groups the id is negative.

## Usage

Dry run (prints the fixed label, sends nothing, needs no token):

```
python scripts/relay_notify.py started --dry-run
```

Real send (requires the two environment variables):

```
set -a && source .env.local && set +a
python scripts/relay_notify.py started
python scripts/relay_notify.py approval
python scripts/relay_notify.py verified
python scripts/relay_notify.py complete
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Notification sent (or printed in `--dry-run`) |
| 2 | Invalid usage / unknown event |
| 3 | Missing `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` |
| 4 | Delivery failure (network / API) |

The script fails safe: if configuration is missing it exits non-zero without
sending and without printing the token.

## Suggested relay integration

Call the script at the relay lifecycle points. Keep it advisory — never block
work on notification delivery. Examples:

- When picking up a task: `python scripts/relay_notify.py started`
- When a task needs a human gate (DB write, schema, backend, credentials):
  `python scripts/relay_notify.py approval`
- On closeout: `python scripts/relay_notify.py verified` **or**
  `python scripts/relay_notify.py not-verified`
- After the human merges/acks: `python scripts/relay_notify.py complete`

Because only labels are sent, the operator still opens the repo (`tasks/`,
`results/`, `audits/`) to read the actual content. This preserves the human
approval gate described in `TWO_AGENT_RELAY_GOVERNANCE.md`.

### Phase 2 question labels (group convention)

The Telegram **group chat** may use human-readable prefixes when a ping needs
context before opening the repo. These are conventions for the operator, not
new `relay_notify.py` events:

| Label | Emoji | Open on laptop |
|-------|-------|----------------|
| Check Cursor | 🔵 | `tasks/` / `results/` — implementation or scope question |
| Check App | 🟠 | Product / UX decision |
| Check Risk | 🔴 | Schema, prod, credentials, irreversible action |

Agents still send only fixed `relay_notify.py` events; the full question lives
in `results/`. See `RELAY_OPERATING_GUIDE.md`.

## Rollback

```
rm scripts/relay_notify.py
rm docs/architecture/RELAY_TELEGRAM_NOTIFICATIONS.md
```

(No other files are created or modified by this feature.)
