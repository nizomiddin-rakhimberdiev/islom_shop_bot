import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram.types import Update
from .bot import bot, dp

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        update = Update(**data)
        dp.feed_update(bot, update)   # Aiogramga update berish
        return JsonResponse({"ok": True})

    return JsonResponse({"status": "method not allowed"})
