import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = 'TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token='TOKEN')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calculate = KeyboardButton('Рассчитать')
btn_info = KeyboardButton('Информация')
keyboard_markup.add(btn_calculate, btn_info)

inline_keyboard_markup = InlineKeyboardMarkup()
btn_calories = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
btn_formulas = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
inline_keyboard_markup.add(btn_calories, btn_formulas)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Я бот, помогающий здоровью. Нажми 'Рассчитать', чтобы начать.", reply_markup=keyboard_markup)


@dp.message_handler(lambda message: message.text.lower() == 'рассчитать')
async def main_menu(message: types.Message):
    await message.answer("Выбери опцию:", reply_markup=inline_keyboard_markup)


@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):

    formula = "Формула Миффлина-Сан Жеора:\n\nДля мужчин:\nBMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5\n\nДля женщин:\nBMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161"
    await bot.send_message(call.message.chat.id, formula)
    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await UserState.age.set()
    await bot.send_message(call.message.chat.id, "Введите свой возраст:")
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer("Введите свой рост:")


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer("Введите свой вес:")


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал.")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


