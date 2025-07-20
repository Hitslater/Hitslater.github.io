from aiogram.types import WebAppInfo
from aiogram import types
from .keyboards import keyboard
from .main import dp
from .handlers import dp

web_app = WebAppInfo(url="https://hitslater.github.io/")

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Site", web_app=web_app)]
    ],
    
    resize_keyboard=True
)

@dp.message_handler(commands=['site'])
async def cmd_site(message: types.Message):
    await message.answer("Текст", reply_markup=keyboard)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать!", reply_markup=keyboard)


