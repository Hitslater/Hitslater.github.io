from aiogram import Bot, Dispatcher
import asyncio
from handlers import start, buy_process, pre_checkout_process, successful_payment, view_cart, clear_cart

bot = Bot(token='8053900025:AAH2h7-SXmdh6CMsK6jor_ZCrWy96k_LB-8')
dp = Dispatcher(bot=bot)

# Регистрация хэндлеров
dp.register_message_handler(start, commands=['start'])
dp.register_message_handler(buy_process, content_types=['web_app_data'])
dp.register_pre_checkout_query_handler(pre_checkout_process, lambda query: True)
dp.register_message_handler(successful_payment, content_types=['successful_payment'])
dp.register_message_handler(view_cart, commands=['viewcart'])
dp.register_message_handler(clear_cart, commands=['clearcart'])

async def main():
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')