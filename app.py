import os
from flask import Flask, request, abort
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import bot_handlers as handlers

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set")

app = Flask(__name__)
bot = Bot(token=TOKEN)

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)
dispatcher.add_handler(CommandHandler("start", handlers.start))
dispatcher.add_handler(CommandHandler("login", handlers.cmd_login))
dispatcher.add_handler(CommandHandler("whoami", handlers.cmd_whoami))
dispatcher.add_handler(CallbackQueryHandler(handlers.handle_menu_callback))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update_json = request.get_json(force=True)
        update = Update.de_json(update_json, bot)
        dispatcher.process_update(update)
        return "OK", 200
    else:
        abort(403)

@app.route("/")
def index():
    return "Telegram bot with Google Sheets integration is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
