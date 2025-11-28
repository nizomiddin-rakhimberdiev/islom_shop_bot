from django.apps import AppConfig
import asyncio
from aiogram import Bot
from django.conf import settings


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'   # MUHIM!!!

    def ready(self):
        """
        Webhook faqat production muhitda o‘rnatiladi.
        Local (DEBUG=True) vaqtida webhook o‘rnatish ishlamaydi
        va xatoga sabab bo‘lmaydi.
        """
        if settings.DEBUG:
            # Local development, webhook qo‘ymaymiz
            return

        # Production serverda (Render) webhook o‘rnatamiz
        try:
            asyncio.run(self.set_webhook())
        except RuntimeError:
            # Agar event loop allaqachon bo'lsa (gunicorn), asyncio.run ishlamaydi
            loop = asyncio.get_event_loop()
            loop.create_task(self.set_webhook())

    async def set_webhook(self):
        bot = Bot(settings.BOT_TOKEN)
        await bot.set_webhook(settings.WEBHOOK_URL)
