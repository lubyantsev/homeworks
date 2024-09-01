import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = 'YOUR_API_TOKEN_HERE'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния
class ScheduleStates(StatesGroup):
    waiting_for_name = State()

# Расписание
schedule = {
    "Понедельник": ["Свободно", "Свободно", "Свободно"],
    "Вторник": ["Свободно", "Свободно", "Свободно"],
    "Среда": ["Свободно", "Свободно", "Свободно"],
    "Четверг": ["Свободно", "Свободно", "Свободно"],
    "Пятница": ["Свободно", "Свободно", "Свободно"],
    "Суббота": ["Свободно", "Свободно", "Свободно"],
    "Воскресенье": ["Свободно", "Свободно", "Свободно"],
}

# Функция для отображения расписания
def get_schedule_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for day, hours in schedule.items():
        for i, status in enumerate(hours):
            button_text = f"{day} - Час {i + 1}: {status}"
            callback_data = f"{day}_{i}"
            keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return keyboard

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer("Вот расписание на неделю:", reply_markup=get_schedule_keyboard())

@dp.callback_query_handler(lambda c: True)
async def process_schedule(callback_query: types.CallbackQuery):
    day, hour = callback_query.data.split("_")
    hour = int(hour)

    if schedule[day][hour] == "Свободно":
        await ScheduleStates.waiting_for_name.set()
        await bot.send_message(callback_query.from_user.id, "Введите ваше имя:")
        await bot.answer_callback_query(callback_query.id)
    else:
        name = schedule[day][hour]
        await bot.send_message(callback_query.from_user.id, f"Этот час занят: {name}. Хотите освободить его? (Да/Нет)", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Да", "Нет"))
        await bot.answer_callback_query(callback_query.id)

@dp.message_handler(state=ScheduleStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    day, hour = message.reply_to_message.text.split(" - ")[0], int(message.reply_to_message.text.split(" - Час ")[1].split(":")[0]) - 1
    schedule[day][hour] = name
    await state.finish()
    await message.answer("Вы записаны на этот час!", reply_markup=get_schedule_keyboard())

@dp.message_handler(lambda message: message.text.lower() in ["да", "нет"], state='*')
async def process_free_time(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        day, hour = message.reply_to_message.text.split(" - ")[0], int(message.reply_to_message.text.split(" - Час ")[1].split(":")[0]) - 1
        schedule[day][hour] = "Свободно"
        await message.answer("Время освобождено.", reply_markup=get_schedule_keyboard())
    else:
        await message.answer("Окей, время остается занятым.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
