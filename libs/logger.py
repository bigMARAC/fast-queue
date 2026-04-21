import logging
import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

class DiscordHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        msg =  "🚨 **ERRO CRÍTICO NO SISTEMA** 🚨" if record.levelno >= logging.ERROR else "⚠️ **AVISO NO SISTEMA** ⚠️"
        payload = {"content": f"{msg}\n```{log_entry}```"}

        asyncio.create_task(self.send_to_discord(payload))

    async def send_to_discord(self, payload):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(DISCORD_WEBHOOK_URL, json=payload)
            except Exception:
                pass

def setup_logger(service_name: str):
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "service": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    discord_handler = DiscordHandler()
    discord_handler.setFormatter(formatter)
    logger.addHandler(discord_handler)

    return logger