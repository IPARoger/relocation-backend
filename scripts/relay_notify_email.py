#!/usr/bin/env python3
"""relay_notify_email.py — relay pings via Gmail SMTP (stdlib only)."""

import argparse
import json
import os
import smtplib
import sys
import urllib.error
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
TIMEOUT = 30

EVENT_SUBJECT = {
    "started": "Task started — Cursor agent launching",
    "approval": "ACTION REQUIRED — review and merge Pull Request",
    "complete": "Task complete",
    "verified": "VERIFIED",
    "not-verified": "NOT VERIFIED",
    "low-balance": "Low balance — top up API credits before next run",
    "test": "Relay email test — notifications are working",
}


def repo_urls():
    repo = os.environ.get("GITHUB_REPOSITORY", "IPARoger/relocation-backend").strip()
    base = "https://github.com/" + repo
    return {
        "repo": base,
        "actions": base + "/actions",
        "pulls": base + "/pulls",
        "tasks": base + "/tree/main/tasks",
        "results": base + "/tree/main/results",
    }


def latest_open_pr():
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not repo or not token:
        return None
    url = f"https://api.github.com/repos/{repo}/pulls?state=open&per_page=1&sort=created&direction=desc"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            pulls = json.loads(resp.read().decode())
        if pulls:
            p = pulls[0]
            return {"number": p.get("number"), "title": p.get("title", ""), "url": p.get("html_url", "")}
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError):
        return None
    return None


def build_body(event, task=None, extra=None):
    links = repo_urls()
    lines = ["Relocation relay notification", "", f"Event: {event}"]
    if task:
        lines.append(f"Task: {task}")
    if extra:
        lines.append(extra)
    lines.extend(["", "Where to go:", ""])

    if event == "started":
        lines.extend([
            f"  • Task file: {links['tasks']}",
            f"  • Workflow runs: {links['actions']}",
            "",
            "A Cursor cloud agent is executing this task.",
            "You will get another email with the Pull Request link when it finishes.",
        ])
    elif event == "approval":
        pr = latest_open_pr()
        lines.extend([">>> MERGE THIS PULL REQUEST <<<", ""])
        if pr:
            lines.extend([f"  PR #{pr['number']}: {pr['title']}", f"  {pr['url']}", ""])
        else:
            lines.extend([f"  Open PRs: {links['pulls']}", ""])
        lines.extend([
            "Steps:",
            "  1. Open the PR link above",
            "  2. Review the changes",
            "  3. Click Merge",
            "",
            f"Results (after merge): {links['results']}",
        ])
    elif event == "low-balance":
        lines.extend([
            "Top up OpenAI and/or Cursor billing, then re-run the workflow.",
            f"  • Actions: {links['actions']}",
        ])
    elif event == "test":
        lines.append("Gmail relay notifications are configured correctly.")
    else:
        lines.append(f"  • Repository: {links['repo']}")

    lines.extend(["", "— automated relay (relocation-backend)"])
    return "\n".join(lines)


def send_email(subject, body, to_addr, from_addr, app_password):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.attach(MIMEText(body, "plain", "utf-8"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=TIMEOUT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(from_addr, app_password)
        smtp.sendmail(from_addr, [to_addr], msg.as_string())


def credentials():
    user = os.environ.get("GMAIL_USER", "").strip().strip('"').strip("'")
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip().strip('"').strip("'")
    to_addr = os.environ.get("RELAY_NOTIFY_EMAIL", "").strip() or user
    if not user or not password:
        return None
    return user, password, to_addr


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="relay_notify_email.py")
    parser.add_argument("event", nargs="?", choices=list(EVENT_SUBJECT.keys()))
    parser.add_argument("--task", default=None)
    parser.add_argument("--message", default=None)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv[1:])


def main(argv):
    args = parse_args(argv)
    creds = credentials()
    if not creds:
        sys.stderr.write("Missing GMAIL_USER and/or GMAIL_APP_PASSWORD.\n")
        return 3
    from_addr, app_password, to_addr = creds
    event = "test" if args.verify else args.event
    if not event:
        sys.stderr.write("Usage: relay_notify_email.py <event> | --verify\n")
        return 2
    task = args.task
    prefix = f"[Relay task {task}] " if task else "[Relay] "
    subject = prefix + EVENT_SUBJECT.get(event, event)
    body = build_body(event, task=task, extra=args.message)
    if args.dry_run:
        sys.stdout.write(subject + "\n\n" + body + "\n")
        return 0
    try:
        send_email(subject, body, to_addr, from_addr, app_password)
    except (smtplib.SMTPException, OSError, TimeoutError) as exc:
        sys.stderr.write("Email delivery failed: " + str(exc) + "\n")
        return 4
    sys.stdout.write("sent: " + event + " -> " + to_addr + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
