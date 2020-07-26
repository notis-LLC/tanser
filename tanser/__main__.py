import asyncio
import logging

from fastapi import FastAPI

from tanser.config import (
    DEBUG,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_REST_API_URL,
)
from tanser.handling import router
from tanser.telegram import telegram_bot

log = logging.getLogger(__name__)


async def up():
    app.state.telegram_task_id = asyncio.create_task(
        telegram_bot(
            TELEGRAM_REST_API_URL,
            TELEGRAM_API_ID,
            TELEGRAM_API_HASH,
            TELEGRAM_BOT_TOKEN,
        )
    )


async def down():
    app.state.telegram_task_id.cancel()


app = FastAPI(debug=DEBUG, on_startup=[up], on_shutdown=[down])
app.router = router
