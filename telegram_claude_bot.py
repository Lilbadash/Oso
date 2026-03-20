#!/usr/bin/env python3
"""
Telegram → Claude Code bridge.

Setup:
1. Get a bot token from @BotFather on Telegram
2. Set your token in the BOT_TOKEN variable below (or export TELEGRAM_BOT_TOKEN=...)
3. Run: python3 telegram_claude_bot.py
4. Message your bot on Telegram — Claude will respond!
"""

import os
import subprocess
import time
import requests

# ─── CONFIG ──────────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CLAUDE_CMD = "/opt/node22/bin/claude"
ALLOWED_USER_IDS = []  # Fill with your Telegram user ID to restrict access, or leave empty to allow anyone
# ─────────────────────────────────────────────────────────────────────────────

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text):
    """Send a message back to Telegram."""
    # Telegram has a 4096 char limit per message
    for chunk in [text[i:i+4096] for i in range(0, len(text), 4096)]:
        requests.post(f"{BASE_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown"
        })


def ask_claude(prompt):
    """Pass a prompt to Claude Code CLI and return the response."""
    try:
        result = subprocess.run(
            [CLAUDE_CMD, "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout.strip()
        if result.returncode != 0 and result.stderr:
            output += f"\n\n[stderr]: {result.stderr.strip()}"
        return output or "_(no response)_"
    except subprocess.TimeoutExpired:
        return "Request timed out (>120s)."
    except Exception as e:
        return f"Error running Claude: {e}"


def get_updates(offset=None):
    """Long-poll Telegram for new messages."""
    params = {"timeout": 30, "offset": offset}
    try:
        resp = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=35)
        return resp.json().get("result", [])
    except Exception:
        return []


def is_allowed(user_id):
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS


def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("ERROR: Set your bot token first.")
        print("  Either edit BOT_TOKEN in this file, or:")
        print("  export TELEGRAM_BOT_TOKEN=your_token_here")
        return

    print("Bot is running. Send a message to your Telegram bot!")
    offset = None

    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            user_id = message["from"]["id"]
            text = message.get("text", "").strip()

            if not text:
                continue

            if not is_allowed(user_id):
                send_message(chat_id, "Access denied.")
                continue

            print(f"[{user_id}] {text}")
            send_message(chat_id, "Thinking...")

            response = ask_claude(text)
            send_message(chat_id, response)

        time.sleep(1)


if __name__ == "__main__":
    main()
