import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Списки часов и зарезервированных часов
hours = [f"{i}:00" for i in range(15)]
reserved_hours = set()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Добро пожаловать! Используйте /schedule для просмотра расписания.')

def schedule(update: Update, context: CallbackContext) -> None:
    keyboard = []
    for hour in hours:
        if hour in reserved_hours:
            button = InlineKeyboardButton(f"{hour} (занято)", callback_data=f"free_{hour}")
        else:
            button = InlineKeyboardButton(f"{hour} (свободно)", callback_data=f"reserve_{hour}")
        keyboard.append([button])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите час:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    action, hour = query.data.split('_')

    if action == "reserve":
        if len(reserved_hours) < 15:
            reserved_hours.add(hour)
            query.edit_message_text(text=f"Час {hour} зарезервирован.")
        else:
            query.edit_message_text(text="Все часы заняты!")
    elif action == "free":
        reserved_hours.remove(hour)
        query.edit_message_text(text=f"Час {hour} освобожден.")

def main() -> None:
    # Вставьте свой токен здесь
    updater = Updater("YOUR_TOKEN_HERE")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("schedule", schedule))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
