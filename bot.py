import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, State, StatesGroup
from aiogram.utils import executor
from aiogram.dispatcher import filters

API_TOKEN = 'YOUR_API_TOKEN'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определение состояний
class FormState(StatesGroup):
    enter_name = State()

# Расписание
schedule = {
    "Monday": ["Free", "Free", "Free"],
    "Tuesday": ["Free", "Free", "Free"],
    "Wednesday": ["Free", "Free", "Free"],
    "Thursday": ["Free", "Free", "Free"],
    "Friday": ["Free", "Free", "Free"],
}

# Функция для создания клавиатуры
def create_schedule_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for day in schedule.keys():
        keyboard.add(types.KeyboardButton(day))
    return keyboard

def create_hours_keyboard(day):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for hour in range(3):
        button_text = f"{hour + 1} - {schedule[day][hour]}"
        keyboard.add(types.KeyboardButton(button_text))
    keyboard.add(types.KeyboardButton("Назад"))
    return keyboard

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Выберите день недели:", reply_markup=create_schedule_keyboard())

@dp.message_handler(filters.Text(equals=list(schedule.keys())))
async def show_hours(message: types.Message):
    day = message.text
    await message.answer(f"Часы для {day}:", reply_markup=create_hours_keyboard(day))

@dp.message_handler(filters.Text(startswith=[f"{i + 1} - " for i in range(3)]))
async def occupy_hour(message: types.Message):
    day = message.reply_to_message.text.split(" ")[-1]
    hour_index = int(message.text.split(" ")[0]) - 1
    current_status = schedule[day][hour_index]

    if current_status == "Free":
        await FormState.enter_name.set()
        await message.answer("Введите ваше имя:")
        await message.answer(f"Вы заняли {day} {hour_index + 1} час.")
    else:
        await message.answer(f"{day} {hour_index + 1} уже занят именем '{current_status}'.\nХотите освободить это время? (да/нет)")

@dp.message_handler(state=FormState.enter_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    day = message.reply_to_message.text.split(" ")[-1]
    hour_index = int(message.reply_to_message.text.split(" ")[0]) - 1

    schedule[day][hour_index] = name
    await state.finish()
    await message.answer(f"Вы успешно заняли {day} {hour_index + 1} час. Ваше имя: {name}")

@dp.message_handler(lambda message: message.text.lower() in ["да", "нет"])
async def handle_confirmation(message: types.Message):
    if message.text.lower() == "да":
        # Здесь нужно освободить время
        day = message.reply_to_message.text.split(" ")[-1]
        hour_index = int(message.reply_to_message.text.split(" ")[0]) - 1
        schedule[day][hour_index] = "Free"
        await message.answer(f"{day} {hour_index + 1} час освобожден.")
    else:
        await message.answer("Время не освобождено.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
