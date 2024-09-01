from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from collections import defaultdict

# Инициализация доступных часов
available_hours = {f"{i}:00": True for i in range(9, 24)}  # Часы с 9:00 до 23:00
students_schedule = defaultdict(list)  # Словарь для хранения расписаний студентов

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Добро пожаловать! Используйте /reserve <часы> для резервирования времени или /free <часы> для освобождения.")

def reserve(update: Update, context: CallbackContext):
    student_name = update.message.from_user.username
    if len(context.args) != 1:
        update.message.reply_text("Используйте: /reserve <часы>, например: /reserve 10:00")
        return
    
    hour = context.args[0]
    if hour in available_hours and available_hours[hour]:
        available_hours[hour] = False
        students_schedule[student_name].append(hour)
        update.message.reply_text(f"Вы зарезервировали {hour}.")
    else:
        update.message.reply_text("Этот час уже занят или не существует.")

def free(update: Update, context: CallbackContext):
    student_name = update.message.from_user.username
    if len(context.args) != 1:
        update.message.reply_text("Используйте: /free <часы>, например: /free 10:00")
        return
    
    hour = context.args[0]
    if hour in students_schedule[student_name]:
        available_hours[hour] = True
        students_schedule[student_name].remove(hour)
        update.message.reply_text(f"Вы освободили {hour}.")
    else:
        update.message.reply_text("Вы не зарезервировали этот час.")

def status(update: Update, context: CallbackContext):
    response = "Доступные часы:\n"
    for hour, is_available in available_hours.items():
        status = "Свободно" if is_available else "Занято"
        response += f"{hour}: {status}\n"
    update.message.reply_text(response)

def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")  # Замените на токен вашего бота
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("reserve", reserve))
    dp.add_handler(CommandHandler("free", free))
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
