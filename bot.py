import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создаем глобальную переменную для хранения расписания
schedule = {
    "Пн": [None, None, None],  # 3 часа
    "Вт": [None, None, None],
    "Ср": [None, None, None],
    "Чт": [None, None, None],
    "Пт": [None, None, None],
    "Сб": [None, None, None],
    "Вс": [None, None, None],
}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Добро пожаловать! Используйте /schedule для просмотра расписания.')

def schedule_command(update: Update, context: CallbackContext) -> None:
    keyboard = []
    for day, hours in schedule.items():
        row = []
        for i, name in enumerate(hours):
            if name is None:
                button_text = f"{day} Час {i+1}: Свободно"
            else:
                button_text = f"{day} Час {i+1}: {name}"
            row.append(InlineKeyboardButton(button_text, callback_data=f"{day}_{i}"))
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Расписание:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    day, hour_index = query.data.split('_')
    hour_index = int(hour_index)

    # Если час свободен, предложите записаться
    if schedule[day][hour_index] is None:
        query.edit_message_text(text=f'Введите ваше имя для записи на {day} Час {hour_index + 1}:')
        return

    # Если час занят, предложите освободить
    student_name = schedule[day][hour_index]
    query.edit_message_text(text=f'На {day} Час {hour_index + 1} записан {student_name}. Освободить? (да/нет)')

def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip()
    if text.lower() == "да":
        query = context.user_data.get('last_query')
        if query:
            day, hour_index = query.split('_')
            hour_index = int(hour_index)
            schedule[day][hour_index] = None
            update.message.reply_text(f'Время {day} Час {hour_index + 1} освобождено!')
            context.user_data.pop('last_query')
            return
    elif text.lower() == "нет":
        update.message.reply_text('Запись отменена.')
        context.user_data.pop('last_query')
        return

    if update.message.reply_to_message:
        day, hour_index = context.user_data.get('last_query').split('_')
        hour_index = int(hour_index)
        
        # Записываем имя студента
        schedule[day][hour_index] = text
        update.message.reply_text(f'Вы записались на {day} Час {hour_index + 1} как {text}!')
        context.user_data.pop('last_query')

def main() -> None:
    # Вставьте сюда токен вашего бота
    updater = Updater("YOUR_TOKEN_HERE")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("schedule", schedule_command))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
