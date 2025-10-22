from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from google_sheets import find_user_by_login, update_telegram_id, find_user_by_tg_id, get_user_role

MENU_KEYS = [
    ("Данные о точке", "point_info"),
    ("Заказы", "orders"),
    ("Не принятые накладные", "not_accepted"),
    ("Вычерки (фиксация)", "crossouts_fix"),
    ("Вычерки Есалукова", "crossouts_esalukov"),
    ("Расписание заказов", "orders_schedule"),
    ("Расписание заказа воды", "water_order_schedule"),
    ("Информация о поставщике", "supplier_info"),
]

def build_main_menu():
    buttons, row = [], []
    for i, (label, key) in enumerate(MENU_KEYS, 1):
        row.append(InlineKeyboardButton(label, callback_data=f"menu:{key}"))
        if i % 2 == 0:
            buttons.append(row); row = []
    if row: buttons.append(row)
    buttons.append([InlineKeyboardButton("❌ Закрыть", callback_data="menu:close")])
    return InlineKeyboardMarkup(buttons)

def build_back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="menu:main")]])

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = find_user_by_tg_id(chat_id)
    if user:
        text = f"Главное меню (роль: {user.get('Роль', 'не указана')})"
    else:
        text = "Вы не авторизованы. Используйте /login <логин> <пароль>."
    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=build_main_menu())

def handle_menu_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    query.answer()
    if not data.startswith("menu:"): return
    key = data.split(":", 1)[1]
    if key == "main":
        query.edit_message_text("Главное меню", reply_markup=build_main_menu()); return
    if key == "close":
        try: query.message.delete()
        except Exception: query.edit_message_text("Закрыто."); return

    text_map = {
        "point_info": "Информация о точке...",
        "orders": "Ваши заказы...",
        "not_accepted": "Не принятые накладные...",
        "crossouts_fix": "Вычерки (фиксация)...",
        "crossouts_esalukov": "Вычерки Есалукова...",
        "orders_schedule": "Расписание заказов...",
        "water_order_schedule": "Расписание заказа воды...",
        "supplier_info": "Информация о поставщике...",
    }
    text = text_map.get(key, "Раздел в разработке.")
    query.edit_message_text(text=text, reply_markup=build_back_keyboard())

def cmd_login(update: Update, context: CallbackContext):
    args = context.args
    if len(args) < 2:
        update.message.reply_text("Использование: /login <логин> <пароль>"); return
    login, password = args[0], args[1]
    user = find_user_by_login(login)
    if not user:
        update.message.reply_text("Пользователь не найден."); return
    if str(user.get("Пароль", "")).strip() != password:
        update.message.reply_text("Неверный пароль."); return
    tg_id = str(update.effective_user.id)
    update_telegram_id(login, tg_id)
    update.message.reply_text(f"✅ Авторизация успешна. Telegram ID привязан ({tg_id}).")

def cmd_whoami(update: Update, context: CallbackContext):
    tg_id = str(update.effective_user.id)
    user = find_user_by_tg_id(tg_id)
    if not user:
        update.message.reply_text("Вы не авторизованы."); return
    update.message.reply_text(f"Вы: {user['Логин']} (роль: {user.get('Роль','?')})")
