import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Расписание на неделю
schedule = {
    'Понедельник': ['09:00', '10:00', '11:00'],
    'Вторник': ['09:00', '10:00', '11:00'],
    'Среда': ['09:00', '10:00', '11:00'],
    'Четверг': ['09:00', '10:00', '11:00'],
    'Пятница': ['09:00', '10:00', '11:00'],
}

# Словарь для хранения занятых часов
booked_slots = {day: [None] * len(times) for day, times in schedule.items()}

# Функция для отображения расписания
def start(update: Update, context: CallbackContext) -> None:
    keyboard = []
    for day, times in schedule.items():
        buttons = []
        for i, time in enumerate(times):
            status = booked_slots[day][i]
            if status is None:
                button_text = time + " (Свободно)"
            else:
                button_text = time + f" (Занято: {status})"
            buttons.append(InlineKeyboardButton(button_text, callback_data=f"{day}_{i}"))
        keyboard.append(buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите день и время:', reply_markup=reply_markup)

# Обработка нажатий на кнопки
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    day, index = query.data.split('_')
    index = int(index)
    
    if booked_slots[day][index] is None:
        # Бронирование
        query.message.reply_text("Введите ваше имя:")
        context.user_data['booking'] = (day, index)
    else:
        # Освобождение
        query.message.reply_text("Вы хотите освободить это время? (Да/Нет)")
        context.user_data['unbooking'] = (day, index)

# Обработка ввода имени
def handle_message(update: Update, context: CallbackContext) -> None:
    if 'booking' in context.user_data:
        day, index = context.user_data['booking']
        name = update.message.text
        booked_slots[day][index] = name
        del context.user_data['booking']
        start(update, context)
    elif 'unbooking' in context.user_data:
        day, index = context.user_data['unbooking']
        if update.message.text.lower() in ['да', 'yes']:
            booked_slots[day][index] = None
        del context.user_data['unbooking']
        start(update, context)

def main() -> None:
    # Вставьте свой токен ниже
    updater = Updater("YOUR_TOKEN_HERE")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запускаем бота
    updater.start_polling()

    # Ожидаем завершения работы
    updater.idle()

if __name__ == '__main__':
    main()
