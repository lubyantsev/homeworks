import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '7496069476:AAEmEJvx70OUkElm_JV8q4BypnswN3Nk0aA'  # Замените на ваш токен

logging.basicConfig(level=logging.INFO)

bot = Bot(token='7496069476:AAEmEJvx70OUkElm_JV8q4BypnswN3Nk0aA')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Основная клавиатура
keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calculate = KeyboardButton('Рассчитать')
btn_info = KeyboardButton('Информация')
btn_buy = KeyboardButton('Купить')
keyboard_markup.add(btn_calculate, btn_info, btn_buy)

# Inline клавиатура для продуктов
inline_keyboard_markup = InlineKeyboardMarkup()
btn_product1 = InlineKeyboardButton('Product1', callback_data='product_buying')
btn_product2 = InlineKeyboardButton('Product2', callback_data='product_buying')
btn_product3 = InlineKeyboardButton('Product3', callback_data='product_buying')
btn_product4 = InlineKeyboardButton('Product4', callback_data='product_buying')
inline_keyboard_markup.add(btn_product1, btn_product2, btn_product3, btn_product4)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Я бот, помогающий здоровью. Нажми 'Рассчитать', чтобы начать.", reply_markup=keyboard_markup)

@dp.message_handler(lambda message: message.text.lower() == 'рассчитать')
async def main_menu(message: types.Message):
    await message.answer("Выбери опцию:", reply_markup=inline_keyboard_markup)

@dp.message_handler(lambda message: message.text.lower() == 'купить')
async def get_buying_list(message: types.Message):
    # Список продуктов с их изображениями
    products = [
        {
            'name': 'Витамин Щ',
            'description': 'Помогает',
            'price': 100,
            'image_path': r'C:\Users\Александр Лубянцев\Desktop\2024-09-06_11-51-47.png'
        },
        {
            'name': 'Витамин Ч',
            'description': 'Лучше не покупать',
            'price': 200,
            'image_path': r'C:\Users\Александр Лубянцев\Desktop\institut_de_angeli_relif_supp._rekt._12_1093630_1.jpg'
        },
        {
            'name': 'Витамин Х',
            'description': 'Только для женщин',
            'price': 300,
            'image_path': r'C:\Users\Александр Лубянцев\Desktop\6019510984.jpg'
        },
        {
            'name': 'Витаминный комплекс',
            'description': 'Лучше поесть чего-нибудь',
            'price': 400,
            'image_path': r'C:\Users\Александр Лубянцев\Desktop\1638957_43207078.jpeg'
        },
    ]

    for product in products:
        # Формируем строку с информацией о продукте
        product_info = f'Название: {product["name"]} | Описание: {product["description"]} | Цена: {product["price"]}\n'
        await message.answer(product_info)  # Отправляем информацию о продукте
        await bot.send_photo(message.chat.id, photo=open(product['image_path'], 'rb'))  # Отправляем изображение

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard_markup)

@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, "Вы успешно приобрели продукт!")
    await call.answer()

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
