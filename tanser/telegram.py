import logging
from typing import List, Optional

import httpx
from httpx import HTTPError
from pydantic import BaseModel, ValidationError
from starlette.datastructures import URL
from telethon import TelegramClient, events
from telethon.events import NewMessage

log = logging.getLogger(__name__)


class ButtonsValidator(BaseModel):
    link: str
    text: str


class CommandResponseValidator(BaseModel):
    text: str
    buttons: Optional[List[ButtonsValidator]]


async def telegram_bot(
    api_url: URL, telegram_api_id: int, telegram_api_hash: str, telegram_bot_token: str
):
    client = TelegramClient("manser-bot", telegram_api_id, telegram_api_hash)
    bot = await client.start(bot_token=telegram_bot_token)

    http = httpx.AsyncClient()

    async def _req(url) -> str:
        log.warning("Req to: %r", url)
        try:
            resp = await http.post(url)
            resp.raise_for_status()
            data = CommandResponseValidator(**resp.json())
            return data.text
        except HTTPError:
            log.exception("Failed to request: %r", url)
        except ValidationError:
            log.exception("Failed to parse response")
        except Exception:
            log.exception("Something bad happend")
        return "Ошибка обработки запроса. Повторите позже"

    @bot.on(events.NewMessage(pattern="(/.*)"))
    async def command(event: NewMessage.Event):
        """Send a message when the command /start is issued."""

        comm = event.pattern_match.group(1)
        url = str(api_url) + comm
        await event.respond(await _req(url))
        raise events.StopPropagation

    await bot.run_until_disconnected()
