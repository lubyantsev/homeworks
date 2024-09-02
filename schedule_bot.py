import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = 'TKN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token='TKN')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    waiting_for_day = State()
    waiting_for_time = State()
    waiting_for_name = State()


days_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton('ПН 401')
btn2 = KeyboardButton('СР 401')
btn3 = KeyboardButton('ЧТ 416')
btn4 = KeyboardButton('СБ 416')
btn5 = KeyboardButton('ВС 415')
days_keyboard.add(btn1, btn2, btn3, btn4, btn5)

time_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
time_btn1 = KeyboardButton('08:00 - 09:30')
time_btn2 = KeyboardButton('10:00 - 11:30')
time_btn3 = KeyboardButton('12:00 - 13:30')
back = KeyboardButton('Назад')
time_keyboard.add(time_btn1, time_btn2, time_btn3, back)

schedule = {day: {time: [] for time in ['08:00 - 09:30', '10:00 - 11:30', '12:00 - 13:30']} for day in ['ПН 401', 'СР 401', 'ЧТ 416', 'СБ 416', 'ВС 415']}


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await UserState.waiting_for_day.set()
    await message.answer("Расписание ↓↓↓↓↓", reply_markup=days_keyboard)


@dp.message_handler(state=UserState.waiting_for_day)
async def choose_day(message: types.Message, state: FSMContext):
    if message.text in ['ПН 401', 'СР 401', 'ЧТ 416', 'СБ 416', 'ВС 415']:
        await state.update_data(day=message.text)
        await UserState.waiting_for_time.set()
        await show_schedule(message.text, message.chat.id)
    else:
        await message.answer("Пожалуйста, выберите день из списка внизу")


async def show_schedule(day: str, chat_id: int):
    schedule_info = f"Расписание на {day}:\n"
    for time, names in schedule[day].items():
        if names:
            schedule_info += f"{time}: {', '.join(names)}\n"
        else:
            schedule_info += f"{time}: Свободно\n"
    await bot.send_message(chat_id, schedule_info)
    await bot.send_message(chat_id, "Выберите время урока ↓↓↓↓↓", reply_markup=time_keyboard)


@dp.message_handler(state=UserState.waiting_for_time)
async def choose_time(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    day = user_data.get('day')

    if message.text in ['08:00 - 09:30', '10:00 - 11:30', '12:00 - 13:30']:
        if schedule[day][message.text]:
            await message.answer("Это время уже занято. Выберите другое время.")
            return

        await state.update_data(time=message.text)
        await UserState.waiting_for_name.set()
        await message.answer("Введите ваше имя:")
    elif message.text == 'Назад':   # как сделать,чтобы кнопка Назад отправляла к выбору времени урока?
        await start(message)   # if message.text is 'Назад': или это здесь?
    else:
        await message.answer("Пожалуйста, выберите время из списка внизу")


@dp.message_handler(state=UserState.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await UserState.waiting_for_time.set()
        user_data = await state.get_data()
        await show_schedule(user_data.get('day'), message.chat.id)
    else:
        user_data = await state.get_data()
        day = user_data.get('day')
        time = user_data.get('time')
        name = message.text

        schedule[day][time].append(name)

        await message.answer(f"Ваше расписание:\nДень: {day}\nВремя: {time}\nИмя: {name}")

        await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
