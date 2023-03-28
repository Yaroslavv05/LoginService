from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from validate_email import validate_email
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
import logging
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestTask.settings')
django.setup()

from django.contrib.auth.models import User
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
TOKEN = '5875851778:AAF_Gfrs5vv83JbErvBOYXDSGNHj6YAUOr8'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
hide_keyboard = ReplyKeyboardRemove()
markup0 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup0.add('Реєстрація')
button_link_on_site = InlineKeyboardButton(text='Перейти на сайт', url='http://127.0.0.1:8000/')
inline_kb_full = InlineKeyboardMarkup(row_width=1).add(button_link_on_site)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привіт {message.from_user.full_name}, я бот для реєстрації!', reply_markup=markup0)


class FSMRegistration(StatesGroup):
    username = State()
    email = State()
    password1 = State()
    password2 = State()


@dp.message_handler(content_types=['text'], state=None)
async def main(message: types.Message):
    if message.text == 'Реєстрація':
        await bot.send_message(message.from_user.id, 'Почнемо реєстрацію!', reply_markup=hide_keyboard)
        await FSMRegistration.username.set()
        await bot.send_message(message.from_user.id, "Ім'я користувача:")


@dp.message_handler(state=FSMRegistration.username)
async def username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await FSMRegistration.email.set()
    await bot.send_message(message.from_user.id, 'Пошта:')


@dp.message_handler(state=FSMRegistration.email)
async def username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    is_valid = validate_email(data['email'])
    if is_valid == True:
        await FSMRegistration.password1.set()
        await bot.send_message(message.from_user.id, 'Пароль:\n(Має бути не менше 8 символів!)')
    else:
        await bot.send_message(message.from_user.id, 'Пошту введено неправильно!\nПовторіть спробу:')
        await FSMRegistration.email.set()


@dp.message_handler(state=FSMRegistration.password1)
async def username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password1'] = message.text
    if len(data['password1']) < 8:
        await bot.send_message(message.from_user.id, 'Пароль повинен містити щонайменше 8 символів!\nПовторіть спробу:')
        await FSMRegistration.password1.set()
    else:
        await FSMRegistration.password2.set()
        await bot.send_message(message.from_user.id, 'Повторіть пароль:')


User = get_user_model()


@dp.message_handler(state=FSMRegistration.password2)
async def username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password2'] = message.text
    if data['password1'] == data['password2']:
        await bot.send_message(message.from_user.id, 'Ви успішно зареєструвалися!\nПерейдіть на сайт і увійдіть до свого облікового запису:', reply_markup=inline_kb_full)
        user = await sync_to_async(User.objects.create_user)(username=data['username'], email=data['email'], password=data['password1'])
        await sync_to_async(user.save)()
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Паролі повинні збігатися!\nПовторіть спробу:')
        await FSMRegistration.password2.set()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
else:
    print('Бот не работает!')