from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from config.settings import settings


@dataclass(frozen=True)
class TelegramSendResult:
    ok: bool
    status_code: int | None = None
    response: Any | None = None
    error: str | None = None


class TelegramService:
    @staticmethod
    def send(text: str) -> TelegramSendResult:
        token = settings.TELEGRAM_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        if not token or not chat_id:
            return TelegramSendResult(
                ok=False,
                error="Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in environment",
            )

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        try:
            resp = requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "disable_web_page_preview": True,
                },
                timeout=15,
            )
            # Avoid crashing the app if Telegram is down or token invalid.
            if not resp.ok:
                return TelegramSendResult(
                    ok=False,
                    status_code=resp.status_code,
                    response=_safe_json(resp),
                    error=f"Telegram API returned HTTP {resp.status_code}",
                )

            return TelegramSendResult(
                ok=True,
                status_code=resp.status_code,
                response=_safe_json(resp),
            )
        except Exception as e:  # noqa: BLE001 - keep app resilient in production
            return TelegramSendResult(ok=False, error=str(e))


def _safe_json(resp: requests.Response) -> Any:
    try:
        return resp.json()
    except Exception:  # noqa: BLE001
        return resp.text