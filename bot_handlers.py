import os
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from google_sheets import get_sheet

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)  # асинхронный бот

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
    keyboard = []
    for row in options:
        buttons = [InlineKeyboardButton(text=item, callback_data=item) for item in row]
        keyboard.append(buttons)
    if add_back:
        keyboard.append([InlineKeyboardButton("⬅ Назад", callback_data="back")])
    return InlineKeyboardMarkup(keyboard)

# Проверка, авторизован ли пользователь
async def is_authorized(chat_id):
    sheet = get_sheet("Users")  # Лист с авторизованными пользователями
    users = sheet.col_values(1)  # Предположим, chat_id в колонке A
    return str(chat_id) in users

# Главная функция обработки обновлений
async def handle_update(update: dict):
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        if text == "/start":
            if await is_authorized(chat_id):
                await send_main_menu(chat_id)
            else:
                await bot.send_message(chat_id=chat_id, text="❌ У вас нет доступа к боту.")
    elif "callback_query" in update:
        callback = update["callback_query"]
        chat_id = callback["message"]["chat"]["id"]
        data = callback["data"]
        if data == "back":
            if await is_authorized(chat_id):
                await send_main_menu(chat_id)
            else:
                await bot.send_message(chat_id=chat_id, text="❌ У вас нет доступа к боту.")
        else:
            await send_submenu(chat_id, data)

# Отправка главного меню
async def send_main_menu(chat_id):
    await bot.send_message(
        chat_id=chat_id,
        text="Главное меню:",
        reply_markup=build_keyboard(MAIN_MENU)
    )

# Отправка подменю с кнопкой "Назад"
async def send_submenu(chat_id, title):
    await bot.send_message(
        chat_id=chat_id,
        text=f"Вы выбрали: *{title}*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=build_keyboard([], add_back=True)
    )
