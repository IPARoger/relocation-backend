# Task 47a — Expand relay_notifier

## 1) Lines changed (before/after)

- Added argparse parsing with optional flags:
  - `--task` (string, default `None`)
  - `--message` (string, default `None`)
- `build_message()` now accepts optional task/message context:
  - appends `Task: {task}` when `--task` provided
  - appends `{message}` when `--message` provided
  - unchanged output when neither flag is provided
- Existing event labels unchanged.
- Telegram API call structure unchanged (`send(token, chat_id, text)` payload unchanged).

## 2) Both dry-run outputs

Command:
`./venv/bin/python scripts/relay_notify.py started --dry-run`

Output:
```text
▶️ Task started
exit1:0
```

Command:
`./venv/bin/python scripts/relay_notify.py started --task 47 --message "test" --dry-run`

Output:
```text
▶️ Task started
Task: 47
test
exit2:0
```

## 3) Status

**VERIFIED**

- Both dry-run checks exited 0.
- Only `scripts/relay_notify.py` modified.
