import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Расписание
schedule = {
    "Понедельник": ["Свободно", "Свободно", "Свободно"],
    "Вторник": ["Свободно", "Свободно", "Свободно"],
    "Среда": ["Свободно", "Свободно", "Свободно"],
    "Четверг": ["Свободно", "Свободно", "Свободно"],
    "Пятница": ["Свободно", "Свободно", "Свободно"],
}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Используйте /schedule для просмотра расписания.')

def schedule_handler(update: Update, context: CallbackContext) -> None:
    keyboard = []
    for day, hours in schedule.items():
        buttons = [InlineKeyboardButton(f"{hour} ({day})", callback_data=f"{day}:{i}") for i, hour in enumerate(hours)]
        keyboard.append(buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите день и час:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    day, hour_index = query.data.split(":")
    hour_index = int(hour_index)

    if schedule[day][hour_index] == "Свободно":
        query.edit_message_text(text=f"Введите ваше имя для бронирования '{day} - Час {hour_index + 1}':")
        context.user_data['booking'] = (day, hour_index)
    else:
        name = schedule[day][hour_index]
        query.edit_message_text(text=f"Час уже занят {name}. Нажмите /schedule для просмотра расписания.")

def receive_name(update: Update, context: CallbackContext) -> None:
    if 'booking' in context.user_data:
        day, hour_index = context.user_data['booking']
        name = update.message.text
        schedule[day][hour_index] = name
        update.message.reply_text(f"Вы успешно забронировали '{day} - Час {hour_index + 1}' на имя {name}.")
        del context.user_data['booking']
        
    else:
        update.message.reply_text("Пожалуйста, выберите час для бронирования с помощью /schedule.")

def release_hour(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Введите ваше имя для освобождения часа:')
    context.user_data['release'] = True

def process_release_name(update: Update, context: CallbackContext) -> None:
    if 'release' in context.user_data:
        name = update.message.text
        released = False
        for day, hours in schedule.items():
            for i, hour in enumerate(hours):
                if hour == name:
                    schedule[day][i] = "Свободно"
                    released = True
                    update.message.reply_text(f"Час '{day} - Час {i + 1}' успешно освобожден.")
                    break
            if released:
                break
        if not released:
            update.message.reply_text("Вы не занимали ни одного часа.")
        del context.user_data['release']
    else:
        update.message.reply_text("Пожалуйста, используйте команду /release для освобождения часа.")

def main() -> None:
    # Вставьте ваш токен
    updater = Updater("YOUR_TOKEN_HERE")

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("schedule", schedule_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_name))
    updater.dispatcher.add_handler(CommandHandler("release", release_hour))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_release_name))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
