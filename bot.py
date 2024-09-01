import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import State
from aiogram.utils import executor

API_TOKEN = 'YOUR_TOKEN_HERE'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Хранилище для времени
available_time = 10

# Определяем состояния
class Form(State):
    waiting_for_action = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(f'Добро пожаловать! У вас есть {available_time} единиц времени. '
                         'Используйте /occupy для занятия времени и /release для его освобождения.')


@dp.message_handler(commands=['occupy'])
async def occupy_time(message: types.Message):
    global available_time
    if available_time > 0:
        available_time -= 1
        await message.reply(f'Вы заняли 1 единицу времени. Осталось {available_time}.')
    else:
        await message.reply('Время закончилось. Пожалуйста, освободите время.')


@dp.message_handler(commands=['release'])
async def release_time(message: types.Message):
    global available_time
    available_time += 1
    await message.reply(f'Вы освободили 1 единицу времени. Осталось {available_time}.')


@dp.errors_handler()
async def error_handler(update: types.Update, exception: Exception):
    logging.error(f'Update: {update} caused error: {exception}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
