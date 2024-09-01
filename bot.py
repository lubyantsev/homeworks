import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.utils import executor
from aiogram.dispatcher import State, StatesGroup

API_TOKEN = 'YOUR_API_TOKEN_HERE'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание экземпляров бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определение состояний
class ScheduleStates(StatesGroup):
    waiting_for_name = State()

# Расписание
schedule = {
    "Понедельник": ["", "", ""],
    "Вторник": ["", "", ""],
    "Среда": ["", "", ""],
    "Четверг": ["", "", ""],
    "Пятница": ["", "", ""],
}

# Функция для создания кнопок расписания
def get_schedule_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for day, hours in schedule.items():
        for index, name in enumerate(hours):
            button_text = f"{day} - Час {index + 1}: {'Свободно' if not name else name}"
            callback_data = f"{day}:{index}"  # Передаем день и индекс часа
            keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return keyboard

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать в расписание! Используйте кнопки ниже, чтобы занять или освободить время.", reply_markup=get_schedule_keyboard())

@dp.callback_query_handler(filters.Text)
async def handle_schedule(callback_query: types.CallbackQuery):
    day, hour_index = callback_query.data.split(":")
    hour_index = int(hour_index)

    if not schedule[day][hour_index]:  # Если час свободен
        await callback_query.message.answer("Введите ваше имя:")
        await ScheduleStates.waiting_for_name.set()
        # Сохраняем информацию о текущем дне и часу
        await dp.current_state().update_data(day=day, hour_index=hour_index)
    else:  # Если час занят
        name = schedule[day][hour_index]
        await callback_query.message.answer(f"Этот час занят {name}. Хотите освободить его?", reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("Да", callback_data=f"release:{day}:{hour_index}"),
            types.InlineKeyboardButton("Нет", callback_data="cancel")
        ))

@dp.callback_query_handler(lambda c: c.data.startswith('release:'))
async def release_time(callback_query: types.CallbackQuery):
    _, day, hour_index = callback_query.data.split(":")
    hour_index = int(hour_index)
    schedule[day][hour_index] = ""  # Освобождаем час
    await callback_query.answer("Время освобождено!")
    await callback_query.message.edit_reply_markup(get_schedule_keyboard())

@dp.callback_query_handler(lambda c: c.data == "cancel")
async def cancel_action(callback_query: types.CallbackQuery):
    await callback_query.answer("Действие отменено.")

@dp.message_handler(state=ScheduleStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    day = user_data.get('day')
    hour_index = user_data.get('hour_index')

    name = message.text
    schedule[day][hour_index] = name  # Записываем имя в расписание
    await state.finish()
    await message.answer("Вы записаны на этот час!", reply_markup=get_schedule_keyboard())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
