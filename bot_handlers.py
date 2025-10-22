from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)

# Главное меню
MAIN_MENU = [
    ["Данные о точке"],
    ["Заказы"],
    ["Не принятые накладные"],
    ["Вычерки (фиксация)"],
    ["Вычерки Есалукова"],
    ["Расписание заказов"],
    ["Расписание заказа воды"],
    ["Информация о поставщике"]
]

def build_keyboard(options, add_back=False):
    """
    Создаёт инлайн-кнопки. 
    add_back=True добавляет кнопку 'Назад'.
    """
    keyboard = []
    for row in options:
        buttons = [InlineKeyboardButton(text=item, callback_data=item) for item in row]
        keyboard.append(buttons)
    if add_back:
        keyboard.append([InlineKeyboardButton("⬅ Назад", callback_data="back")])
    return InlineKeyboardMarkup(keyboard)

def handle_update(update: dict):
    """
    Основная функция обработки апдейтов от Telegram.
    """
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            send_main_menu(chat_id)

    elif "callback_query" in update:
        callback = update["callback_query"]
        chat_id = callback["message"]["chat"]["id"]
        data = callback["data"]

        if data == "back":
            send_main_menu(chat_id)
        else:
            send_submenu(chat_id, data)

def send_main_menu(chat_id):
    bot.send_message(
        chat_id=chat_id,
        text="Главное меню:",
        reply_markup=build_keyboard(MAIN_MENU)
    )

def send_submenu(chat_id, title):
    # Здесь можно добавить динамическую логику для подменю
    bot.send_message(
        chat_id=chat_id,
        text=f"Вы выбрали: *{title}*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=build_keyboard([], add_back=True)  # Только кнопка "Назад"
    )
