import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StateGroup
from aiogram.utils import executor

API_TOKEN = 'YOUR_API_TOKEN'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определение состояний
class UserState(StateGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Напишите 'Calories', чтобы начать.")

@dp.message_handler(lambda message: message.text.lower() == 'calories')
async def set_age(message: types.Message):
    await UserState.age.set()  # Устанавливаем состояние age
    await message.answer("Введите свой возраст:")

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)  # Сохраняем возраст
    await UserState.growth.set()  # Устанавливаем состояние growth
    await message.answer("Введите свой рост:")

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)  # Сохраняем рост
    await UserState.weight.set()  # Устанавливаем состояние weight
    await message.answer("Введите свой вес:")

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)  # Сохраняем вес
    data = await state.get_data()  # Получаем все данные

    # Получаем значения из данных
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    # Здесь выбираем формулу для мужчин или женщин. В данном примере для мужчин.
    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f"Норма калорий: {calories:.2f} ккал.")
    await state.finish()  # Завершаем состояние

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
