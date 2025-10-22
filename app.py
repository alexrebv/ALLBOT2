from flask import Flask, request
import os
import asyncio
from bot_handlers import handle_update

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Маршрут для webhook
@app.route(f"/webhook/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    # Запускаем асинхронную функцию через asyncio
    asyncio.run(handle_update(update))
    return "OK", 200

# Проверка работы сервера
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
