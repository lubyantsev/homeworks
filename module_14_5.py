from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from crud_functions import initiate_db, add_user, is_included

API_TOKEN = '7496069476:AAEmEJvx70OUkElm_JV8q4BypnswN3Nk0aA'  # Замените на ваш токен

bot = Bot(token='7496069476:AAEmEJvx70OUkElm_JV8q4BypnswN3Nk0aA')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
btn_register = KeyboardButton('Регистрация')
btn_calculate = KeyboardButton('Рассчитать')
btn_info = KeyboardButton('Информация')
btn_buy = KeyboardButton('Купить')
keyboard_markup.add(btn_register, btn_calculate, btn_info, btn_buy)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Я бот, помогающий здоровью. Нажми 'Регистрация', чтобы начать.", reply_markup=keyboard_markup)


@dp.message_handler(lambda message: message.text.lower() == 'регистрация')
async def sign_up(message: types.Message):
    await RegistrationState.username.set()
    await message.answer("Введите имя пользователя (только латинский алфавит):")


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя.")
    else:
        await state.update_data(username=username)
        await RegistrationState.email.set()
        await message.answer("Введите свой email:")


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await RegistrationState.age.set()
    await message.answer("Введите свой возраст:")


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)

    data = await state.get_data()
    username = data['username']
    email = data['email']

    add_user(username, email, age)

    await message.answer("Вы успешно зарегистрированы!")
    await state.finish()

if __name__ == '__main__':
    initiate_db()
    executor.start_polling(dp, skip_updates=True)
