from aiogram import Bot 
from aiogram import Dispatcher

import asyncio

bot = Bot(token='8053900025:AAH2h7-SXmdh6CMsK6jor_ZCrWy96k_LB-8')
dp = Dispatcher(bot=bot)

async def main():
    from handlers import dp
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')
