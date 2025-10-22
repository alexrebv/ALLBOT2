from flask import Flask, request
import os
from google_sheets import append_row

app = Flask(__name__)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # Токен бота
WEBHOOK_PATH = f"/webhook/{TELEGRAM_TOKEN}"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = request.get_json()
    if not update:
        return "ok", 200

    chat_id = update.get("message", {}).get("chat", {}).get("id")
    text = update.get("message", {}).get("text")

    if chat_id and text:
        # Добавляем в Google Sheet
        append_row("Лист1", [chat_id, text])

    return "ok", 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)

