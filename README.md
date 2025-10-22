# Telegram Render Bot (Google Sheets Edition)

Этот проект реализует Telegram-бота, который работает на Render и использует Google Sheets
как базу данных для хранения пользователей, ролей и прочей информации.

## Основные функции:
- Авторизация через `/login <логин> <пароль>` (проверка данных в Google Sheets)
- Привязка Telegram ID к пользователю
- Главное меню с inline-кнопками и подменю с кнопкой "Назад"
- Гибкая структура: все роли, пользователи и объекты — в Google Sheets

## Как развернуть
1. Включите Google Sheets API в Google Cloud Console.
2. Создайте Service Account и скачайте credentials.json.
3. Поделитесь доступом к своей таблице с сервисным аккаунтом.
4. Заполните .env:
    TELEGRAM_TOKEN=...
    GOOGLE_SHEET_ID=...
    GOOGLE_CREDENTIALS_FILE=credentials.json
5. Загрузите проект на Render (Web Service).
6. Выполните `python set_webhook.py` локально или через Render Shell.
