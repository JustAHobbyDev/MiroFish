#!/usr/bin/env python3
"""
Minimal one-off Telegram alert CLI.

Credentials are read from env by default:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

Examples:
  telegram-alert "Build finished"
  echo "Long message" | telegram-alert
  telegram-alert --parse-mode Markdown -m "*Done*"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_TOKEN_ENV = "TELEGRAM_BOT_TOKEN"
DEFAULT_CHAT_ENV = "TELEGRAM_CHAT_ID"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message_parts", nargs="*", help="Message text if not using --message or stdin.")
    parser.add_argument("-m", "--message", help="Explicit message text.")
    parser.add_argument("--token", help="Telegram bot token. Defaults to env.")
    parser.add_argument("--chat-id", help="Telegram chat id. Defaults to env.")
    parser.add_argument("--token-env", default=DEFAULT_TOKEN_ENV, help=f"Bot token env var. Default: {DEFAULT_TOKEN_ENV}")
    parser.add_argument("--chat-id-env", default=DEFAULT_CHAT_ENV, help=f"Chat id env var. Default: {DEFAULT_CHAT_ENV}")
    parser.add_argument("--parse-mode", choices=["Markdown", "MarkdownV2", "HTML"], help="Telegram parse mode.")
    parser.add_argument("--disable-preview", action="store_true", help="Disable link previews.")
    parser.add_argument("--silent", action="store_true", help="Send without notification.")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds.")
    parser.add_argument("--print-response", action="store_true", help="Print Telegram JSON response.")
    return parser


def _resolve_message(args: argparse.Namespace) -> str:
    if args.message:
        message = args.message
    elif args.message_parts:
        message = " ".join(args.message_parts)
    elif not sys.stdin.isatty():
        message = sys.stdin.read()
    else:
        raise SystemExit("No message provided. Pass text, use --message, or pipe stdin.")

    message = message.strip()
    if not message:
        raise SystemExit("Message is empty.")
    return message


def _resolve_secret(explicit: Optional[str], env_name: str, label: str) -> str:
    value = explicit or os.environ.get(env_name, "")
    if not value:
        raise SystemExit(f"Missing {label}. Pass it explicitly or set ${env_name}.")
    return value


def send_telegram_message(
    *,
    token: str,
    chat_id: str,
    text: str,
    parse_mode: Optional[str] = None,
    disable_preview: bool = False,
    silent: bool = False,
    timeout: int = 20,
) -> dict:
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": "true" if disable_preview else "false",
        "disable_notification": "true" if silent else "false",
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    body = urlencode(payload).encode("utf-8")
    request = Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Telegram API HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise SystemExit(f"Telegram API request failed: {exc}") from exc


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    message = _resolve_message(args)
    token = _resolve_secret(args.token, args.token_env, "Telegram bot token")
    chat_id = _resolve_secret(args.chat_id, args.chat_id_env, "Telegram chat id")

    response = send_telegram_message(
        token=token,
        chat_id=chat_id,
        text=message,
        parse_mode=args.parse_mode,
        disable_preview=args.disable_preview,
        silent=args.silent,
        timeout=args.timeout,
    )
    if not response.get("ok"):
        raise SystemExit(f"Telegram API error: {json.dumps(response, ensure_ascii=False)}")

    if args.print_response:
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print("sent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

