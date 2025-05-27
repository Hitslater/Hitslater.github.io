from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="🛒 Перейти в магазин",
            web_app=WebAppInfo(url="https://hitslater.github.io/")
        )]
    ]
)