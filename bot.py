import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище для времени
available_time = 10

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Добро пожаловать! У вас есть {available_time} единиц времени. '
                              'Используйте /occupy для занятия времени и /release для его освобождения.')

# Команда для занятия времени
def occupy(update: Update, context: CallbackContext) -> None:
    global available_time
    if available_time > 0:
        available_time -= 1
        update.message.reply_text(f'Вы заняли 1 единицу времени. Осталось {available_time}.')
    else:
        update.message.reply_text('Время закончилось. Пожалуйста, освободите время.')

# Команда для освобождения времени
def release(update: Update, context: CallbackContext) -> None:
    global available_time
    available_time += 1
    update.message.reply_text(f'Вы освободили 1 единицу времени. Осталось {available_time}.')

# Обработчик ошибок
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    # Создаем Updater и передаем ему токен вашего бота
    updater = Updater("YOUR_TOKEN_HERE")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("occupy", occupy))
    dispatcher.add_handler(CommandHandler("release", release))

    # Логирование ошибок
    dispatcher.add_error_handler(error)

    # Запускаем бота
    updater.start_polling()

    # Ожидаем завершения работы
    updater.idle()

if __name__ == '__main__':
    main()
