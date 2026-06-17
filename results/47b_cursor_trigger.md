# Task 47b — Cursor Trigger Workflow

## 1. cursor_trigger.yml full contents

```yaml
name: cursor-task-trigger

on:
  push:
    branches: [main]
    paths: ['tasks/**.md']

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install requests
        run: pip install requests

      - name: Extract task info
        id: task
        run: |
          TASK_FILE=$(git diff --name-only HEAD~1 HEAD \
            | grep "^tasks/" | head -1)
          TASK_NUM=$(basename "$TASK_FILE" \
            | grep -oE '^[0-9]+')
          echo "file=$TASK_FILE" >> $GITHUB_OUTPUT
          echo "number=$TASK_NUM" >> $GITHUB_OUTPUT

      - name: Notify Telegram — new task ready
        run: |
          python scripts/relay_notify.py started \
            --task "${{ steps.task.outputs.number }}" \
            --message "New task ready: \
              ${{ steps.task.outputs.file }}"
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```

## 2. YAML validation output

```
valid
```

## 3. git diff --stat output (staged)

```
 .github/workflows/cursor_trigger.yml | 43 ++++++++++++++++++++++++++++++++++++
 1 file changed, 43 insertions(+)
```

## 4. Status

**VERIFIED**
