from aiogram.types import WebAppInfo
from aiogram import types

web_app = WebAppInfo(url='https://hitslater.github.io/')



keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Site', web_app=web_app)]
    ],
    
    resize_keyboard=True
)

cb = CallbackData('btn', 'action')
key = InLineKeyboardMarkup(
    inline_keyboard = [[InLineKeyboardButton('Pay', callback_data = 'btn:buy')]]    
    
)

